import subprocess

def generate_narrative_and_presentation(topic):
    subprocess.run(["python", "base.py", topic])

def synthesize_audio(topic):
    subprocess.run(["python", "synthesize_file.py", "--text", f"../data/narrative_{topic}.txt"])

def create_video():
    subprocess.run(["python", "create_video.py"])

def generate_video(topic):
    generate_narrative_and_presentation(topic)
    synthesize_audio(topic)
    create_video()


import streamlit as st

st.title('Video Generator')

topic = st.text_input('Enter the topic', '')

if st.button('Generate Video'):
    generate_video(topic)
    video_file = 'output.mp4'
    video_bytes = open(video_file, 'rb').read()
    st.video(video_bytes)