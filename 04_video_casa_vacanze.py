"""
Script 4: Video Presentazione Casa Vacanze
Carica foto e crea video con avatar che descrive gli ambienti
"""

import requests
import time
import os
from config import BASE_URL, get_headers

# =============================================================================
# CONFIGURAZIONE
# =============================================================================

# Avatar femminile business (supporta sfondi personalizzati)
AVATAR_ID = "Adriana_Business_Front_public"

# Voce italiana femminile naturale
VOICE_ID = "750533f27c5649979110086898518280"  # Gabriella - Natural

# Cartella con le foto (usa _fixed per foto ottimizzate)
FOTO_FOLDER = "foto_casa_vacanze_fixed"

# Nome della casa vacanze
NOME_CASA = "Roma Caput Mundi Apartment"

# Definizione delle scene con i testi
# La chiave deve corrispondere al nome del file (senza numero e estensione)
SCENE_CONFIG = {
    "soggiorno": {
        "ordine": 1,
        "testo": f"Ciao! Sono Francesca e vi do il benvenuto al {NOME_CASA}. Questo luminoso bilocale nel cuore della Balduina è a soli 200 metri dalla stazione Appiano, a due fermate da San Pietro. Il soggiorno è dotato di un comodo divano letto, perfetto per un ospite in più."
    },
    "cucina": {
        "ordine": 2,
        "testo": "L'angolo cottura è completamente attrezzato con lavastoviglie, frigorifero e tutto il necessario per preparare i vostri pasti. Pratico e funzionale, proprio come a casa vostra!"
    },
    "pranzo": {
        "ordine": 3,
        "testo": "La zona pranzo è luminosa e accogliente, perfetta per gustare una colazione o una cena in tranquillità. L'appartamento dispone anche di Wi-Fi veloce, aria condizionata, Netflix e Sky inclusi."
    },
    "camera": {
        "ordine": 4,
        "testo": "Ecco la camera matrimoniale, silenziosa e con affaccio sul verde. Potrete svegliarvi ogni mattina con una vista rilassante sulla natura. Le lenzuola sono in cotone di alta qualità per garantirvi il massimo comfort."
    },
    "bagno": {
        "ordine": 5,
        "testo": "Il bagno moderno è dotato di una doccia grande e spaziosa, con bidet e tutti i comfort. Troverete asciugamani di qualità e tutto il necessario per il vostro soggiorno."
    },
    "balcone": {
        "ordine": 6,
        "testo": "Infine, il balcone privato con vista sul giardino. Il posto perfetto per una colazione all'aperto o un aperitivo al tramonto. Potete prenotare su Airbnb, Booking, oppure sul nostro sito web. Per qualsiasi domanda contattateci sui social. Vi aspetto a Roma!"
    }
}

# =============================================================================
# FUNZIONI
# =============================================================================

def find_photos():
    """Trova le foto nella cartella e le ordina"""
    photos = []

    if not os.path.exists(FOTO_FOLDER):
        print(f"ERRORE: Cartella '{FOTO_FOLDER}' non trovata!")
        return []

    for filename in os.listdir(FOTO_FOLDER):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Estrai il nome dell'ambiente dal filename (es: "01_ingresso.jpg" -> "ingresso")
            name_without_ext = os.path.splitext(filename)[0]
            parts = name_without_ext.split('_', 1)

            if len(parts) == 2:
                ambiente = parts[1].lower()
            else:
                ambiente = name_without_ext.lower()

            photos.append({
                "filename": filename,
                "filepath": os.path.join(FOTO_FOLDER, filename),
                "ambiente": ambiente
            })

    # Ordina per filename
    photos.sort(key=lambda x: x["filename"])
    return photos


def upload_photo(filepath):
    """Carica una foto su HeyGen e ritorna l'asset_id"""

    # Determina il content type
    if filepath.lower().endswith('.png'):
        content_type = 'image/png'
    else:
        content_type = 'image/jpeg'

    # Headers - il file va inviato come RAW BINARY DATA
    headers = {
        "X-Api-Key": get_headers()["X-Api-Key"],
        "Content-Type": content_type,
        "Accept": "application/json"
    }

    # Leggi il file come binary e invialo nel body
    with open(filepath, 'rb') as f:
        file_data = f.read()

    response = requests.post(
        "https://upload.heygen.com/v1/asset",
        headers=headers,
        data=file_data
    )

    if response.status_code == 200:
        data = response.json()
        asset_id = data.get("data", {}).get("id")
        return {"asset_id": asset_id}
    else:
        print(f"  Errore upload: {response.status_code}")
        print(f"  {response.text[:300]}")
        return None


