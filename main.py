import os
import time
import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from schemas import TranscriptionResponse, TranscriptionSegment

from model.utils import bytes_to_tensor, join_speakers, renumerate_speakers, filter_text
from model.transcription import AudioTranscriber
from model.diarization import AudioDiarizer

app = FastAPI()
transcriber = AudioTranscriber()
diarizer = AudioDiarizer(os.environ['AUTH_TOKEN'])

@app.post('/api/transcribe')
def transcribe(audio: UploadFile) -> TranscriptionResponse:
    start_time = time.time()
    audio = audio.file.read()
    audio = bytes_to_tensor(audio)

    audio_segments = diarizer.diarize(audio)
    audio_segments = join_speakers(audio_segments)

    text_segments = []
    for segment in audio_segments:
        text = transcriber.transcribe(segment.audio)['text']
        segment = TranscriptionSegment(text=text, speaker=segment.speaker, start=segment.start, end=segment.end)
        print(time.time() - start_time, segment)
        text_segments.append(segment)

    text_segments = filter_text(text_segments)
    text_segments = renumerate_speakers(text_segments)

    response = TranscriptionResponse(
        transcription=text_segments,
        speakers=len(set(map(lambda segment: segment.speaker, text_segments))),
        audio_duration=audio.shape[0] / 16000,
        processing_time=time.time() - start_time,
        processing_device=transcriber.device,
    )
    print(response)
    return response

app.mount('/', StaticFiles(directory='web', html=True))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
