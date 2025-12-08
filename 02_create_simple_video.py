"""
Script 2: Crea un Video Semplice
ATTENZIONE: Questo script CONSUMA CREDITI!
- Video di ~30 secondi = 0.5-1 credito (dipende dal tipo di avatar)
"""

import requests
import time
from config import BASE_URL, get_headers

# =============================================================================
# CONFIGURAZIONE - MODIFICA QUESTI VALORI
# =============================================================================

# Avatar: Abigail (Upper Body) - espressiva
AVATAR_ID = "Abigail_expressive_2024112501"

# Voce: Giovanni Rossi (italiano, maschile)
VOICE_ID = "7b6722df52c44a79b6adb6c3074588d8"

# Il testo che l'avatar dira' (max 5000 caratteri)
# Tieni il testo corto per risparmiare crediti!
SCRIPT_TEXT = """
Ciao! Questo è il mio primo video creato con le API di HeyGen.
È incredibile come sia facile creare video con avatar e intelligenza artificiale.
Grazie per aver guardato!
"""

# Colore sfondo (hex)
BACKGROUND_COLOR = "#1a1a2e"  # Blu scuro

# =============================================================================

def create_video():
    """Crea un video con l'API HeyGen"""

    print("="*50)
    print("CREAZIONE VIDEO")
    print("="*50)

    # Verifica configurazione
    if AVATAR_ID == "YOUR_AVATAR_ID" or VOICE_ID == "YOUR_VOICE_ID":
        print("\nERRORE: Devi configurare AVATAR_ID e VOICE_ID!")
        print("Esegui prima 01_list_avatars_voices.py per ottenere gli ID.")
        return None

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
                    "input_text": SCRIPT_TEXT.strip(),
                    "voice_id": VOICE_ID
                },
                "background": {
                    "type": "color",
                    "value": BACKGROUND_COLOR
                }
            }
        ],
        "dimension": {
            "width": 1280,
            "height": 720
        },
        "title": "Il mio primo video HeyGen"
    }

    print(f"\nAvatar: {AVATAR_ID}")
    print(f"Voce: {VOICE_ID}")
    print(f"Lunghezza script: {len(SCRIPT_TEXT)} caratteri")
    print(f"Risoluzione: 1280x720 (720p)")

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
        print(f"\nVideo creato con successo!")
        print(f"Video ID: {video_id}")
        return video_id
    else:
        print(f"\nErrore nella risposta: {data}")
        return None


def check_video_status(video_id):
    """Controlla lo stato del video e attende il completamento"""

    print("\n" + "="*50)
    print("ATTESA COMPLETAMENTO VIDEO")
    print("="*50)

    max_attempts = 60  # Max 5 minuti (60 * 5 sec)
    attempt = 0

    while attempt < max_attempts:
        response = requests.get(
            f"{BASE_URL}/v1/video_status.get",
            headers=get_headers(),
            params={"video_id": video_id}
        )

        if response.status_code != 200:
            print(f"\nErrore nel controllo stato: {response.status_code}")
            print(response.text)
            return None

        data = response.json()
        status = data.get("data", {}).get("status")

        print(f"  [{attempt+1}] Stato: {status}")

        if status == "completed":
            video_url = data.get("data", {}).get("video_url")
            thumbnail_url = data.get("data", {}).get("thumbnail_url")
            duration = data.get("data", {}).get("duration")

            print("\n" + "="*50)
            print("VIDEO COMPLETATO!")
            print("="*50)
            print(f"\nDurata: {duration} secondi")
            print(f"\nURL Video (scade in 7 giorni):")
            print(video_url)
            print(f"\nURL Thumbnail:")
            print(thumbnail_url)

            return {
                "video_url": video_url,
                "thumbnail_url": thumbnail_url,
                "duration": duration
            }

        elif status == "failed":
            error = data.get("data", {}).get("error")
            print(f"\nVideo FALLITO!")
            print(f"Errore: {error}")
            return None

        # Attendi 5 secondi prima del prossimo controllo
        time.sleep(5)
        attempt += 1

    print("\nTimeout: il video sta impiegando troppo tempo.")
    return None


def download_video(video_url, filename="my_first_video.mp4"):
    """Scarica il video"""

    print(f"\nDownload video in corso...")

    response = requests.get(video_url, stream=True)

    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Video salvato come: {filename}")
        return True
    else:
        print(f"Errore download: {response.status_code}")
        return False


if __name__ == "__main__":
    print("="*50)
    print("HeyGen API - Creazione Video Semplice")
    print("="*50)
    print("\nATTENZIONE: Questo script CONSUMA CREDITI!")

    # Conferma
    confirm = input("\nVuoi procedere? (s/n): ").lower()
    if confirm != 's':
        print("Operazione annullata.")
        exit()

    # Crea il video
    video_id = create_video()

    if video_id:
        # Attendi completamento
        result = check_video_status(video_id)

        if result:
            # Chiedi se scaricare
            download = input("\nVuoi scaricare il video? (s/n): ").lower()
            if download == 's':
                download_video(result["video_url"])

    print("\n" + "="*50)
    print("FINE")
    print("="*50)
