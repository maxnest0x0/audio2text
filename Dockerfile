FROM pytorch/pytorch
WORKDIR /app

ARG AUTH_TOKEN
ENV AUTH_TOKEN=${AUTH_TOKEN}

RUN apt-get update && \
    apt-get install --assume-yes --no-install-recommends ffmpeg

COPY requirements.txt .
RUN pip install --requirement requirements.txt

RUN python -c "import whisper; whisper.load_model('turbo')"
RUN python -c "from pyannote.audio import Pipeline; \
    Pipeline.from_pretrained('pyannote/speaker-diarization-3.1', use_auth_token='${AUTH_TOKEN}')"

COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
