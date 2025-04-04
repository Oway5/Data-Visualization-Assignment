import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

INPUT_FILE = "carpark_data.json"
OUTPUT_DIR = "visualizations"
OUTPUT_FILE_SCATTER = os.path.join(OUTPUT_DIR, "availability_vs_total_lots_scatter.png")

def preprocess_data(data):
    if not data or 'items' not in data or not data['items']:
        print("No items found in the data.")
        return pd.DataFrame()

    carpark_entries = data['items'][0]['carpark_data']
    processed_list = []
    for entry in carpark_entries:
        carpark_number = entry['carpark_number']
        update_time = entry['update_datetime']
        for info in entry['carpark_info']:
            try:
                total_lots = int(info['total_lots'])
                lots_available = int(info['lots_available'])
                lot_type = info['lot_type']
                if total_lots > 0:
                    availability_pct = (lots_available / total_lots) * 100
                else:
                    availability_pct = 0

                processed_list.append({
                    'carpark_number': carpark_number,
                    'lot_type': lot_type,
                    'total_lots': total_lots,
                    'lots_available': lots_available,
                    'availability_pct': availability_pct,
                    'update_datetime': update_time
                })
            except (ValueError, KeyError) as e:
                print(f"Skipping entry due to error: {e} in carpark {carpark_number}")
                continue

    return pd.DataFrame(processed_list)

def plot_availability_vs_total_lots(df, output_path):
    df_cars = df[df['lot_type'] == 'C'].copy()
    if df_cars.empty:
        print("No car lot data found for scatter plot.")
        return

    df_cars['total_lots'] = pd.to_numeric(df_cars['total_lots'], errors='coerce')
    df_cars['availability_pct'] = pd.to_numeric(df_cars['availability_pct'], errors='coerce')
    df_cars.dropna(subset=['total_lots', 'availability_pct'], inplace=True)

    if df_cars.empty:
        print("No valid numeric data for car lots scatter plot.")
        return

    plt.figure(figsize=(12, 7))
    sns.scatterplot(data=df_cars, x='total_lots', y='availability_pct', alpha=0.6, s=50) # s adjusts point size
    plt.title('Carpark Availability Percentage vs. Total Lots (Lot Type C)')
    plt.xlabel('Total Car Lots')
    plt.ylabel('Availability Percentage (%)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.ylim(0, 105) # Percentage range with a bit of padding
    plt.xlim(left=0)
    plt.savefig(output_path)
    plt.close()
    print(f"Saved scatter plot to {output_path}")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    try:
        with open(INPUT_FILE, 'r') as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_FILE}' not found.")
        exit()
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{INPUT_FILE}'.")
        exit()
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        exit()

    carpark_df = preprocess_data(raw_data)

    if not carpark_df.empty:
        plot_availability_vs_total_lots(carpark_df, OUTPUT_FILE_SCATTER)
    else:
        print("Processed DataFrame is empty, skipping plot generation.")

    print("Scatter plot visualization script finished.") 