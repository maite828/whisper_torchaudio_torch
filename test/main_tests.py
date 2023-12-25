import unittest
import pytest
import os

from whisper_torchaudio_torch.main import transcribe_audio, exclude_audio_chunk


@pytest.fixture
def sample_audio_file():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample_audio.wav")


def test_transcribe_audio(sample_audio_file):
    model = "base"
    language = "galician"
    result = transcribe_audio(model, sample_audio_file, language)
    assert result is not None
    assert result['text'] in [" Mercores 3 de marzo de 1992.", " Mercores III de marzo de 1992."]


def test_exclude_audio_chunk(sample_audio_file):
    start_time = 0.5
    end_time = 1.5
    audio_excluded, sample_rate = exclude_audio_chunk(sample_audio_file, start_time, end_time)

    assert audio_excluded is not None
    assert sample_rate == 8000
    assert audio_excluded.shape[1] == 32725


if __name__ == '__main__':
    unittest.main()
