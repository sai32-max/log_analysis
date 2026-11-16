import logging
import os

from ingestion.read import ingest
from processing.extract_transform import extract
from processing.geolocation import geo_location
from storage.db import get_connection, create_table, clear_attempts, insert_attempts

logger = logging.getLogger("main")


def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s : %(message)s",
        handlers=[
            logging.FileHandler(os.path.join("logs", "app.log"), encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def main():
    lines = ingest("./data")
    if not lines:
        logger.error("Aucune ligne lue dans ./data, arrêt du programme")
        return

    events = [e for e in (extract(line) for line in lines) if e]
    logger.info("%d événements utiles sur %d lignes", len(events), len(lines))

    unique_ips = {e["ip"] for e in events}
    logger.info("%d IP à géolocaliser", len(unique_ips))
    countries = {ip: geo_location(ip) for ip in unique_ips}
    missing = sum(1 for c in countries.values() if c is None)
    logger.warning("%d IP sans pays trouvé", missing)

    rows = [
        (e["time"], e["event"], e["user"], e["ip"], countries[e["ip"]])
        for e in events
    ]

    conn = get_connection()
    try:
        create_table(conn)
        clear_attempts(conn)
        insert_attempts(conn, rows)
        logger.info("%d lignes enregistrées dans PostgreSQL", len(rows))
    except Exception:
        logger.exception("Erreur pendant l'enregistrement dans PostgreSQL")
    finally:
        conn.close()


if __name__ == "__main__":
    setup_logging()
    try:
        main()
    except Exception:
        logger.exception("Erreur inattendue dans le pipeline")