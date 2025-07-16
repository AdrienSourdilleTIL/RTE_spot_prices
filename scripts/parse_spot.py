import json
import pandas as pd
from datetime import datetime
from pathlib import Path

def parse_json_to_csv():
    today_str = datetime.today().strftime("%Y-%m-%d")
    base_path = Path(__file__).resolve().parent.parent
    input_path = base_path / "data" / "Raw" / "Spot_Price" / f"spot_price_{today_str}.json"
    output_dir = base_path / "docs" / "data"
    output_path = output_dir / f"spot_price_{today_str}.csv"

    if not input_path.exists():
        raise FileNotFoundError(f"No file found for today: {input_path}")

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    values = data["france_power_exchanges"][0]["values"]
    rows = [
        {
            "start_date": v["start_date"],
            "end_date": v["end_date"],
            "price_eur_per_mwh": v["price"],
            "load_mw": v["value"]
        }
        for v in values
    ]

    df = pd.DataFrame(rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved CSV to {output_path.resolve()}")

if __name__ == "__main__":
    parse_json_to_csv()
