FROM ubuntu:xenial

RUN apt-get update

RUN apt-get install -y \
    curl \
    bzip2 \
    libfreetype6 \
    libgl1-mesa-dev \
    libglu1-mesa \
    libxi6 \
    python3 \
    python3-pip \
    python-imaging

RUN apt-get -y autoremove

COPY requirements.txt .

RUN pip3 install -r requirements.txt

RUN curl -SL http://download.blender.org/release/Blender2.77/blender-2.77a-linux-glibc211-x86_64.tar.bz2 -o blender.tar.bz2

RUN mkdir /usr/local/blender && \
    tar -jxvf blender.tar.bz2 -C /usr/local/blender --strip-components=1 && \
    rm blender.tar.bz2

VOLUME /data

COPY scene.py .
COPY palette.py .
COPY bot.py .
COPY scene.blend .

ENTRYPOINT ["/usr/local/blender/blender", "-b"]
