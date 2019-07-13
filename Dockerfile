FROM ubuntu:latest
LABEL maintainer="snowsphere <prismistim@hotmail.com>"

RUN apt-get update
RUN apt-get install python3 python3-pip libsm6 libxext6 libxrender-dev -y

RUN pip3 install flask tensorflow keras pillow
RUN pip3 install --upgrade opencv-python

CMD cd /home/vnn

# build : docker build . (-t prismistim/vnn:0.1 でタグ付け)
# run : docker run -it --rm -p 7000:7000 -v "c:/Users/snowsphere/workspace/vnn:/home/vnn" prismistim/vnn:0.1