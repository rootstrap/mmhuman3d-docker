# mmhuman3d-docker

Docker for mmhuman3d - open-mmlab exposing streamlit a app. 

[mmhuman3d](https://github.com/open-mmlab/mmhuman3d) is an Open Source project PyTorch-based the use of 3D human parametric models, it is a part of the OpenMMLab project.

The container can be downloaded at []() or it can modified editing the file [docker/Dockerfile](docker/Dockerfile). 

**mmhuman3d needs GPU for inference**, so you need to support GPU inside your container. 

## Nvidia Image 
It depends on the image [nvcr.io/nvidia/pytorch:22.08-py3](https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/rel_22-08.html#rel_22-08). You need to create an account at create [NGC](https://ngc.nvidia.com/signin) and [generate an api key](https://ngc.nvidia.com/setup/api-key).  

Login into ngc: 

```bash
	docker login nvcr.io
	Username: $oauthtoken
	password: [insert here your api key]
```

## Running docker container 
```bash 
mkdir vis_results
mkdir videos 
docker run --gpus all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 -it --rm -v $(pwd)/videos:/app/mmhuman3d/videos -v $(pwd)/vis_results/vis_results:/app/mmhuman3d/vis_results -p 8501:8501 nvcr.io/nvidia/pytorch:22.08-py3_mmhuman3d
```

## Usage 
Open the browser at ['http://localhost:8501'](http://localhost:8501)
 
