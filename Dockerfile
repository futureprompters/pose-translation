FROM python:3.10-bookworm

RUN apt-get -y update && apt-get -y install git
RUN pip install --upgrade pip  # enable PEP 660 support \
    && pip install torch torchvision torchaudio \
    && pip install -e . \
    && pip install pycocotools \
    && pip install protobuf==3.20.0 \

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash \
    && apt-get install git-lfs \
    && git lfs install


RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Copy the current directory contents into the container at $HOME/app setting the owner to the user
COPY --chown=user . $HOME/app

RUN pip install -r requirements.txt


EXPOSE 7860

CMD ["python", "app.py"]