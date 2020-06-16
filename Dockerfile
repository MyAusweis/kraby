# Build a docker image containing:
# * Tensorflow 1.15 with Cuda support
# * Stable-Baselines

FROM tensorflow/tensorflow:1.15.2-gpu-py3-jupyter
RUN pip install gym stable-baselines
WORKDIR /tf/kraby
COPY . /tf/kraby
RUN pip install -e .
