"""
Script 4 EN: Video Presentazione Casa Vacanze - ENGLISH VERSION
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

# Voce inglese femminile - da trovare
# Per ora usiamo una voce inglese comune, puoi cambiarla dopo
VOICE_ID = "1bd001e7e50f421d891986aad5158bc8"  # Sara - English US

# Cartella con le foto (stessa del video italiano)
FOTO_FOLDER = "foto_casa_vacanze"

# Nome della casa vacanze
NOME_CASA = "Roma Caput Mundi Apartment"

# Definizione delle scene con i testi IN INGLESE
SCENE_CONFIG = {
    "soggiorno": {
        "ordine": 1,
        "testo": f"Hello! Welcome to {NOME_CASA}. This bright one-bedroom apartment in the heart of Balduina is just 200 meters from Appiano station, two stops from Saint Peter's. The living room features a comfortable sofa bed, perfect for an extra guest."
    },
    "cucina": {
        "ordine": 2,
        "testo": "The kitchenette is fully equipped with a dishwasher, refrigerator, and everything you need to prepare your meals. Practical and functional, just like home!"
    },
    "pranzo": {
        "ordine": 3,
        "testo": "The dining area is bright and welcoming, perfect for enjoying breakfast or dinner in peace. The apartment also features fast Wi-Fi, air conditioning, Netflix and Sky included."
    },
    "camera": {
        "ordine": 4,
        "testo": "Here's the master bedroom, quiet with a view of the greenery. You can wake up every morning with a relaxing view of nature. The sheets are high-quality cotton to ensure maximum comfort."
    },
    "bagno": {
        "ordine": 5,
        "testo": "The modern bathroom has a large and spacious shower, with bidet and all amenities. You'll find quality towels and everything you need for your stay."
    },
    "balcone": {
        "ordine": 6,
        "testo": "Finally, the private balcony with garden view. The perfect spot for breakfast outdoors or a sunset aperitivo. You can book on Airbnb, Booking, or on our website. For any questions contact us on social media. See you in Rome!"
    }
}

# =============================================================================
# FUNZIONI (identiche alla versione italiana)
# =============================================================================

def find_photos():
    """Trova le foto nella cartella e le ordina"""
    photos = []

    if not os.path.exists(FOTO_FOLDER):
        print(f"ERROR: Folder '{FOTO_FOLDER}' not found!")
        return []

    for filename in os.listdir(FOTO_FOLDER):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
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

    photos.sort(key=lambda x: x["filename"])
    return photos


def upload_photo(filepath):
    """Carica una foto su HeyGen e ritorna l'asset_id"""

    if filepath.lower().endswith('.png'):
        content_type = 'image/png'
    else:
        content_type = 'image/jpeg'

    headers = {
        "X-Api-Key": get_headers()["X-Api-Key"],
        "Content-Type": content_type,
        "Accept": "application/json"
    }

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
        print(f"  Upload error: {response.status_code}")
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
        "title": f"Presentation {NOME_CASA} (EN)"
    }

    print(f"\nCreating video with {len(video_inputs)} scenes...")

    response = requests.post(
        f"{BASE_URL}/v2/video/generate",
        headers=get_headers(),
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        return data.get("data", {}).get("video_id")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def wait_for_video(video_id):
    """Attende il completamento del video"""

    print("\nWaiting for video to complete...")
    print("(This may take several minutes for multi-scene videos)")

    for attempt in range(120):
        response = requests.get(
            f"{BASE_URL}/v1/video_status.get",
            headers=get_headers(),
            params={"video_id": video_id}
        )

        data = response.json()
        status = data.get("data", {}).get("status")

        print(f"  [{attempt+1}] Status: {status}")

        if status == "completed":
            result = data["data"]
            print("\n" + "="*50)
            print("VIDEO COMPLETED!")
            print("="*50)
            print(f"\nDuration: {result.get('duration')} seconds")
            print(f"\nVideo URL:\n{result.get('video_url')}")
            return result

        elif status == "failed":
            print(f"\nError: {data['data'].get('error')}")
            return None

        time.sleep(5)

    print("\nTimeout!")
    return None


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("="*50)
    print(f"VIDEO PRESENTATION: {NOME_CASA} (ENGLISH)")
    print("="*50)

    # 1. Trova le foto
    print("\n[1] Looking for photos...")
    photos = find_photos()

    if not photos:
        print(f"\nNo photos found in '{FOTO_FOLDER}/'")
        print("Add photos and try again.")
        exit()

    print(f"\nFound {len(photos)} photos:")
    for p in photos:
        config = SCENE_CONFIG.get(p["ambiente"], {})
        status = "OK" if config else "WARNING: room not configured"
        print(f"  - {p['filename']} -> {p['ambiente']} [{status}]")

    valid_photos = [p for p in photos if p["ambiente"] in SCENE_CONFIG]

    if not valid_photos:
        print("\nNo photos match configured rooms!")
        print("Valid rooms:", list(SCENE_CONFIG.keys()))
        exit()

    print(f"\nScenes to create: {len(valid_photos)}")

    estimated_duration = len(valid_photos) * 15
    estimated_credits = (estimated_duration / 60) * 2
    print(f"Estimated duration: ~{estimated_duration} seconds")
    print(f"Estimated credits: ~{estimated_credits:.1f}")

    confirm = input("\nProceed? (y/n): ").lower()
    if confirm != 'y':
        print("Cancelled.")
        exit()

    # 2. Carica le foto
    print("\n[2] Uploading photos to HeyGen...")
    scenes_data = []

    for photo in valid_photos:
        print(f"  Uploading {photo['filename']}...")
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
            print(f"    FAILED - scene skipped")

    if not scenes_data:
        print("\nNo photos uploaded successfully!")
        exit()

    scenes_data.sort(key=lambda x: x["ordine"])

    print(f"\n{len(scenes_data)} scenes ready:")
    for s in scenes_data:
        print(f"  {s['ordine']}. {s['ambiente']}")

    # 3. Crea il video
    print("\n[3] Creating video...")
    video_id = create_video(scenes_data)

    if not video_id:
        print("Error creating video!")
        exit()

    print(f"Video ID: {video_id}")

    # 4. Attendi completamento
    print("\n[4] Waiting for rendering...")
    result = wait_for_video(video_id)

    if result:
        print("\n" + "="*50)
        print("DONE!")
        print("="*50)
        print("\nYour vacation rental video is ready!")
        print("Copy the URL and open it in browser to download.")
