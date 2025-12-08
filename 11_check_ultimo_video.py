"""
Controlla stato ultimo video
"""

import requests
from config import BASE_URL, get_headers

# Prendi ultimo video
r = requests.get(
    f"{BASE_URL}/v1/video.list",
    headers=get_headers(),
    params={"limit": 1}
)

if r.status_code == 200:
    videos = r.json().get('data', {}).get('videos', [])
    if videos:
        v = videos[0]
        video_id = v.get('video_id')
        print(f"Ultimo video: {video_id}")
        print(f"Stato: {v.get('status')}")

        # Dettagli
        r2 = requests.get(
            f"{BASE_URL}/v1/video_status.get",
            headers=get_headers(),
            params={"video_id": video_id}
        )
        if r2.status_code == 200:
            data = r2.json().get('data', {})
            print(f"Errore: {data.get('error')}")
            if data.get('video_url'):
                print(f"URL: {data.get('video_url')}")
