import torch
import numpy as np
import subprocess

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
