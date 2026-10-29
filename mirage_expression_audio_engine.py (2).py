import logging
import math
import struct
import wave
from pathlib import Path
from typing import Union, List

logger = logging.getLogger("MirageAudio")

class AudioEngine:
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        logger.info(f"AudioEngine initialized at {sample_rate}Hz sample rate.")

    def generate_tone(self, frequency: float, duration_seconds: float = 1.0, volume: float = 0.5) -> List[float]:
        """Generates a pure sine wave tone for a given frequency and duration."""
        num_samples = int(self.sample_rate * duration_seconds)
        tone_data = []
        
        for i in range(num_samples):
            t = i / self.sample_rate
            # Sine wave formula
            sample = volume * math.sin(2 * math.pi * frequency * t)
            tone_data.append(sample)
            
        return tone_data

    def save_wav(self, audio_data: List[float], filename: Union[str, Path]) -> bool:
        """Exports raw audio float data into a standard playable WAV file."""
        output_path = Path(filename)
        try:
            with wave.open(str(output_path), 'w') as wf:
                # 1 channel (Mono), 2 bytes per sample (16-bit), sample rate
                wf.setparams((1, 2, self.sample_rate, len(audio_data), 'NONE', 'not compressed'))
                
                for sample in audio_data:
                    # Scale float [-1.0, 1.0] to 16-bit PCM integer range [-32768, 32767]
                    scaled = int(max(-1.0, min(1.0, sample)) * 32767)
                    wf.writeframes(struct.pack('<h', scaled))
                    
            logger.info(f"Audio successfully written to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export WAV file: {e}")
            return False

    def synthesize_state_tone(self, state_code: int, output_file: str = "mirage_state.wav") -> bool:
        """Translates an internal numeric state or mirror score into an acoustic signature."""
        # Map a state code to a fundamental frequency (e.g., base 220Hz + state offset)
        base_freq = 220.0 + (state_code * 15.0)
        logger.info(f"Synthesizing state tone for code {state_code} at {base_freq}Hz...")
        
        tone = self.generate_tone(frequency=base_freq, duration_seconds=1.5, volume=0.4)
        return self.save_wav(tone, output_file)