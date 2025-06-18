from pyannote.audio import Pipeline
import whisper
import torch

class AudioDiarizer:
    def __init__(self, auth_token, model="pyannote/speaker-diarization-3.1", device=None):
        self.device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))

        self.pipeline = Pipeline.from_pretrained(model, use_auth_token=auth_token)
        self.pipeline.to(self.device)

    def diarize(self, audio, sr=16000):
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
            segments.append((audio_segment, speaker, start, end))
        return segments
