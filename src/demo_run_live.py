import subprocess
import sys

PYTHON_BIN = sys.executable

STEPS = [
    ("État avant", f"{PYTHON_BIN} src/demo_show_status.py"),
    ("Ajout des activités de démo", f"{PYTHON_BIN} src/demo_add_activity.py"),
    ("Recalcul des avantages", f"{PYTHON_BIN} src/calculate_rewards.py"),
    ("Contrôles qualité", f"{PYTHON_BIN} src/run_quality_checks.py"),
    ("Snapshot KPI", f"{PYTHON_BIN} src/capture_kpi_snapshot.py"),
    ("Volumétrie", f"{PYTHON_BIN} src/capture_table_volumes.py"),
    ("Envoi Slack", f"{PYTHON_BIN} src/send_slack_message.py"),
    ("État après", f"{PYTHON_BIN} src/demo_show_status.py"),
]


def main():
    for label, command in STEPS:
        print(f"\n=== {label} ===")
        print(f"Commande : {command}")

        result = subprocess.run(command, shell=True, text=True)

        if result.returncode != 0:
            print("\nLa démonstration s'est arrêtée sur une erreur.")
            sys.exit(result.returncode)

    print("\nDémo live terminée avec succès.")


if __name__ == "__main__":
    main()