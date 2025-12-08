"""
Test: Video singola scena con sfondo immagine
~4 secondi = ~0.1 crediti
"""

import requests
import time
import os
from config import BASE_URL, get_headers

# Configurazione
AVATAR_ID = "Adriana_Business_Front_public"  # Donna business senza sfondo fisso
VOICE_ID = "750533f27c5649979110086898518280"  # Gabriella italiana

# Testo breve (~4 secondi)
TESTO_BREVE = "Ciao! Questo e' un test dello sfondo."

def upload_photo(filepath):
    """Carica foto e ritorna asset_id"""
    content_type = 'image/png' if filepath.lower().endswith('.png') else 'image/jpeg'

    headers = {
        'X-Api-Key': get_headers()['X-Api-Key'],
        'Content-Type': content_type,
    }

    with open(filepath, 'rb') as f:
        data = f.read()

    r = requests.post('https://upload.heygen.com/v1/asset', headers=headers, data=data)

    if r.status_code == 200:
        return r.json().get('data', {}).get('id')
    print(f"Errore upload: {r.status_code} - {r.text[:200]}")
    return None

def create_test_video(asset_id):
    """Crea video di test con sfondo immagine"""

    payload = {
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": AVATAR_ID,
                    "avatar_style": "normal"
                },
                "voice": {
                    "type": "text",
                    "input_text": TESTO_BREVE,
                    "voice_id": VOICE_ID
                },
                "background": {
                    "type": "image",
                    "image_asset_id": asset_id
                }
            }
        ],
        "dimension": {
            "width": 1280,
            "height": 720
        },
        "title": "Test Sfondo Immagine"
    }

    print("\nPayload:")
    print(f"  Avatar: {AVATAR_ID}")
    print(f"  Voice: {VOICE_ID}")
    print(f"  Background: image_asset_id = {asset_id}")
    print(f"  Testo: \"{TESTO_BREVE}\"")

    r = requests.post(f"{BASE_URL}/v2/video/generate", headers=get_headers(), json=payload)

    print(f"\nRisposta API: {r.status_code}")
    print(r.json())

    if r.status_code == 200:
        return r.json().get('data', {}).get('video_id')
    return None

def wait_for_video(video_id):
    """Attende completamento"""
    print("\nAttendo rendering...")

    for i in range(60):
        r = requests.get(
            f"{BASE_URL}/v1/video_status.get",
            headers=get_headers(),
            params={"video_id": video_id}
        )
        data = r.json().get('data', {})
        status = data.get('status')

        print(f"  [{i+1}] {status}")

        if status == 'completed':
            print("\n" + "="*50)
            print("VIDEO COMPLETATO!")
            print("="*50)
            print(f"URL: {data.get('video_url')}")
            return True
        elif status == 'failed':
            print(f"\nERRORE: {data.get('error')}")
            return False

        time.sleep(5)

    print("\nTimeout!")
    return False

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("="*50)
    print("TEST SFONDO IMMAGINE - ~4 secondi")
    print("="*50)

    # Trova prima immagine disponibile
    test_image = None

    if os.path.exists("foto_casa_vacanze"):
        for f in os.listdir("foto_casa_vacanze"):
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                test_image = os.path.join("foto_casa_vacanze", f)
                break

    if not test_image:
        for f in os.listdir("."):
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                test_image = f
                break

    if not test_image:
        print("Nessuna immagine trovata!")
        exit()

    print(f"\nImmagine: {test_image}")

    # 1. Upload
    print("\n[1] Upload immagine...")
    asset_id = upload_photo(test_image)

    if not asset_id:
        print("Upload fallito!")
        exit()

    print(f"    Asset ID: {asset_id}")

    # Conferma
    print(f"\nStima: ~4 sec = ~0.1 crediti")
    confirm = input("Procedere? (s/n): ").lower()
    if confirm != 's':
        print("Annullato.")
        exit()

    # 2. Crea video
    print("\n[2] Creazione video...")
    video_id = create_test_video(asset_id)

    if not video_id:
        print("Creazione fallita!")
        exit()

    print(f"    Video ID: {video_id}")

    # 3. Attendi
    print("\n[3] Rendering...")
    wait_for_video(video_id)
