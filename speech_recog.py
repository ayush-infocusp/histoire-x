
# Run in virtual environment
# pip install jupyter-lab
# jupyter-lab


# !pip install torch accelerate torchaudio datasets[audio]
# !pip install --upgrade transformers
# !pip install soundfile
# !pip install librosa
# !pip install jiwer


# pip install ipywidgets


from IPython.display import Audio as Play_Audio
from datasets import load_dataset

from transformers import Wav2Vec2ForCTC, AutoProcessor
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch

import jiwer


fleurs = load_dataset("google/fleurs", "en_us", split="train", streaming=True)
dataset_iterator = iter(fleurs)
#
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")


def getSpeechDetails():
    #
    sample = next(dataset_iterator)
    data = sample['audio']['array']
    # sampling_rate = sample['audio']['sampling_rate']
    #
    sample
    # Play the audio
    # Play_Audio(data=data, rate=sampling_rate)
    #
    inputs = processor(data, sampling_rate=16_000, return_tensors="pt")
    #
    with torch.no_grad():
        outputs = model(**inputs).logits
    #
    ids = torch.argmax(outputs, dim=-1)[0]
    transcription = processor.decode(ids)
    #
    actual = sample['raw_transcription']
    prediction = transcription
    # metrics = jiwer.compute_measures(actual.lower(), prediction.lower())
    #
    return {"actual": actual, "prediction": prediction}
