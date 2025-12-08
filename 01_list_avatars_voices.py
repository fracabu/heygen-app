"""
Script 1: Lista Avatar e Voci disponibili
Questo script NON consuma crediti - e' solo una query di lettura.
"""

import requests
from config import BASE_URL, get_headers

def list_avatars():
    """Ottiene la lista degli avatar disponibili"""
    print("\n" + "="*50)
    print("AVATAR DISPONIBILI")
    print("="*50)

    response = requests.get(
        f"{BASE_URL}/v2/avatars",
        headers=get_headers()
    )

    if response.status_code != 200:
        print(f"Errore: {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    avatars = data.get("data", {}).get("avatars", [])

    # Mostra i primi 10 avatar pubblici
    print(f"\nTrovati {len(avatars)} avatar totali.")
    print("\nPrimi 10 avatar:")
    print("-"*50)

    for i, avatar in enumerate(avatars[:10]):
        print(f"{i+1}. ID: {avatar.get('avatar_id')}")
        print(f"   Nome: {avatar.get('avatar_name', 'N/A')}")
        print(f"   Tipo: {avatar.get('avatar_type', 'N/A')}")
        print()

    return avatars

def list_voices():
    """Ottiene la lista delle voci disponibili"""
    print("\n" + "="*50)
    print("VOCI DISPONIBILI")
    print("="*50)

    response = requests.get(
        f"{BASE_URL}/v2/voices",
        headers=get_headers()
    )

    if response.status_code != 200:
        print(f"Errore: {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    voices = data.get("data", {}).get("voices", [])

    # Filtra voci italiane
    italian_voices = [v for v in voices if v.get("language", "").lower() == "italian"]

    print(f"\nTrovate {len(voices)} voci totali.")
    print(f"Voci italiane: {len(italian_voices)}")

    print("\nVoci italiane disponibili:")
    print("-"*50)
    for i, voice in enumerate(italian_voices[:5]):
        print(f"{i+1}. ID: {voice.get('voice_id')}")
        print(f"   Nome: {voice.get('name', 'N/A')}")
        print(f"   Genere: {voice.get('gender', 'N/A')}")
        print()

    # Mostra anche alcune voci inglesi come alternativa
    english_voices = [v for v in voices if v.get("language", "").lower() == "english"]
    print("\nAlcune voci inglesi:")
    print("-"*50)
    for i, voice in enumerate(english_voices[:5]):
        print(f"{i+1}. ID: {voice.get('voice_id')}")
        print(f"   Nome: {voice.get('name', 'N/A')}")
        print(f"   Genere: {voice.get('gender', 'N/A')}")
        print()

    return voices

def check_quota():
    """Controlla i crediti rimanenti"""
    print("\n" + "="*50)
    print("QUOTA CREDITI")
    print("="*50)

    response = requests.get(
        f"{BASE_URL}/v2/user/remaining_quota",
        headers=get_headers()
    )

    if response.status_code != 200:
        print(f"Errore: {response.status_code}")
        print(response.text)
        return

    data = response.json()
    print(f"\nCrediti rimanenti: {data}")

if __name__ == "__main__":
    print("="*50)
    print("HeyGen API - Esplorazione Risorse")
    print("="*50)
    print("\nQuesto script NON consuma crediti!")

    # Controlla quota
    check_quota()

    # Lista avatar
    avatars = list_avatars()

    # Lista voci
    voices = list_voices()

    print("\n" + "="*50)
    print("PROSSIMI PASSI")
    print("="*50)
    print("""
1. Copia un avatar_id che ti piace
2. Copia un voice_id (preferibilmente italiano)
3. Esegui 02_create_simple_video.py con questi ID
    """)
