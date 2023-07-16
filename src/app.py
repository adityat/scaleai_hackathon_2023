import streamlit as st
import subprocess

def generate_narrative_and_presentation(topic):
    subprocess.run(["python", "base.py", topic])

def synthesize_audio(topic):
    file_path = f"../data/narrative_{topic}.txt"
    with open(file_path, 'r') as file:
        data = file.read()
        dict_data = eval(data)
     
    text_list = []
    for txt in dict_data.values():
        text_list.append(txt)

    for iteration, text in dict_data.items():
        subprocess.run(["python", "synthesize_text.py", "--text", str(text) + str(iteration)])

def create_video():
    subprocess.run(["python", "create_video.py"])

def generate_video(topic):
    generate_narrative_and_presentation(topic)
    synthesize_audio(topic)
    create_video()

st.title('AutoTutor')

topic = st.text_input('Enter the topic', '')

if st.button('Generate Video'):
    # Create a placeholder for the status message
    status_message = st.empty()
    status_message.text('Processing...')
    generate_video(topic)
    video_file = '../data/output.mp4'
    video_bytes = open(video_file, 'rb').read()
    st.video(video_bytes)
    status_message.text('Done!')