"""
Mostra dettagli dei video incluso avatar usato
"""

import requests
from config import BASE_URL, get_headers

def get_video_details(video_id):
    """Recupera dettagli completi di un video"""
    r = requests.get(
        f"{BASE_URL}/v1/video_status.get",
        headers=get_headers(),
        params={"video_id": video_id}
    )
    if r.status_code == 200:
        return r.json().get('data', {})
    return {}

def list_videos_with_details():
    """Lista video con avatar usato"""

    r = requests.get(
        f"{BASE_URL}/v1/video.list",
        headers=get_headers(),
        params={"limit": 20}
    )

    if r.status_code != 200:
        print(f"Errore: {r.status_code}")
        return

    videos = r.json().get('data', {}).get('videos', [])

    print(f"Ultimi {len(videos)} video:\n")
    print("="*70)

    for i, v in enumerate(videos, 1):
        video_id = v.get('video_id')
        title = v.get('title', 'Senza titolo')
        status = v.get('status')

        # Recupera dettagli
        details = get_video_details(video_id)

        print(f"{i}. {title}")
        print(f"   ID: {video_id}")
        print(f"   Stato: {status}")

        # Cerca info avatar nei dettagli
        if details:
            # Il campo potrebbe variare
            avatar_id = details.get('avatar_id')
            if not avatar_id:
                # Prova altri campi
                video_inputs = details.get('video_inputs', [])
                if video_inputs and len(video_inputs) > 0:
                    char = video_inputs[0].get('character', {})
                    avatar_id = char.get('avatar_id')

            if avatar_id:
                print(f"   AVATAR: {avatar_id}")

            # URL video
            url = details.get('video_url')
            if url:
                print(f"   URL: {url[:80]}...")

        print()

if __name__ == "__main__":
    print("="*70)
    print("DETTAGLI VIDEO - CERCA AVATAR USATO")
    print("="*70)
    list_videos_with_details()
