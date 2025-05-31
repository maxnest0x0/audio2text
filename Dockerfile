FROM pytorch/pytorch
WORKDIR /app

RUN apt-get update && \
    apt-get install --assume-yes --no-install-recommends ffmpeg

COPY requirements.txt .
RUN pip install --requirement requirements.txt

RUN python -c "import whisper; whisper.load_model('turbo')"

COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
