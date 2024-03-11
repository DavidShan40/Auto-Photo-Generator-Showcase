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
import re
from ast import literal_eval
import pandas as pd

def extract_first_list_object(input_string):
    # Regex pattern to match list objects
    # This pattern matches anything that starts with '[' and ends with ']', capturing nested lists as well
    pattern = r'\[.*?\]'
    
    # Search for the pattern in the input string
    match = re.search(pattern, input_string)
    
    # If a match is found, return the match, otherwise return None
    return literal_eval(match.group(0)) if match else None

def get_image_description(image_prompt):
    # get details from the input image, This helps me regenerate the same image later by prompt
    system_message_content = """
    1. Your user will input a prompt that describes the picture
    2. write a short description of the picture, around 10-20 words, ignore starting words like "The picture shows"
    3. Show 2 best categories that suitable for this picture, must from the list. If no words in the list fits then say "None" [
    "Abstract",
    "Animals/Wildlife",
    "Arts",
    "Backgrounds/Textures",
    "Beauty/Fashion",
    "Buildings/Landmarks",
    "Business/Finance",
    "Celebrities",
    "Education",
    "Food and Drink",
    "Healthcare/Medical",
    "Holidays",
    "Industrial",
    "Interiors",
    "Miscellaneous",
    "Nature",
    "Objects",
    "Parks/Outdoor",
    "People",
    "Religion",
    "Science",
    "Signs/Symbols",
    "Sports/Recreation",
    "Technology",
    "Transportation",
    "Vintage",
    "None"
] Reference information category_definitions = {
    "Abstract": "Content with fractals, blurs, patterns, textures, or abstract concepts.",
    "Animals/Wildlife": "Content with domestic and wild animals.",
    "Arts": "Content related to art-making objects, people making art, or artwork.",
    "Backgrounds/Textures": "Content appearing as wallpaper/backgrounds, including landscapes, textures, patterns.",
    "Beauty/Fashion": "Content related to beauty products, fashion, hairstyles, clothing, and fashion models.",
    "Buildings/Landmarks": "Content with architectural structures or the built environment.",
    "Business/Finance": "Content related to businesspeople, workplaces, financial districts, and money-related items.",
    "Celebrities": "Content with celebrities, celebrity-related places, or editorial content including celebrity names.",
    "Education": "Content featuring school scenes, graduations, or education-related items.",
    "Food and Drink": "Content depicting food and/or food-related topics.",
    "Healthcare/Medical": "Content related to health, wellness, medicine, medical subjects, and healthy eating.",
    "Holidays": "Content related to international calendar events, seasons, life events, travel, and vacations.",
    "Industrial": "Content related to construction, mining, electricity, trades, tools, and building materials.",
    "Interiors": "Content featuring interiors of buildings, houses, and religious structures.",
    "Miscellaneous": "Can be used for any subject matter.",
    "Nature": "Content featuring environmental-related subjects like plants, animals, clouds, and bodies of water.",
    "Objects": "Content with any object(s) as the main focus.",
    "Parks/Outdoor": "Content related to parks, outdoor activities, and national parks.",
    "People": "Content with a person, group of people, or body parts.",
    "Religion": "Content related to religious or spiritual topics.",
    "Science": "Content related to scientific or medical fields, including technology and natural sciences.",
    "Signs/Symbols": "Content featuring signs, symbols, flags, icons, logos, and gesturing people.",
    "Sports/Recreation": "Content related to sports, fitness, and hobbies on land, air, or water.",
    "Technology": "Content related to computers, phones, appliances, tech concepts like AI and VR.",
    "Transportation": "Content related to modes of transportation and related infrastructure.",
    "Vintage": "Content with a vintage look-and-feel, including retro, kitsch, and sepia tone scenes."
}

4. write 30 key words base on the picture's prompt. The key words should not have any spelling error.

Your output should only show a python list: [ short description in step 2, keywords in step 4(separate by commas) ,  categories in step 3(separate by commas)] , anything else should not show    
    """
    
    # User message directly prompts AI to analyze and describe the provided image
    user_message_content = image_prompt

    response = client.chat.completions.create(model="gpt-4-vision-preview",
    messages=[{"role": "system", "content": system_message_content},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_message_content},
            ],
        }
    ],
    max_tokens=300)
    return response.choices[0].message.content
cover_dir = "new_images_prompt"
today_date = datetime.now().strftime("%Y-%m-%d")
folder_path = os.path.join(cover_dir, today_date)
txt_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]


df_columns = ["Filename","Description","Keywords","Categories"]
df_lists = []
for file_path in txt_files:
    with open(file_path, 'r') as file:
        # Read the content of the file
        content = file.read()
        result_list = extract_first_list_object(get_image_description(str(content)))
        k = 0
        while result_list == None:
            result_list = extract_first_list_object(get_image_description(str(content)))
            k+=1
            if k >= 5:
                print("warning, the description is not executable")
        file_name = os.path.basename(file_path)
        name, ext = os.path.splitext(file_name)
        modified_file_name = f"{name}.jpeg"
        result_list = [modified_file_name] + result_list
        df_lists.append(result_list)
df = pd.DataFrame(df_lists, columns=df_columns)

cover_dir = "Shutterstocks_metadata"
today_date = datetime.now().strftime("%Y-%m-%d")
new_folder_path = os.path.join(cover_dir, today_date)
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)
cover_dir = new_folder_path
csv_filename = os.path.join(cover_dir, "metadata.csv")
df.to_csv(csv_filename, index=False)
print(df.head())