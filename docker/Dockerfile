FROM nvcr.io/nvidia/pytorch:22.08-py3

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_ROOT_USER_ACTION=ignore
ENV FORCE_CUDA=1

RUN apt-get update && apt install -y ffmpeg curl 
RUN pip install --upgrade pip
RUN pip install streamlit Pillow==9.3.0 torch torchvision torchaudio
RUN pip install "git+https://github.com/facebookresearch/pytorch3d.git"

WORKDIR /app

RUN pip install "mmcv-full>=1.3.17,<=1.5.3" -f https://download.openmmlab.com/mmcv/dist/cu117/torch1.13.1+cu117/index.html 
RUN git clone https://github.com/open-mmlab/mmhuman3d.git 

RUN pip install -r /app/mmhuman3d/requirements/runtime.txt

RUN sed -i "s/SyncBN/BN/g" /app/mmhuman3d/configs/hmr/resnet50_hmr_pw3d.py

RUN pip install vedo --no-dependencies 
RUN pip install mmdet mmpose mmcls mmtrack     
RUN pip install -v -e /app/mmhuman3d/ 
RUN pip uninstall -y opencv-contrib-python opencv-contrib-python-headless opencv-python
RUN pip install opencv-contrib-python==4.5.5.62


RUN mkdir -p /app/mmhuman3d/data \
    /app/mmhuman3d/data/body_models \
    /app/mmhuman3d/data/body_models/smpl \
    /app/mmhuman3d/data/checkpoints \
    /app/mmhuman3d/input \
    /app/mmhuman3d/output \
    /app/mmhuman3d/vis_results 

RUN wget -O /app/mmhuman3d/data/checkpoints/resnet50_hmr_pw3d.pth https://openmmlab-share.oss-cn-hangzhou.aliyuncs.com/mmhuman3d/models/hmr/resnet50_hmr_pw3d-04f40f58_20211201.pth?versionId=CAEQHhiBgMD6zJfR6xciIDE0ODQ3OGM2OWJjMTRlNmQ5Y2ZjMWZhMzRkOTFiZDFm  
    
COPY basicModel_f_lbs_10_207_0_v1.0.0.pkl /app/mmhuman3d/data/body_models/smpl/SMPL_FEMALE.pkl 
COPY basicmodel_m_lbs_10_207_0_v1.0.0.pkl /app/mmhuman3d/data/body_models/smpl/SMPL_MALE.pkl 
COPY basicModel_neutral_lbs_10_207_0_v1.0.0.pkl /app/mmhuman3d/data/body_models/smpl/SMPL_NEUTRAL.pkl
COPY smpl_mean_params.npz /app/mmhuman3d/data/body_models/
COPY J_regressor_extra.npy /app/mmhuman3d/data/body_models/
COPY J_regressor_h36m.npy /app/mmhuman3d/data/body_models/
ADD main.py /app/mmhuman3d/


RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app/mmhuman3d

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]


