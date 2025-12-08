"""
Script 3: Video con Scene Multiple
ATTENZIONE: Questo script CONSUMA PIU' CREDITI!
- Ogni scena aggiunge durata = piu' crediti
"""

import requests
import time
from config import BASE_URL, get_headers

# =============================================================================
# CONFIGURAZIONE
# =============================================================================

AVATAR_ID = "YOUR_AVATAR_ID"
VOICE_ID = "YOUR_VOICE_ID"

# Definisci le scene del tuo video
# Ogni scena puo' avere testo e sfondo diverso
SCENES = [
    {
        "text": "Benvenuto! Oggi ti mostrero' come creare video con scene multiple.",
        "background_color": "#1a1a2e"  # Blu scuro
    },
    {
        "text": "Ogni scena puo' avere uno sfondo diverso, come questo verde.",
        "background_color": "#16a085"  # Verde
    },
    {
        "text": "E questo e' il finale! Grazie per aver guardato.",
        "background_color": "#8e44ad"  # Viola
    }
]

# =============================================================================

def create_multi_scene_video():
    """Crea un video con scene multiple"""

    print("="*50)
    print("CREAZIONE VIDEO MULTI-SCENA")
    print("="*50)

    if AVATAR_ID == "YOUR_AVATAR_ID" or VOICE_ID == "YOUR_VOICE_ID":
        print("\nERRORE: Configura AVATAR_ID e VOICE_ID!")
        return None

    # Costruisci video_inputs da SCENES
    video_inputs = []
    for i, scene in enumerate(SCENES):
        video_input = {
            "character": {
                "type": "avatar",
                "avatar_id": AVATAR_ID,
                "avatar_style": "normal"
            },
            "voice": {
                "type": "text",
                "input_text": scene["text"],
                "voice_id": VOICE_ID
            },
            "background": {
                "type": "color",
                "value": scene["background_color"]
            }
        }
        video_inputs.append(video_input)
        print(f"Scena {i+1}: {len(scene['text'])} caratteri, sfondo {scene['background_color']}")

    payload = {
        "video_inputs": video_inputs,
        "dimension": {
            "width": 1280,
            "height": 720
        },
        "title": "Video Multi-Scena"
    }

    print(f"\nTotale scene: {len(video_inputs)}")
    print("\nInvio richiesta...")

    response = requests.post(
        f"{BASE_URL}/v2/video/generate",
        headers=get_headers(),
        json=payload
    )

    if response.status_code != 200:
        print(f"\nErrore: {response.status_code}")
        print(response.text)
        return None

    data = response.json()
    video_id = data.get("data", {}).get("video_id")

    if video_id:
        print(f"\nVideo ID: {video_id}")
        return video_id

    print(f"\nErrore: {data}")
    return None


def wait_for_video(video_id):
    """Attende il completamento del video"""

    print("\nAttendo completamento...")

    for attempt in range(60):
        response = requests.get(
            f"{BASE_URL}/v1/video_status.get",
            headers=get_headers(),
            params={"video_id": video_id}
        )

        data = response.json()
        status = data.get("data", {}).get("status")
        print(f"  [{attempt+1}] {status}")

        if status == "completed":
            video_url = data["data"]["video_url"]
            print(f"\nVideo completato!")
            print(f"URL: {video_url}")
            return video_url

        elif status == "failed":
            print(f"\nFallito: {data['data'].get('error')}")
            return None

        time.sleep(5)

    print("\nTimeout!")
    return None


if __name__ == "__main__":
    print("HeyGen - Video Multi-Scena")
    print("="*50)
    print(f"\nQuesto video avra' {len(SCENES)} scene.")
    print("Stima crediti: ~1-2 crediti (dipende dalla durata)")

    confirm = input("\nProcedere? (s/n): ").lower()
    if confirm != 's':
        print("Annullato.")
        exit()

    video_id = create_multi_scene_video()
    if video_id:
        wait_for_video(video_id)
