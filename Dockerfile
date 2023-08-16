FROM python:3.10-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y \
    cmake \
    build-essential \
    curl \
    software-properties-common \
    git \
    ffmpeg \
    tesseract-ocr \
    openssl \
    unixodbc \
    curl \
    software-properties-common \
    gcc-11 \ 
    g++-11 \
    sqlite3 \
    libzbar0 \
    && update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 90 --slave /usr/bin/g++ g++ /usr/bin/g++-11 --slave /usr/bin/gcov gcov /usr/bin/gcov-11 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get update \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && bash -c 'source "$HOME/.cargo/env"' 

# debconf: delaying package configuration, since apt-utils is not installed

COPY Home.py  .
COPY utils.py  .
# COPY .streamlit  .
ADD .streamlit /app/.streamlit
COPY requirements.txt  .
# COPY packages.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

## -- production -- ##
## remember to add config.toml file from chat documents file
# EXPOSE 80
# ENTRYPOINT ["streamlit", "run"]
# CMD ["Home.py"]

## -- local deployement -- # 
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]

