import requests

def get_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"

    response = requests.get(url)
    data = response.json()

    if coin_id not in data:
        return None

    return data[coin_id]["usd"]