"""
Utility: Controlla crediti HeyGen
"""
import requests
from config import BASE_URL, get_headers

def check_credits():
    r = requests.get(f'{BASE_URL}/v2/user/remaining_quota', headers=get_headers())
    data = r.json()['data']
    print(f"Crediti API rimanenti: {data['remaining_quota']}")
    return data['remaining_quota']

if __name__ == "__main__":
    check_credits()
