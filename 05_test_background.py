"""
Test: Verifica upload immagine e struttura background
NON consuma crediti - solo upload e validazione
"""

import requests
import os
import json
from config import BASE_URL, get_headers

# =============================================================================
# TEST 1: Verifica che l'upload funzioni
# =============================================================================

def test_upload(filepath):
    """Testa l'upload di un'immagine e mostra la risposta completa"""

    if not os.path.exists(filepath):
        print(f"File non trovato: {filepath}")
        return None

    # Content type
    if filepath.lower().endswith('.png'):
        content_type = 'image/png'
    else:
        content_type = 'image/jpeg'

    headers = {
        'X-Api-Key': get_headers()['X-Api-Key'],
        'Content-Type': content_type,
        'Accept': 'application/json'
    }

    with open(filepath, 'rb') as f:
        file_data = f.read()

    print(f"Uploading {filepath} ({len(file_data)} bytes)...")
    print(f"Content-Type: {content_type}")

    r = requests.post(
        'https://upload.heygen.com/v1/asset',
        headers=headers,
        data=file_data
    )

    print(f"\nStatus code: {r.status_code}")
    print(f"\nRisposta completa:")
    print(json.dumps(r.json(), indent=2))

    if r.status_code == 200:
        data = r.json().get('data', {})
        return {
            'id': data.get('id'),
            'url': data.get('url'),
            'image_key': data.get('image_key')
        }
    return None

# =============================================================================
# TEST 2: Mostra come appare il payload per la creazione video
# =============================================================================

def show_video_payload_comparison(asset_data):
    """Mostra le due opzioni per il background"""

    print("\n" + "="*60)
    print("OPZIONE 1: Usando 'url'")
    print("="*60)
    payload_url = {
        "background": {
            "type": "image",
            "url": asset_data.get('url')
        }
    }
    print(json.dumps(payload_url, indent=2))

    print("\n" + "="*60)
    print("OPZIONE 2: Usando 'image_asset_id' (RACCOMANDATO)")
    print("="*60)
    payload_id = {
        "background": {
            "type": "image",
            "image_asset_id": asset_data.get('id')
        }
    }
    print(json.dumps(payload_id, indent=2))

# =============================================================================
# TEST 3: Verifica validazione API (senza creare video)
# =============================================================================

def test_validation_only(asset_id):
    """
    Tenta di creare un video con parametri minimi per vedere se l'API
    accetta la struttura del background
    """

    # Questo payload e' volutamente incompleto per testare solo la validazione
    payload = {
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": "test_invalid",  # ID invalido per forzare errore
                    "avatar_style": "normal"
                },
                "voice": {
                    "type": "text",
                    "input_text": "Test",
                    "voice_id": "test_invalid"
                },
                "background": {
                    "type": "image",
                    "image_asset_id": asset_id  # Usiamo image_asset_id
                }
            }
        ],
        "dimension": {
            "width": 1280,
            "height": 720
        }
    }

    print("\n" + "="*60)
    print("TEST VALIDAZIONE (con avatar/voice invalidi)")
    print("="*60)
    print("Payload inviato:")
    print(json.dumps(payload, indent=2))

    r = requests.post(
        f"{BASE_URL}/v2/video/generate",
        headers=get_headers(),
        json=payload
    )

    print(f"\nStatus code: {r.status_code}")
    print(f"Risposta:")
    print(json.dumps(r.json(), indent=2))

    # Se l'errore e' sull'avatar/voice, significa che il background e' OK
    response = r.json()
    error = response.get('error', '') or response.get('message', '')

    if 'avatar' in error.lower() or 'voice' in error.lower():
        print("\n>>> IL BACKGROUND E' STATO ACCETTATO!")
        print(">>> L'errore e' solo sull'avatar/voice invalido")
    elif 'background' in error.lower() or 'image' in error.lower():
        print("\n>>> ERRORE NEL BACKGROUND!")
        print(">>> Verifica la struttura")

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("="*60)
    print("TEST BACKGROUND IMMAGINE - SENZA CONSUMARE CREDITI")
    print("="*60)

    # Cerca un'immagine di test
    test_images = []

    # Cerca in foto_casa_vacanze
    if os.path.exists("foto_casa_vacanze"):
        for f in os.listdir("foto_casa_vacanze"):
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                test_images.append(os.path.join("foto_casa_vacanze", f))
                break

    # Cerca nella directory corrente
    for f in os.listdir("."):
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            test_images.append(f)
            break

    if not test_images:
        print("\nNessuna immagine trovata per il test!")
        print("Metti un file .jpg o .png nella cartella del progetto")
        exit()

    test_image = test_images[0]
    print(f"\nUsero' per il test: {test_image}")

    # Test 1: Upload
    print("\n" + "="*60)
    print("TEST 1: UPLOAD IMMAGINE")
    print("="*60)
    asset_data = test_upload(test_image)

    if asset_data:
        # Test 2: Mostra opzioni payload
        show_video_payload_comparison(asset_data)

        # Test 3: Validazione
        if asset_data.get('id'):
            test_validation_only(asset_data['id'])

        print("\n" + "="*60)
        print("RIEPILOGO")
        print("="*60)
        print(f"Asset ID: {asset_data.get('id')}")
        print(f"Asset URL: {asset_data.get('url')}")
        print(f"Image Key: {asset_data.get('image_key')}")
        print("\nPer usare questo sfondo nel video:")
        print('  "background": {')
        print('    "type": "image",')
        print(f'    "image_asset_id": "{asset_data.get("id")}"')
        print('  }')
