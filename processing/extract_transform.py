import re

FAILED_PATTERN = re.compile(
    r'Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>\S+)'
)
INVALID_PATTERN = re.compile(
    r'Invalid user (?P<user>\S*)\s+from (?P<ip>\S+)'
)
ACCEPTED_PATTERN = re.compile(
    r'Accepted password for (?P<user>\S+) from (?P<ip>\S+)'
)


def extract(row: str):
    """Retourne un dictionnaire pour une ligne utile, sinon None."""
    for event_type, pattern in (
        ("failed", FAILED_PATTERN),
        ("invalid_user", INVALID_PATTERN),
        ("accepted", ACCEPTED_PATTERN),
    ):
        match = pattern.search(row)
        if match:
            return {
                "event": event_type,
                "user": match.group("user") or "(vide)",
                "ip": match.group("ip"),
                "time": row[:15],  # ex : "May 24 00:28:00"
            }
    return None


if __name__ == "__main__":
    samples = [
        "May 24 00:28:00 ns sshd[1351222]: Failed password for invalid user test from 45.156.87.204 port 41740 ssh2",
        "May 24 00:27:57 ns sshd[1351222]: Invalid user test from 45.156.87.204 port 41740",
        "May 19 08:49:50 ns sshd[1257866]: Accepted password for adminesisa from 10.10.33.81 port 59176 ssh2",
        "May 24 00:04:36 ns sshd[1350968]: Connection closed by 127.0.0.1 port 40940 [preauth]",
    ]
    for line in samples:
        print(extract(line))