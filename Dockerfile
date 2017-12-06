# Start with cuDNN base image
FROM nvidia/cuda:8.0-cudnn5-devel-ubuntu16.04
WORKDIR /env
# Install git, wget, python-dev, pip, BLAS + LAPACK and other dependencies
RUN apt-get update && apt-get install -y \
  gfortran \
  git \
  wget \
  liblapack-dev \
  libopenblas-dev \
  python-dev \
  python-pip \
  python-nose \
  python-numpy \
  python-scipy

ADD . /env
# Set CUDA_ROOT
ENV CUDA_ROOT /usr/local/cuda/bin
ENV PYTHONPATH /env
# Install bleeding-edge Theano
ARG THEANO_VERSION=rel-0.8.2
RUN pip install --upgrade pip
RUN pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git@${THEANO_VERSION}
RUN pip install --upgrade six
# Set up .theanorc for CUDA
RUN echo "[global]\ndevice=gpu\nfloatX=float32\noptimizer_including=cudnn\n[lib]\ncnmem=0.1\n[nvcc]\nfastmath=True" > /root/.theanorc

# Install OpenCV
RUN git clone --depth 1 https://github.com/opencv/opencv.git /env/opencv && \
	cd /env/opencv && \
	mkdir build && \
	cd build && \
	cmake -DWITH_QT=ON -DWITH_OPENGL=ON -DFORCE_VTK=ON -DWITH_TBB=ON -DWITH_GDAL=ON -DWITH_XINE=ON -DBUILD_EXAMPLES=ON .. && \
	make -j"$(nproc)"  && \
	make install && \
	ldconfig && \
	echo 'ln /dev/null /dev/raw1394' >> ~/.bashrc

CMD ["python","NNRobotUSup/Brain/__init__.py"]