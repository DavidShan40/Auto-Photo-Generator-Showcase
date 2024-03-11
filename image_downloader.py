from datetime import datetime
import requests
import os

k=0
def download_images_pixabay(query, api_key, folder='images', num_images=50):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    params = {
        'key': api_key,
        'q': query,
        'order': 'latest', #popular
        'image_type': 'photo',
        'per_page': num_images,
    }
    
    response = requests.get('https://pixabay.com/api/', params=params)
    data = response.json()
    for i, image in enumerate(data['hits'], start=1):
        image_url = image['largeImageURL']
        try:
            img_data = requests.get(image_url).content
            file_path = os.path.join(folder, f'{k}.jpg')
            k+=1
            #file_path = os.path.join(folder, f'{query}_{i}.jpg')
            with open(file_path, 'wb') as f:
                f.write(img_data)
            print(f"Downloaded {file_path}")
        except Exception as e:
            print(f"Failed to download {image_url}: {e}")

# Example usage
api_key = os.getenv("Pixabay_API_KEY")  # Replace with your Pixabay API key

queries = [
    "Best Selling Photography Trends 2024",
    "Top Selling Stock Photos",
    "Most Popular Photography Genres",
    "High Demand Photography Subjects",
    "Best Selling Fine Art Photography",
    "Most Downloaded Images Shutterstock",
    "Trending Photography on Instagram",
    "Photography Market Analysis",
    "Best Selling Nature Photography",
    "Top Photography Categories in Demand"
]
cover_dir = "old_images"
today_date = datetime.now().strftime("%Y-%m-%d")
new_folder_path = os.path.join(cover_dir, today_date)
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)
cover_dir = new_folder_path
for query in queries:
    download_images_pixabay(query, api_key, cover_dir, 5)

# future try Unsplash and Pexels 