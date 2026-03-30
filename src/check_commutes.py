import os
import time
from pathlib import Path
import requests
import pandas as pd
from sqlalchemy import text
from dotenv import load_dotenv
from db import get_engine

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
COMPANY_ADDRESS = os.getenv("COMPANY_ADDRESS", "1362 Avenue des Platanes, 34970 Lattes, France")

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"

SPORT_COMMUTE_RULES = {
    "Marche/Running": {"travel_mode": "WALK", "max_km": 15},
    "Vélo/Trottinette/Autres": {"travel_mode": "BICYCLE", "max_km": 25},
}

def geocode_address(address, cache):
    if not address or pd.isna(address):
        return None

    address = str(address).strip()
    if address in cache:
        return cache[address]

    r = requests.get(
        GEOCODE_URL,
        params={"address": address, "key": API_KEY},
        timeout=30
    )

    data = r.json()

    if data.get("status") != "OK":
        cache[address] = None
        return None

    loc = data["results"][0]["geometry"]["location"]
    result = {"lat": loc["lat"], "lng": loc["lng"]}
    cache[address] = result
    return result

def compute_route_distance(origin_coords, destination_coords, travel_mode):
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.distanceMeters,routes.duration"
    }

    payload = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": origin_coords["lat"],
                    "longitude": origin_coords["lng"]
                }
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": destination_coords["lat"],
                    "longitude": destination_coords["lng"]
                }
            }
        },
        "travelMode": travel_mode,
        "languageCode": "fr"
    }

    r = requests.post(ROUTES_URL, headers=headers, json=payload, timeout=30)

    if r.status_code != 200:
        return None, f"ROUTES_API_ERROR {r.status_code}: {r.text[:300]}"

    data = r.json()
    routes = data.get("routes", [])

    if not routes:
        return None, "Aucun itinéraire retourné"

    distance_m = routes[0].get("distanceMeters")
    if distance_m is None:
        return None, "Distance absente dans la réponse"

    return round(distance_m / 1000, 2), None

def check_commutes():
    engine = get_engine()

    employees_df = pd.read_sql("""
        SELECT employee_id, full_name, home_address, commute_mode
        FROM employees
        ORDER BY employee_id
    """, engine)

    geocode_cache = {}
    company_coords = geocode_address(COMPANY_ADDRESS, geocode_cache)

    if not company_coords:
        raise ValueError("Impossible de géocoder l'adresse de l'entreprise.")

    results = []

    for _, row in employees_df.iterrows():
        employee_id = row["employee_id"]
        employee_name = row["full_name"]
        home_address = row["home_address"]
        commute_mode = row["commute_mode"]

        rule = SPORT_COMMUTE_RULES.get(commute_mode)

        if not rule:
            results.append({
                "employee_id": employee_id,
                "employee_name": employee_name,
                "home_address": home_address,
                "company_address": COMPANY_ADDRESS,
                "commute_mode": commute_mode,
                "distance_km": None,
                "max_allowed_km": None,
                "validation_status": "NOT_APPLICABLE",
                "validation_comment": "Mode non concerné par la prime sportive"
            })
            continue

        if not home_address or pd.isna(home_address):
            results.append({
                "employee_id": employee_id,
                "employee_name": employee_name,
                "home_address": home_address,
                "company_address": COMPANY_ADDRESS,
                "commute_mode": commute_mode,
                "distance_km": None,
                "max_allowed_km": rule["max_km"],
                "validation_status": "ERROR",
                "validation_comment": "Adresse domicile manquante"
            })
            continue

        try:
            home_coords = geocode_address(home_address, geocode_cache)

            if not home_coords:
                results.append({
                    "employee_id": employee_id,
                    "employee_name": employee_name,
                    "home_address": home_address,
                    "company_address": COMPANY_ADDRESS,
                    "commute_mode": commute_mode,
                    "distance_km": None,
                    "max_allowed_km": rule["max_km"],
                    "validation_status": "ERROR",
                    "validation_comment": "Géocodage impossible"
                })
                continue

            distance_km, route_error = compute_route_distance(
                origin_coords=home_coords,
                destination_coords=company_coords,
                travel_mode=rule["travel_mode"]
            )

            if route_error:
                results.append({
                    "employee_id": employee_id,
                    "employee_name": employee_name,
                    "home_address": home_address,
                    "company_address": COMPANY_ADDRESS,
                    "commute_mode": commute_mode,
                    "distance_km": None,
                    "max_allowed_km": rule["max_km"],
                    "validation_status": "ERROR",
                    "validation_comment": route_error
                })
                continue

            max_allowed_km = rule["max_km"]

            if distance_km <= max_allowed_km:
                status = "VALID"
                comment = f"Distance cohérente ({distance_km} km)"
            else:
                status = "TO_REVIEW"
                comment = f"Distance au-dessus du seuil ({distance_km} km > {max_allowed_km} km)"

            results.append({
                "employee_id": employee_id,
                "employee_name": employee_name,
                "home_address": home_address,
                "company_address": COMPANY_ADDRESS,
                "commute_mode": commute_mode,
                "distance_km": distance_km,
                "max_allowed_km": max_allowed_km,
                "validation_status": status,
                "validation_comment": comment
            })

            time.sleep(0.10)

        except Exception as e:
            results.append({
                "employee_id": employee_id,
                "employee_name": employee_name,
                "home_address": home_address,
                "company_address": COMPANY_ADDRESS,
                "commute_mode": commute_mode,
                "distance_km": None,
                "max_allowed_km": rule["max_km"],
                "validation_status": "ERROR",
                "validation_comment": str(e)[:300]
            })

    results_df = pd.DataFrame(results)

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE commute_checks"))

    results_df.to_sql("commute_checks", engine, if_exists="append", index=False)

    print("Contrôle des trajets terminé.")
    print(f"commute_checks : {len(results_df)} lignes")
    print("\nRépartition des statuts :")
    print(results_df["validation_status"].value_counts())

if __name__ == "__main__":
    check_commutes()
