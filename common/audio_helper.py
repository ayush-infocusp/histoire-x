import io
import librosa


def convert_audio_puarray(audioFile):
    # try:
        # audioFile.seek(0)
        # audio_buffer = io.BytesIO(audioFile.read())
        SAMPLING_RATE = 16000
        audio_data, sample_rate = librosa.load(audioFile, sr=SAMPLING_RATE)
        print("hello 0909",audio_data)
        return {"sample_rate": sample_rate, "audio_data": audio_data}
    # except Exception as e:
        # print(e)
