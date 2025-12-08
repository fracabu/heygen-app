"""
Lista ultimi video generati con i loro URL
"""

import requests
from config import BASE_URL, get_headers

def list_videos(limit=20):
    """Recupera lista video"""

    r = requests.get(
        f"{BASE_URL}/v1/video.list",
        headers=get_headers(),
        params={"limit": limit}
    )

    print(f"Status: {r.status_code}")

    if r.status_code == 200:
        data = r.json()
        videos = data.get('data', {}).get('videos', [])

        print(f"\nTrovati {len(videos)} video:\n")
        print("="*80)

        for i, v in enumerate(videos, 1):
            print(f"{i}. {v.get('title', 'Senza titolo')}")
            print(f"   ID: {v.get('video_id')}")
            print(f"   Stato: {v.get('status')}")
            print(f"   Durata: {v.get('duration', 'N/A')} sec")

            if v.get('video_url'):
                print(f"   URL: {v.get('video_url')}")
            elif v.get('status') == 'completed':
                # Prova a recuperare URL
                url = get_video_url(v.get('video_id'))
                if url:
                    print(f"   URL: {url}")

            print()

        return videos
    else:
        print(f"Errore: {r.text}")
        return []

def get_video_url(video_id):
    """Recupera URL di un video specifico"""
    r = requests.get(
        f"{BASE_URL}/v1/video_status.get",
        headers=get_headers(),
        params={"video_id": video_id}
    )

    if r.status_code == 200:
        return r.json().get('data', {}).get('video_url')
    return None

if __name__ == "__main__":
    print("="*80)
    print("ULTIMI VIDEO GENERATI")
    print("="*80)
    list_videos(limit=10)
