
import os
import moviepy.editor as mp
import spacy
import requests
import pyttsx3
import tkinter as tk
from tkinter import messagebox

nlp = spacy.load("en_core_web_sm")
engine = pyttsx3.init()

def generate_audio(text, output_file):
    engine.setProperty('rate', 120)  # Adjust the rate to your preference (120 words per minute)
    engine.save_to_file(text, output_file)
    engine.runAndWait()

def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]
    return keywords

def search_and_download_image(keyword, output_folder, unsplash_api_key):
    base_url = f'https://api.unsplash.com/photos/random?query={keyword}'
    headers = {'Authorization': f'Client-ID {unsplash_api_key}'}

    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        image_url = data['urls']['regular']
        output_file = os.path.join(output_folder, f"img{search_and_download_image.counter}.jpg")  # Use counter to generate filename
        search_and_download_image.counter += 1

        os.makedirs(output_folder, exist_ok=True)

        img_data = requests.get(image_url).content
        with open(output_file, 'wb') as f:
            f.write(img_data)

        print(f"Downloaded image for {keyword}: {output_file}")
        return output_file
    else:
        print(f"Failed to fetch image for {keyword}")

# Initialize counter attribute
search_and_download_image.counter = 1

def generate_video():
    output_folder = 'generated_files'
    os.makedirs(output_folder, exist_ok=True)  # Create the output folder

    # Read text from file
    with open('selected_text.txt', 'r') as file:
        input_text = file.read().strip()

    audio_file = os.path.join(output_folder, "output_audio.mp3")
    generate_audio(input_text, audio_file)

    keywords = extract_keywords(input_text)
    print("Extracted Keywords:", keywords)

    image_folder = os.path.join(output_folder, 'downloaded_images')
    os.makedirs(image_folder, exist_ok=True)  # Create the image folder

    unsplash_api_key = 'whcjZPPsoanBxXIc3nWcafrTBTeq7-kK1XRb0vamNig'  # Your Unsplash API key

    # Create a list to store image file paths
    image_files = []

    for keyword in keywords:
        image_files.append(search_and_download_image(keyword, image_folder, unsplash_api_key))

    audio_duration = mp.AudioFileClip(audio_file).duration
    num_images = len(keywords)

    # Calculate the duration of each image clip
    image_duration = audio_duration / num_images

    clips = []

    # Sort image files based on their names
    sorted_image_files = sorted(image_files)

    for img_path in sorted_image_files:
        clip = mp.ImageClip(img_path).set_duration(image_duration)
        clips.append(clip)

    final_clip = mp.concatenate_videoclips(clips, method="compose")
    final_clip = final_clip.set_audio(mp.AudioFileClip(audio_file).subclip(0, audio_duration))

    final_output_file = os.path.join(output_folder, "final_video.mp4")
    final_clip.write_videofile(final_output_file, codec='libx264', fps=24)

    # Display an alert after video generation
    show_alert(final_output_file)

def show_alert(video_file):
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    root.update()  # Update the display

    result = messagebox.askquestion("Video Generated", "The video was successfully generated. Do you want to open it?")

    if result == 'yes':
        os.system(f'start {video_file}')  # Open the video file using the default program

    root.mainloop()

if __name__ == "__main__":
    generate_video()
