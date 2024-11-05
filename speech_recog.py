from IPython.display import Audio as Play_Audio
from datasets import load_dataset

from transformers import Wav2Vec2ForCTC, AutoProcessor
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch


fleurs = load_dataset("google/fleurs", "en_us", split="train", streaming=True)
dataset_iterator = iter(fleurs)
#
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")


def get_speech_details(data):
    """get the speech details"""
    inputs = processor(data, sampling_rate=16_000, return_tensors="pt")
    #
    with torch.no_grad():
        outputs = model(**inputs).logits
    #
    ids = torch.argmax(outputs, dim=-1)[0]
    transcription = processor.decode(ids)
    #
    actual = ''
    prediction = transcription
    #
    return {"actual": actual, "prediction": prediction}
