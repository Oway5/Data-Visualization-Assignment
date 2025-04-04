import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

INPUT_FILE = "carpark_data.json"
OUTPUT_DIR = "visualizations"

def preprocess_data(data):
    """Extracts and preprocesses carpark data into a pandas DataFrame."""
    if not data or 'items' not in data or not data['items']:
        print("No items found in the data.")
        return pd.DataFrame() 

    # Assuming the structure always has one item in the 'items' list
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
                continue #if malformed 

    return pd.DataFrame(processed_list)

def plot_availability_distribution(df, output_path):
    """Plots the distribution of availability percentage for car ('C') lots."""
    df_cars = df[df['lot_type'] == 'C'].copy() # Filter for car lots
    if df_cars.empty:
        print("No car lot data found for distribution plot.")
        return

  
    df_cars['availability_pct'] = pd.to_numeric(df_cars['availability_pct'], errors='coerce')
    df_cars.dropna(subset=['availability_pct'], inplace=True)

    if df_cars.empty:
        print("No valid numeric availability data for car lots.")
        return

    plt.figure(figsize=(10, 6))
    sns.histplot(df_cars['availability_pct'], bins=20, kde=True)
    plt.title('Distribution of Carpark Availability Percentage (Lot Type C)')
    plt.xlabel('Availability Percentage (%)')
    plt.ylabel('Number of Carparks')
    plt.grid(axis='y', alpha=0.5)
    plt.savefig(output_path)
    plt.close()
    print(f"Saved availability distribution plot to {output_path}")

def plot_availability_by_lot_type(df, output_path):
    """Plots the average availability percentage by lot type."""
    if df.empty or 'availability_pct' not in df.columns or 'lot_type' not in df.columns:
         print("DataFrame is empty or missing required columns for lot type plot.")
         return
    
    # Ensuring availability_pct is numeric
    df['availability_pct'] = pd.to_numeric(df['availability_pct'], errors='coerce')
    avg_availability = df.groupby('lot_type')['availability_pct'].mean().reset_index()

    if avg_availability.empty:
        print("No data to plot after grouping by lot type.")
        return

    plt.figure(figsize=(10, 6))
    sns.barplot(x='lot_type', y='availability_pct', data=avg_availability, palette='viridis')
    plt.title('Average Carpark Availability Percentage by Lot Type')
    plt.xlabel('Lot Type')
    plt.ylabel('Average Availability Percentage (%)')
    plt.ylim(0, 100) 
    plt.grid(axis='y', alpha=0.5)
    plt.savefig(output_path)
    plt.close()
    print(f"Saved average availability by lot type plot to {output_path}")


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    dist_plot_path = os.path.join(OUTPUT_DIR, "availability_distribution.png")
    type_plot_path = os.path.join(OUTPUT_DIR, "availability_by_type.png")

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
        plot_availability_distribution(carpark_df, dist_plot_path)
        plot_availability_by_lot_type(carpark_df, type_plot_path)
    else:
        print("Processed DataFrame is empty, skipping plot generation.")

    print("Visualization script finished.") 