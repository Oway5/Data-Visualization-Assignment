import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

INPUT_FILE = "carpark_data.json"
OUTPUT_DIR = "visualizations"
OUTPUT_FILE_PLOT = os.path.join(OUTPUT_DIR, "lot_type_vs_available_scatter.png")

def preprocess_data(data):
    """Extracts and preprocesses carpark data into a pandas DataFrame."""
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

                processed_list.append({
                    'carpark_number': carpark_number,
                    'lot_type': lot_type,
                    'total_lots': total_lots,
                    'lots_available': lots_available,
                    # 'availability_pct': availability_pct, # Removed
                    'update_datetime': update_time
                })
            except (ValueError, KeyError) as e:
                print(f"Skipping entry due to error: {e} in carpark {carpark_number}")
                continue

    return pd.DataFrame(processed_list)

def plot_lot_type_vs_available(df, output_path):
    """Plots lots available vs. lot type using a scatter plot."""
    if df.empty:
        print("No data found for the plot.")
        return

    # Ensure columns are correct type and handle NaNs
    df['lots_available'] = pd.to_numeric(df['lots_available'], errors='coerce')
    df['lot_type'] = df['lot_type'].astype(str) # Ensure lot_type is string
    df.dropna(subset=['lots_available', 'lot_type'], inplace=True)

    if df.empty:
        print("No valid numeric data for the scatter plot.")
        return

    df_sorted = df.sort_values('lot_type')

    plt.figure(figsize=(12, 7))
    sns.scatterplot(data=df_sorted, x='lot_type', y='lots_available', alpha=0.7, s=40)


    plt.title('Available Lots per Carpark by Lot Type')
    plt.xlabel('Lot Type')
    plt.ylabel('Number of Lots Available')
    plt.grid(axis='y', linestyle='--', linewidth=0.5)
    plt.ylim(bottom=-5) # Start y a bit below 0 to see points at 0 clearly


    plt.savefig(output_path)
    plt.close()
    print(f"Saved Lot Type vs Available Lots scatter plot to {output_path}")

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
        plot_lot_type_vs_available(carpark_df, OUTPUT_FILE_PLOT)
    else:
        print("Processed DataFrame is empty, skipping plot generation.")

    print("Lot Type vs Available Lots visualization script finished.") 