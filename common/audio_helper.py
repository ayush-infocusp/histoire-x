import io
import librosa


def convert_audio_puarray(audioFile):
    try:
        SAMPLING_RATE = 16000
        audio_data, sample_rate = librosa.load(audioFile, sr=SAMPLING_RATE)
        return {"sample_rate": sample_rate, "audio_data": audio_data}
    except Exception as e:
        print(e)
