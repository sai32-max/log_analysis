import psycopg2


def load_env(path=".env"):
    """Lit le fichier .env (lignes CLE=VALEUR) et renvoie un dictionnaire."""
    values = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip()
    return values


def get_connection():
    env = load_env()
    return psycopg2.connect(
        host=env.get("PG_HOST", "localhost"),
        port=env.get("PG_PORT", "5432"),
        dbname=env.get("PG_DB", "log_analysis"),
        user=env.get("PG_USER", "postgres"),
        password=env["PG_PASSWORD"],
    )


def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                id SERIAL PRIMARY KEY,
                log_time TEXT,
                event TEXT NOT NULL,
                username TEXT,
                ip TEXT NOT NULL,
                country TEXT
            )
        """)
    conn.commit()


def insert_attempts(conn, rows):
    """rows : liste de tuples (log_time, event, username, ip, country)."""
    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO attempts (log_time, event, username, ip, country) "
            "VALUES (%s, %s, %s, %s, %s)",
            rows,
        )
    conn.commit()


if __name__ == "__main__":
    conn = get_connection()
    create_table(conn)
    print("Table attempts créée")
    conn.close()