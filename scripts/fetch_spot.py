import os
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from pathlib import Path
import json

load_dotenv()

TOKEN_URL = "https://digital.iservices.rte-france.com/token/oauth/"
API_URL = "https://digital.iservices.rte-france.com/open_api/wholesale_market/v2/france_power_exchanges"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("SECRET_ID")

def get_rte_token():
    response = requests.post(
        TOKEN_URL,
        data={'grant_type': 'client_credentials'},
        auth=(CLIENT_ID, CLIENT_SECRET)
    )
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Token request failed with status {response.status_code}")

def fetch_latest_power_exchange_data(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    now = datetime.now(timezone.utc)
    yesterday = now - timedelta(days=1)

    params = {
        "start_date": yesterday.replace(hour=0, minute=0, second=0, microsecond=0).isoformat(),
        "end_date": now.replace(hour=23, minute=59, second=59, microsecond=0).isoformat(),
    }

    response = requests.get(API_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    try:
        token = get_rte_token()
        data = fetch_latest_power_exchange_data(token)
        
        base_path = Path(__file__).resolve().parent.parent
        output_dir = base_path / "data" / "Raw" / "Spot_Price"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        date_str = (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%d")
        output_file = output_dir / f"spot_price_{date_str}.json"

        print(f"[DEBUG] Writing data to: {output_file.resolve()}")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Data saved to {output_file.resolve()}")

    except Exception as e:
        print(f"Error: {e}")
