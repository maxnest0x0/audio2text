import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles

from model.preprocessing import bytes_to_tensor
from model.transcription import AudioTranscriber

app = FastAPI()
transcriber = AudioTranscriber()

@app.post('/api/transcribe')
async def transcribe(audio: UploadFile):
    audio = await audio.read()
    audio = bytes_to_tensor(audio)
    transcriber.set_audio(audio)
    text = transcriber.get_result()
    print(text)

    return {
        'transcription': [
            {'speaker': 0, 'text': text},
        ],
    }

app.mount('/', StaticFiles(directory='web', html=True))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
