# Auto Photo Generator Showcase

## Overview
This showcase demonstrates how to use Python to automatically generate beautiful photos by leveraging APIs and advanced image processing techniques.

## How It Works

### Steps Involved:
1. **Image Downloading**:
    - Utilizes the Pixabay API to download images based on specified queries.
    - Images are stored in dated folders, implementing error handling and sequential naming conventions (`image_downloader.py`).

2. **Image Processing with OpenAI**:
    - Integrates OpenAI's API to encode images in base64.
    - Obtains detailed descriptions via GPT-4 Vision.
    - Generates new images using DALL-E 3 based on these descriptions.
    - Manages directories efficiently and handles errors with retries (`generate.py`).

3. **Image Upscaling**:
    - Employs OpenCV to upscale all images within a specified folder to double their original size, based on the current date.
    - Replaces original images with their upscaled versions (`upscaler.py`).

4. **Metadata Extraction and Categorization** (Optional):
    - Automates the extraction and categorization of image descriptions using OpenAI's GPT-4 API.
    - Preprocesses text for analysis.
    - Saves metadata to a CSV file, suitable for over one million image prompts.
    - This functionality is particularly useful for Shutterstock's Metadata system (`shutterstocks_csv.py`).

## Getting Started

### Installation:

#### Step 1: Install Required Libraries
To use the code, you must first install the required libraries by running the following commands in your terminal:

```bash
pip install opencv-python-headless
pip install openai
```

#### Step 2: Set Up Environment Variables
Next, you need to save your OpenAI and Pixabay API keys in environment variables for secure access. Add the following lines to your environment variable configuration file (such as create `.bashrc`, `.zshrc`, or `.env` file in your project directory, or change on your local computer):

export OPENAI_API_KEY="your_openai_key"
export PIXABAY_API_KEY="your_pixabay_key"

Make sure to replace `"your_openai_key"` and `"your_pixabay_key"` with your actual API keys from OpenAI and Pixabay, respectively.

#### Step 3: Run the Application
Finally, execute the `main.py` script to start the application by running the following command in your terminal:

```bash
python main.py
```