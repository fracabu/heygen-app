"""
Cerca voci inglesi femminili
"""

import requests
from config import BASE_URL, get_headers

r = requests.get(f"{BASE_URL}/v2/voices", headers=get_headers())

if r.status_code == 200:
    voices = r.json().get('data', {}).get('voices', [])

    print("VOCI INGLESI FEMMINILI:\n")
    print("="*70)

    for v in voices:
        lang = v.get('language', '').lower()
        gender = v.get('gender', '').lower()

        # Solo inglese e femminile
        if 'english' in lang and gender == 'female':
            print(f"ID: {v.get('voice_id')}")
            print(f"Nome: {v.get('name')}")
            print(f"Lingua: {v.get('language')}")
            print()
