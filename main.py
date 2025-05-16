import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.post('/api/transcribe')
def transcribe(audio: UploadFile):
    return {
        'transcription': [
            {'speaker': 0, 'text': 'Привет всем! Как ваши дела? Сегодня у нас очень интересная тема для обсуждения.'},
            {'speaker': 1, 'text': 'Привет! Да, я согласен. Я думаю, что мы можем начать с самого начала, чтобы все были в курсе.'},
            {'speaker': 0, 'text': 'Отлично! Тогда, давайте начнём с того, что... эээ... нужно определиться с основными понятиями, чтобы не было путаницы.'},
            {'speaker': 2, 'text': 'Извините, что вмешиваюсь, но мне кажется, что мы упускаем важный момент. А именно...'},
            {'speaker': 1, 'text': 'Да, ты прав! Спасибо, что обратил на это внимание. Это действительно важно.'},
            {'speaker': 0, 'text': 'Хорошо, тогда давайте вернёмся к этому вопросу чуть позже. Сейчас же, давайте продолжим с тем, что мы уже начали обсуждать.'},
        ],
    }

app.mount('/', StaticFiles(directory='web', html=True))

if __name__ == '__main__':
    uvicorn.run(app)
