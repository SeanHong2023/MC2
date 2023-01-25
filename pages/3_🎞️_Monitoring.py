import streamlit as st
import cv2
from pytube import YouTube
import shutil
from scripts.tflite_lib import *
import io
import subprocess

# func to save BytesIO on a drive
def write_bytesio_to_file(bytesio, filename):
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytesio.getbuffer())

def get_video_info(video_path):
    # so now we can process it with OpenCV functions
    cap = cv2.VideoCapture(video_path)

    # grab some parameters of video to use them for writing a new, processed video
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)  ##<< No need for an int
    n_frames = cap.get(7)
    return cap, w, h, fps, n_frames


def detect_video(model, video_info, save_path):
    cap, w, h, fps, n_frames = video_info 
    # specify a writer to write a processed video to a disk frame by frame
    fourcc_mp4 = cv2.VideoWriter_fourcc(*'mp4v')
    out_mp4 = cv2.VideoWriter(save_path, fourcc_mp4, fps, (w, h))
   
    p = st.progress(0)
    i = 0 
    while True:
        ret, frame = cap.read()
        if not ret: break
        if i%int(fps)==0: #1초마다
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            detections = model.detect(frame)
            frame = visualize(frame, detections)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) 
        frame = visualize(frame, detections)
        out_mp4.write(frame)
        i+=1
        p.progress(int((i/n_frames)*100))
        
    
    out_mp4.release()
    cap.release()


def main(tmp_save, tmp_save_cvt, tmp_result, tmp_result_cvt):
    
    st.sidebar.markdown("#")
    model_path = 'models/effdet_v5.tflite'
    model = load_model(model_path)
    
    mk = '''
    # 이상 행동 판별 데모  
    # 
    ##### 인공지능을 이용해 구토 등 이상증상을 판별합니다.
    ---

    '''
    st.markdown(mk)
    
    video_data = st.file_uploader("Upload file", ['mp4','mov', 'avi', 'webm'])
    if video_data:
        write_bytesio_to_file(video_data, tmp_save)
        # subprocess.run(["ffmpeg", "-y", "-i", tmp_save, "-c:v", "libx264", tmp_save_cvt])
        # subprocess.call(args=f"ffmpeg -y -i {tmp_save} -c:v libx264 {tmp_save_cvt}".split(" "), shell=True)
        subprocess.call(f"ffmpeg -y -i {tmp_save} -c:v libx264 {tmp_save_cvt}", shell=True)
        video_info = get_video_info(tmp_save_cvt)
        st.write(video_info[1:])
    
        if st.button('분석 시작'):
            detect_video( model, video_info, tmp_result)
            subprocess.call(args=f"ffmpeg -y -i {tmp_result} -c:v libx264 {tmp_result_cvt}".split(" "), shell=True)
            st.video(tmp_result_cvt)


if __name__ == '__main__':
    tmp_save = './tmp-videos/tmp_1.mp4'
    tmp_save_cvt = './tmp-videos/tmp_2.mp4'
    tmp_result  = './tmp-videos/tmp_3.mp4'
    tmp_result_cvt  = './tmp-videos/tmp_4.mp4'
    main(tmp_save, tmp_save_cvt, tmp_result, tmp_result_cvt)

