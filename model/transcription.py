import whisper
import torch

class AudioTranscriber:
    def __init__(self, model_version: str = 'turbo', language: str = 'ru', device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = whisper.load_model(model_version, device=device)
        self.language = language

    def transcribe(self, audio: torch.Tensor) -> str:
        fp16 = self.device != 'cpu' # Suppress warning
        return self.model.transcribe(audio, language=self.language, fp16=fp16)
