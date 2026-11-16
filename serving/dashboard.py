import matplotlib.pyplot as plt
from storage.db import get_connection


def run_query(conn, sql):
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def bar_chart(labels, values, title, subtitle, ylabel, filename):
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, values, color="#6B7B2A")
    ax.set_title(title, loc="left", fontsize=14, fontweight="bold", pad=28)
    ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=9, color="gray")
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.3)
    ax.bar_label(bars, padding=3)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)
    print(f"Graphique enregistré : {filename}")


def main():
    conn = get_connection()

    pays = run_query(conn, """
        SELECT COALESCE(country, 'Inconnu') AS pays, COUNT(*) AS nb
        FROM attempts
        WHERE event = 'failed'
        GROUP BY pays
        ORDER BY nb DESC
        LIMIT 10
    """)
    bar_chart(
        [p[0] for p in pays], [p[1] for p in pays],
        title="Tentatives échouées par pays",
        subtitle="Top 10 — source : logs auth.log",
        ylabel="Nombre de tentatives échouées",
        filename="serving/tentatives_par_pays.png",
    )

    users = run_query(conn, """
        SELECT username, COUNT(*) AS nb
        FROM attempts
        WHERE event = 'accepted'
        GROUP BY username
        ORDER BY nb DESC
    """)
    bar_chart(
        [u[0] for u in users], [u[1] for u in users],
        title="Connexions réussies par utilisateur",
        subtitle="Source : logs auth.log",
        ylabel="Nombre de connexions réussies",
        filename="serving/reussites_par_user.png",
    )

    invalid = run_query(conn, """
        SELECT COALESCE(NULLIF(username, ''), '(vide)') AS identifiant, COUNT(*) AS nb
        FROM attempts
        WHERE event = 'invalid_user'
        GROUP BY identifiant
        ORDER BY nb DESC
        LIMIT 10
    """)
    bar_chart(
        [i[0] for i in invalid], [i[1] for i in invalid],
        title="Tentatives avec « invalid user »",
        subtitle="Top 10 des identifiants essayés",
        ylabel="Nombre de tentatives",
        filename="serving/invalid_user.png",
    )

    conn.close()


if __name__ == "__main__":
    main()