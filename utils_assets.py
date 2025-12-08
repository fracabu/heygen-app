"""
Utility: Gestione Asset HeyGen
- Lista asset
- Upload con nome identificabile
- Elimina asset
"""
import requests
import os
from config import BASE_URL, get_headers

def list_assets(file_type=None, limit=20):
    """Lista tutti gli asset"""
    params = {'limit': limit}
    if file_type:
        params['file_type'] = file_type

    r = requests.get(f'{BASE_URL}/v1/asset/list', headers=get_headers(), params=params)
    data = r.json()

    print(f"Totale asset: {data.get('data', {}).get('total', 0)}")
    print("="*60)

    assets = data.get('data', {}).get('assets', [])
    for i, a in enumerate(assets):
        print(f"{i+1}. {a.get('name', 'N/A')}")
        print(f"   Tipo: {a.get('file_type')}")
        print(f"   ID: {a.get('id')}")
        print(f"   URL: {a.get('url')}")
        print()

    return assets

def upload_image(filepath):
    """Carica un'immagine e ritorna ID e URL"""
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

    r = requests.post(
        'https://upload.heygen.com/v1/asset',
        headers=headers,
        data=file_data
    )

    if r.status_code == 200:
        data = r.json().get('data', {})
        asset_id = data.get('id')
        url = data.get('url')
        print(f"  OK! ID: {asset_id}")
        print(f"  URL: {url}")
        return {'id': asset_id, 'url': url}
    else:
        print(f"  Errore: {r.status_code}")
        print(f"  {r.text[:200]}")
        return None

def delete_asset(asset_id):
    """Elimina un asset"""
    r = requests.post(
        f'{BASE_URL}/v1/asset/delete',
        headers=get_headers(),
        json={'asset_id': asset_id}
    )
    print(f"Delete {asset_id}: {r.status_code}")
    return r.status_code == 200

if __name__ == "__main__":
    print("=== ASSET HEYGEN ===\n")
    list_assets(file_type='image', limit=10)
