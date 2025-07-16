import json
import pandas as pd
from pathlib import Path
from datetime import datetime

def parse_json_to_csv():
    base_path = Path(__file__).resolve().parent.parent
    input_dir = base_path / "data" / "Raw" / "Spot_Price"
    output_dir = base_path / "docs" / "data"
    
    # Find latest file by date in filename spot_price_YYYY-MM-DD.json
    json_files = list(input_dir.glob("spot_price_*.json"))
    if not json_files:
        raise FileNotFoundError(f"No spot_price JSON files found in {input_dir}")
    
    # Sort by date extracted from filename descending, pick latest
    latest_file = sorted(json_files, key=lambda f: f.stem.split("_")[-1], reverse=True)[0]

    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    values = data["france_power_exchanges"][0]["values"]

    rows = []
    for v in values:
        start_dt = datetime.fromisoformat(v["start_date"])
        end_dt = datetime.fromisoformat(v["end_date"])
        hour_range = f"{start_dt.hour:02d}-{end_dt.hour:02d}"
        price_eur_per_mwh = v["price"]
        price_eur_per_kwh = round(price_eur_per_mwh / 1000, 3)  # Convert €/MWh to €/kWh
        load_mw = v["value"]

        rows.append({
            "start_date": v["start_date"],
            "end_date": v["end_date"],
            "hour_range": hour_range,
            "price_eur_per_mwh": price_eur_per_mwh,
            "price_eur_per_kwh": price_eur_per_kwh,
            "load_mw": load_mw,
        })

    df = pd.DataFrame(rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"spot_price_{latest_file.stem.split('_')[-1]}.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved CSV to {output_path.resolve()}")

if __name__ == "__main__":
    parse_json_to_csv()
