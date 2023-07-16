import os
import glob
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_audioclips

# Path to your files
pdf_file = '../data/presentation.pdf'
audio_folder = '../data/audio_files'  # Folder containing your audio files

# Convert PDF to list of images
pdf = PdfReader(pdf_file)
num_pages = len(pdf.pages)
images = convert_from_path(pdf_file, dpi=200)

# Save images to disk
image_files = []
for i in range(num_pages):
    image_path = f'slide_{i}.png'
    images[i].save(image_path, 'PNG')
    image_files.append(image_path)

# Get audio files from folder, sorted by name
audio_files = sorted(list(glob.iglob('../**/*.mp3', recursive=True)))

# Get durations from audio files and concatenate audio
durations = []
audio_clips = []
for audio_file in audio_files:
    audio = AudioFileClip(audio_file)
    durations.append(audio.duration)
    audio_clips.append(audio)

concatenated_audio = concatenate_audioclips(audio_clips)

# Create video from images and audio
clip = ImageSequenceClip(image_files, durations=durations)
clip = clip.set_audio(concatenated_audio)
clip.write_videofile('../data/output.mp4', fps=1)

# Clean up image files
for image_file in image_files:
    os.remove(image_file)
