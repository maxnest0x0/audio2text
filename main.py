import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles

from model.preprocessing import bytes_to_tensor
from model.transcription import AudioTranscriber

app = FastAPI()

@app.post('/api/transcribe')
async def transcribe(audio: UploadFile):
    print('Reading file...')
    audio = await audio.read()
    print('Running ffmpeg...')
    audio = bytes_to_tensor(audio)

    transcriber = AudioTranscriber()
    transcriber.set_audio(audio)
    print('Transcribing...')
    text = transcriber.get_result()
    print('Result:', text)

    return {
        'transcription': [
            {'speaker': 0, 'text': text},
        ],
    }

app.mount('/', StaticFiles(directory='web', html=True))

if __name__ == '__main__':
    uvicorn.run(app)
