import whisper
import torch

class AudioTranscriber:
    def __init__(self, model_version: str ='turbo', language: str ='ru', device: str = None) -> None:
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model =  whisper.load_model(model_version, device=device)

        self.language = language

    def set_audio(self, audio) -> None:
        self.audio = audio

    def remove_the_noise(self) -> None:
        pass

    def __transcribe(self):
        fp16 = self.device != 'cpu' # Suppress warning
        return self.model.transcribe(self.audio, language=self.language, fp16=fp16)

    def recognize_the_polyphony(self):
        pass

    def get_result(self) -> str:
        return self.__transcribe()['text']
