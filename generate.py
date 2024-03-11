# https://gptpluginz.com/how-to-use-dall-e-3-api-and-gpt-4-vision/

from datetime import datetime
from openai import OpenAI
import base64
import requests
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
import time
load_dotenv()  # This loads the contents of the .env file into the environment

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_description(base64_image):
    # get details from the input image, This helps me regenerate the same image later by prompt
    system_message_content = """
    Generate a comprehensive and nuanced description of an image that includes artistic elements such as style, color scheme, composition, and mood. The description should be detailed enough to allow for the recreation of the image based on textual information alone. Use specific artistic vocabulary and ensure the inclusion of comparative imagery or analogies to enhance clarity and depth.
    """
    
    # User message directly prompts AI to analyze and describe the provided image
    user_message_content = "Provide a detailed description of the provided image, focusing on its artistic style, color scheme, composition, mood, notable features, and any unique details. Use precise artistic terms and include comparisons or analogies to convey the image’s essence."

    response = client.chat.completions.create(model="gpt-4-vision-preview",
    messages=[{"role": "system", "content": system_message_content},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_message_content},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
            ],
        }
    ],
    max_tokens=300)
    return response.choices[0].message.content

def generate_image(prompt):
    modified_prompt = prompt + " The picture should looks like a real photo not AI generated art"
    response = client.images.generate(model="dall-e-3",
    prompt=modified_prompt,
    size="1024x1024",
    quality="standard",
    n=1)
    return response.data[0].url

def save_image_from_url(url, original_filename, cover_dir):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    #webp_filepath = os.path.join(cover_dir, os.path.splitext(original_filename)[0] + '.webp')
    webp_filepath = os.path.join(cover_dir, os.path.splitext(original_filename)[0] + '.jpeg')
    #image.convert("RGB").save(webp_filepath, 'WEBP')
    image.convert("RGB").save(webp_filepath, 'JPEG')

# Main function to tie everything together
def main(image_path, cover_dir, cover_dir_prompt):
    # Step 1: Encode image to base64
    base64_image = encode_image(image_path)

    # Step 2: Get image description
    description = get_image_description(base64_image)
    print(f"Image Description: {description}")

    # Step 3: Generate a new image based on the prompt
    generated_image_url = generate_image(description)
    #print(f"Generated Image URL: {generated_image_url}")
    original_filename = os.path.basename(image_path)
    file_path = os.path.join(cover_dir_prompt, os.path.splitext(original_filename)[0] + '.txt')
    with open(file_path, 'w') as file:
    # Write the string to the file
        file.write(description)

    # Step 4: Save the generated image
    original_filename = os.path.basename(image_path)
    save_image_from_url(generated_image_url, original_filename, cover_dir)
    #print(f"Image saved successfully in {cover_dir}")

# Directories
image_dir = "old_images"
cover_dir = "new_images"
cover_dir_prompt = "new_images_prompt"
today_date = datetime.now().strftime("%Y-%m-%d")
image_dir = os.path.join(image_dir, today_date)
new_folder_path = os.path.join(cover_dir, today_date)
new_folder_prompt_path = os.path.join(cover_dir_prompt, today_date)
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)
if not os.path.exists(new_folder_prompt_path):
    os.makedirs(new_folder_prompt_path)
cover_dir = new_folder_path
cover_dir_prompt = new_folder_prompt_path
photo_num = 1 # between 0 and 500
if __name__ == "__main__":
    # Example usage
    all_files = os.listdir(image_dir)
    image_extensions = ['.jpeg', '.jpg', '.png', '.webp', '.tiff', '.bmp', '.gif']  # List of image file extensions
    image_paths = [os.path.join(image_dir, file) for file in all_files if os.path.splitext(file)[1].lower() in image_extensions]
    #print(image_paths)
    for image_path in image_paths[0:photo_num]:
        start_time = time.time()
        max_retries = 5  # Set a maximum number of retries
        for attempt in range(max_retries):
            try:
                # Try to process the image
                main(image_path, cover_dir, cover_dir_prompt)
                #print(f"Processed {image_path} successfully.")
                break  # Break out of the retry loop if successful
            except Exception as e:
                # Handle the exception if needed
                print(f"An error occurred: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying {image_path} (Attempt {attempt + 2}/{max_retries})...")
                else:
                    print(f"Failed to process {image_path} after {max_retries} attempts.")
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")