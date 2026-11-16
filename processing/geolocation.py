import json
import urllib.request


def geo_location(ip: str):
    """Retourne le code pays (ex : 'FR') d'une IP, ou None si inconnu."""
    url = f"https://ipinfo.io/{ip}/json"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"Erreur géolocalisation {ip} : {e}")
        return None
    return data.get("country")


if __name__ == "__main__":
    print(geo_location("88.147.152.239"))
    print(geo_location("10.10.33.81"))