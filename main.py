import subprocess

# download sample images
subprocess.run(['python', 'image_downloader.py'])
# generate images
subprocess.run(['python', 'generate.py'])
# upscale images
subprocess.run(['python', 'upscaler.py'])
# save shutterstocks csvs
subprocess.run(['python', 'shutterstocks_csvs.py'])
