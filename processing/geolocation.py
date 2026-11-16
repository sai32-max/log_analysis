import json
import logging
import urllib.request
from storage.db import load_env

logger = logging.getLogger(__name__)


def geo_location(ip: str):
    """Retourne le code pays (ex : 'FR') d'une IP, ou None si inconnu."""
    token = load_env().get("IPINFO_TOKEN", "")
    url = f"https://ipinfo.io/{ip}/json"
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        logger.error("Erreur géolocalisation %s : %s", ip, e)
        return None
    return data.get("country")


if __name__ == "__main__":
    print(geo_location("88.147.152.239"))
    print(geo_location("10.10.33.81"))