import whisper
import torch
from pyannote.audio import Pipeline
from schemas import AudioSegment

class AudioDiarizer:
    def __init__(self, auth_token: str, model: str = "pyannote/speaker-diarization-3.1", device: str = None):
        self.device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))

        self.pipeline = Pipeline.from_pretrained(model, use_auth_token=auth_token)
        self.pipeline.to(self.device)

    def diarize(self, audio: torch.Tensor, sr=16000) -> list[AudioSegment]:
        source = {
            'waveform': audio.unsqueeze(0),
            'sample_rate': sr,
        }
        diarization = self.pipeline(source)

        segments = []
        for segment, _, speaker in diarization.itertracks(yield_label=True):
            start, end = segment.start, segment.end
            speaker = int(speaker.removeprefix('SPEAKER_'))

            audio_segment = audio[int(start * sr):int(end * sr)]
            segments.append(AudioSegment(audio=audio_segment, speaker=speaker, start=start, end=end))
        return segments
