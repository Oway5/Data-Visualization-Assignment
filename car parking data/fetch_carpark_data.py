import requests
import json

BASE_URL = "https://api.data.gov.sg/v1"
ENDPOINT = "/transport/carpark-availability"
API_URL = f"{BASE_URL}{ENDPOINT}"
OUTPUT_FILE = "carpark_data.json"

def fetch_latest_carpark_data():
    """
    Fetches the latest carpark availability data from the API and saves it to a file.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status() #exception for bad status codes (4xx or 5xx)
        data = response.json()
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Successfully retrieved data and saved to {OUTPUT_FILE}")

        # if 'items' in data and data['items']:
        #     first_item = data['items'][0]
        #     print("\n--- Example Carpark Data ---")
        #     print(f"Timestamp: {first_item.get('timestamp')}")
        #     if first_item.get('carpark_data'):
        #          print(f"First Carpark Details: {first_item['carpark_data'][0]}")


    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
    except IOError as e:
        print(f"Error writing to file {OUTPUT_FILE}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    fetch_latest_carpark_data() 