def create_video(scenes_data):
    """Crea il video con le scene"""

    video_inputs = []

    for scene in scenes_data:
        video_input = {
            "character": {
                "type": "avatar",
                "avatar_id": AVATAR_ID,
                "avatar_style": "normal"
            },
            "voice": {
                "type": "text",
                "input_text": scene["testo"],
                "voice_id": VOICE_ID
            },
            "background": {
                "type": "image",
                "image_asset_id": scene["asset_id"]
            }
        }
        video_inputs.append(video_input)

    payload = {
        "video_inputs": video_inputs,
        "dimension": {
            "width": 1280,
            "height": 720
        },
        "title": f"Presentazione {NOME_CASA}"
    }

    print(f"\nCreazione video con {len(video_inputs)} scene...")

    response = requests.post(
        f"{BASE_URL}/v2/video/generate",
        headers=get_headers(),
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        return data.get("data", {}).get("video_id")
    else:
        print(f"Errore: {response.status_code}")
        print(response.text)
        return None


def wait_for_video(video_id):
    """Attende il completamento del video"""

    print("\nAttendo completamento video...")
    print("(Questo può richiedere alcuni minuti per video con più scene)")

    for attempt in range(120):  # Max 10 minuti
        response = requests.get(
            f"{BASE_URL}/v1/video_status.get",
            headers=get_headers(),
            params={"video_id": video_id}
        )

        data = response.json()
        status = data.get("data", {}).get("status")

        print(f"  [{attempt+1}] Stato: {status}")

        if status == "completed":
            result = data["data"]
            print("\n" + "="*50)
            print("VIDEO COMPLETATO!")
            print("="*50)
            print(f"\nDurata: {result.get('duration')} secondi")
            print(f"\nURL Video:\n{result.get('video_url')}")
            return result

        elif status == "failed":
            print(f"\nErrore: {data['data'].get('error')}")
            return None

        time.sleep(5)

    print("\nTimeout!")
    return None


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("="*50)
    print(f"VIDEO PRESENTAZIONE: {NOME_CASA}")
    print("="*50)

    # 1. Trova le foto
    print("\n[1] Cerco foto nella cartella...")
    photos = find_photos()

    if not photos:
        print(f"\nNessuna foto trovata in '{FOTO_FOLDER}/'")
        print("Aggiungi le foto e riprova.")
        exit()

    print(f"\nTrovate {len(photos)} foto:")
    for p in photos:
        config = SCENE_CONFIG.get(p["ambiente"], {})
        status = "OK" if config else "ATTENZIONE: ambiente non configurato"
        print(f"  - {p['filename']} -> {p['ambiente']} [{status}]")

    # Filtra solo foto con configurazione
    valid_photos = [p for p in photos if p["ambiente"] in SCENE_CONFIG]

    if not valid_photos:
        print("\nNessuna foto corrisponde agli ambienti configurati!")
        print("Ambienti validi:", list(SCENE_CONFIG.keys()))
        exit()

    print(f"\nScene che verranno create: {len(valid_photos)}")

    # Stima crediti
    estimated_duration = len(valid_photos) * 15  # ~15 sec per scena
    estimated_credits = (estimated_duration / 60) * 2  # ~2 crediti/min per avatar
    print(f"Durata stimata: ~{estimated_duration} secondi")
    print(f"Crediti stimati: ~{estimated_credits:.1f}")

    confirm = input("\nProcedere? (s/n): ").lower()
    if confirm != 's':
        print("Annullato.")
        exit()

    # 2. Carica le foto
    print("\n[2] Caricamento foto su HeyGen...")
    scenes_data = []

    for photo in valid_photos:
        print(f"  Caricamento {photo['filename']}...")
        result = upload_photo(photo["filepath"])

        if result and result.get("asset_id"):
            config = SCENE_CONFIG[photo["ambiente"]]
            scenes_data.append({
                "ambiente": photo["ambiente"],
                "asset_id": result["asset_id"],
                "testo": config["testo"],
                "ordine": config["ordine"]
            })
            print(f"    OK! (ID: {result['asset_id'][:8]}...)")
        else:
            print(f"    FALLITO - scena saltata")

    if not scenes_data:
        print("\nNessuna foto caricata con successo!")
        exit()

    # Ordina per ordine configurato
    scenes_data.sort(key=lambda x: x["ordine"])

    print(f"\n{len(scenes_data)} scene pronte:")
    for s in scenes_data:
        print(f"  {s['ordine']}. {s['ambiente']}")

    # 3. Crea il video
    print("\n[3] Creazione video...")
    video_id = create_video(scenes_data)

    if not video_id:
        print("Errore nella creazione del video!")
        exit()

    print(f"Video ID: {video_id}")

    # 4. Attendi completamento
    print("\n[4] Attendo rendering...")
    result = wait_for_video(video_id)

    if result:
        print("\n" + "="*50)
        print("FATTO!")
        print("="*50)
        print("\nIl video della tua casa vacanze è pronto!")
        print("Copia l'URL e aprilo nel browser per scaricarlo.")
