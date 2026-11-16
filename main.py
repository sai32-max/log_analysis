from ingestion.read import ingest
from processing.extract_transform import extract
from processing.geolocation import geo_location
from storage.db import get_connection, create_table, clear_attempts, insert_attempts


def main():
    lines = ingest("./data")
    if not lines:
        print("Aucune ligne lue, arrêt.")
        return

    events = [e for e in (extract(line) for line in lines) if e]
    print(f"{len(events)} événements utiles sur {len(lines)} lignes")

    unique_ips = {e["ip"] for e in events}
    print(f"{len(unique_ips)} IP à géolocaliser (cela peut prendre plusieurs minutes)")
    countries = {ip: geo_location(ip) for ip in unique_ips}

    rows = [
        (e["time"], e["event"], e["user"], e["ip"], countries[e["ip"]])
        for e in events
    ]

    conn = get_connection()
    create_table(conn)
    clear_attempts(conn)
    insert_attempts(conn, rows)
    conn.close()
    print(f"{len(rows)} lignes enregistrées dans PostgreSQL")


if __name__ == "__main__":
    main()