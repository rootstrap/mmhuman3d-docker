import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import os
import subprocess



def process_video(filepath, video_option):
    video_file = open(filepath, 'rb')
    video_bytes = video_file.read()
    col1.write("Original")
    filename = os.path.basename(filepath)
    result_path = f"vis_results/{filename}"
    bashCommand = []
    if video_option=='multi_person':
        bashCommand = ["python", "demo/estimate_smpl.py", 
        "configs/hmr/resnet50_hmr_pw3d.py", 
        "data/checkpoints/resnet50_hmr_pw3d.pth", 
        "--multi_person_demo", 
        "--tracking_config", "demo/mmtracking_cfg/deepsort_faster-rcnn_fpn_4e_mot17-private-half.py", 
        "--input_path", f"{filepath}", 
        "--show_path", f"{result_path}", 
        "--smooth_type", "savgol"]
    else: 
        bashCommand = ["python", "demo/estimate_smpl.py",
        "configs/hmr/resnet50_hmr_pw3d.py",
        "data/checkpoints/resnet50_hmr_pw3d.pth",
        "--single_person_demo",
        "--det_config", "demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py",
        "--det_checkpoint", "https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r50_fpn_1x_coco/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth",
        "--input_path", f"{filepath}",
        "--show_path" , f"{result_path}",
        "--output", "output/",
        "--smooth_type", "savgol"]

    process = subprocess.run(bashCommand)
    if process.returncode==0:
        col1.video(video_bytes, format="video/mp4", start_time=0)
        col2.write("Result")
        
        video_file_result = open(result_path, 'rb')
        video_bytes_result = video_file_result.read()
        col2.video(video_bytes_result, format="video/mp4", start_time=0)
        with open(result_path, "rb") as file:
            btn = col2.download_button(
                label="Download video",
                data=file,
                file_name=filename,
                mime="video/mp4"
              )
    else:
        st.error('Error: please try again there has been an error.', icon="🚨")
        print(f'Error: Return code:{process.returncode}')


def remove_files(input_path):
    files = os.listdir(input_path)
    for f in files:
        try:
            os.remove(f"{input_path}{f}")
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


INPUT_PATH = "/app/mmhuman3d/input/"
MULTI_PATH = "/app/mmhuman3d/videos/multi_person/"
SINGLE_PATH = "/app/mmhuman3d/videos/single_person/"


st.set_page_config(layout="wide", page_title="Human3d")

st.write("## Find the 3D Human shape in your video!")

st.sidebar.write("## Upload video")

video_options = ('single_person', 'multi_person')
video_option = st.sidebar.selectbox('Choose the type of video:', video_options)

path = MULTI_PATH
if (video_option=='single_person'):
    path = SINGLE_PATH
files = tuple(os.listdir(path))
files = ('None',) + files

option_file = st.sidebar.selectbox(
        'Choose video from the list or upload your own video', files)

col1, col2 = st.columns(2)

uploaded_file = st.sidebar.file_uploader("Upload a video in mp4 format", type=["mp4"])

if st.button('Start'):
    print('press button')
    print(uploaded_file, video_option, option_file)
    if uploaded_file is not None and uploaded_file!='None':
        print('upload file')
        st.write(f'Processing {video_options} file {uploaded_file.name}')
        st.session_state.disabled = True
        remove_files(INPUT_PATH)
        remove_files("/app/mmhuman3d/vis_results/")
        bytes_data = uploaded_file.read()
        with open(os.path.join(INPUT_PATH,uploaded_file.name),"wb") as f:
            f.write(uploaded_file.getbuffer())
        process_video(filepath=f"{INPUT_PATH}{uploaded_file.name}", video_option=video_option)
    elif option_file!='None' and video_option=='single_person':
        print('single_person')
        st.write(f'Process single_person video {option_file}')
        st.session_state.disabled = True
        process_video(filepath=f"{SINGLE_PATH}{option_file}", video_option=video_option)
    elif option_file!='None' and video_option=='multi_person':
        print('multi_person')
        st.write(f'Process multi_person video {option_file}')
        st.session_state.disabled = False
        process_video(filepath=f"{MULTI_PATH}{option_file}", video_option=video_option)
