import requests

API_KEY = "iBE63z4DmaRF4Oh4IFyL7kBrFhj8SxmB"   # jouw API key
TAG = "§DIP§7"

url = f"https://api.voxyl.net/guild/info/{TAG}?api={API_KEY}"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    guild_data = response.json()
    print("Guild data:")
    print(guild_data)

except requests.exceptions.RequestException as e:
    print("Request error:", e)
