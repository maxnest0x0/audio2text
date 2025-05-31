from pydantic import BaseModel

class TranscriptionSegment(BaseModel):
    speaker: int
    text: str

class TranscriptionResponse(BaseModel):
    transcription: list[TranscriptionSegment]
