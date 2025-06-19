import torch
import numpy as np
import subprocess
from schemas import AudioSegment, TranscriptionSegment

# Whisper's `load_audio` apparently doesn't support audio buffer as input
def bytes_to_tensor(buffer: bytes, sr: int = 16000) -> torch.Tensor:
    cmd = [
        "ffmpeg",
        "-nostdin",
        "-threads", "0",
        "-i", "-",
        "-f", "s16le",
        "-ac", "1",
        "-acodec", "pcm_s16le",
        "-ar", str(sr),
        "-"
    ]
    out = subprocess.run(cmd, input=buffer, capture_output=True, check=True).stdout
    ndarray = np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0
    return torch.from_numpy(ndarray)

def join_speakers(segments: list[AudioSegment], separation_time: float = 5) -> list[AudioSegment]:
    last_segment: AudioSegment = None
    results = []

    for segment in segments:
        if (last_segment is not None and
            last_segment.speaker == segment.speaker and
            segment.start - last_segment.end < separation_time):
            last_segment.audio = torch.cat([last_segment.audio, segment.audio])
            last_segment.end = segment.end
        else:
            if last_segment is not None:
                results.append(last_segment)
            last_segment = segment
    if last_segment is not None:
        results.append(last_segment)

    return results

def renumerate_speakers(segments: list[TranscriptionSegment]) -> list[TranscriptionSegment]:
    next_speaker = 0
    mapping = {}
    results = []

    for segment in segments:
        if segment.speaker not in mapping:
            mapping[segment.speaker] = next_speaker
            next_speaker += 1
        segment.speaker = mapping[segment.speaker]
        results.append(segment)

    return results

def filter_text(segments: list[TranscriptionSegment]) -> list[TranscriptionSegment]:
    # Phrases that likely got into dataset from subtitles during silence
    weird_phrases = [
        'Продолжение следует...',
        'Субтитры сделал DimaTorzok',
        'Добавил субтитры DimaTorzok',
        'ПОДПИШИСЬ НА КАНАЛ',
    ]
    results = []

    for segment in segments:
        for phrase in weird_phrases:
            segment.text = segment.text.replace(phrase, '')
        segment.text = segment.text.strip()
        if segment.text:
            results.append(segment)

    return results
