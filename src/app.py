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
        #print(iteration, text)
        subprocess.run(["python", "synthesize_text.py", "--text", str(text) + str(iteration)])

def create_video():
    subprocess.run(["python", "create_video.py"])

def generate_video(topic):
    #generate_narrative_and_presentation(topic)
    #synthesize_audio(topic)
    create_video()


import streamlit as st

st.title('Video Generator')

topic = st.text_input('Enter the topic', '')

if st.button('Generate Video'):
    generate_video(topic)
    video_file = '../data/output.mp4'
    video_bytes = open(video_file, 'rb').read()
    st.video(video_bytes)