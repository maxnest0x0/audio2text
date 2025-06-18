from dataclasses import dataclass
from pydantic import BaseModel
from torch import Tensor

@dataclass
class AudioSegment:
    audio: Tensor
    speaker: int
    start: float
    end: float

class TranscriptionSegment(BaseModel):
    text: str
    speaker: int
    start: float
    end: float

class TranscriptionResponse(BaseModel):
    transcription: list[TranscriptionSegment]
    speakers: int
    audio_duration: float
    processing_time: float
    processing_device: str
