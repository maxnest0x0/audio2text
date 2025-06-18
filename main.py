import os
import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from schemas import TranscriptionResponse, TranscriptionSegment

from model.preprocessing import bytes_to_tensor
from model.transcription import AudioTranscriber
from model.diarization import AudioDiarizer

app = FastAPI()
transcriber = AudioTranscriber()
diarizer = AudioDiarizer(os.environ['AUTH_TOKEN'])

@app.post('/api/transcribe')
def transcribe(audio: UploadFile) -> TranscriptionResponse:
    audio = audio.file.read()
    audio = bytes_to_tensor(audio)
    diarization = diarizer.diarize(audio)

    segments = []
    for segment, speaker, start, end in diarization:
        transcriber.set_audio(segment)
        text = transcriber.get_result()
        segments.append(TranscriptionSegment(speaker=speaker, text=text))
        print(speaker, start, end, text)

    return TranscriptionResponse(transcription=segments)

app.mount('/', StaticFiles(directory='web', html=True))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
