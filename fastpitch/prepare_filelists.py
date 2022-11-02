import os
from collections import defaultdict
from dataset_utils.tts_dataset import Dataset
from pathlib import Path
import json
import random
from tqdm import tqdm

# from text.symbols import symbols
from common.text.symbols import get_symbols
symbols = get_symbols('ipa')

FLIST_PREFIX = 'ru_phonemes'
IN_PATTERN = 'wav|pitch|embed|phonemes|speaker'
OUT_PATTERN = 'wav|pitch|phonemes|speaker'
METADATA_NAME = 'metadata_embed_stress_phonemes_22k_pitch.csv'
DATASETS = [
    # Dataset('ru', '/windows/TTSDatasets/RuDevices', metadata=METADATA_NAME, in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
    # Dataset('ru', '/windows/TTSDatasets/RuDevicesAudiobooks', metadata=METADATA_NAME, in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
    # Dataset('es', '/windows/TTSDatasets/es/tux-valid', metadata='metadata_embed_phonemes.csv', in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
    # Dataset('it', '/windows/TTSDatasets/it/by_book', metadata='metadata_embed_phonemes.csv', in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
    # Dataset('ru', '/windows/TTSDatasets/ru/common_ru', metadata=METADATA_NAME, in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
    # Dataset('ru', '/windows/TTSDatasets/ru/good_books', metadata=METADATA_NAME, in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
    # Dataset('ru', '/windows/TTSDatasets/ru/overwatch', metadata=METADATA_NAME, in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
    # Dataset('ru', '/windows/TTSDatasets/ru/witcher', metadata=METADATA_NAME, in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
    # Dataset('en', '/windows/TTSDatasets/en/LibriTTS', metadata=METADATA_NAME, in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
    # Dataset('en', '/windows/TTSDatasets/en/VCTK', metadata=METADATA_NAME, in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
    Dataset('ru', '/windows/TTSDatasets/ru/ru-books-clean-1', metadata=METADATA_NAME, in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
    Dataset('ru', '/windows/TTSDatasets/ru/ru-books-clean-2', metadata=METADATA_NAME, in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
    Dataset('ru', '/windows/TTSDatasets/ru/ruslan', metadata=METADATA_NAME, in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
    Dataset('ru', '/windows/TTSDatasets/ru/natasha', metadata=METADATA_NAME, in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
    Dataset('ru', '/windows/TTSDatasets/ru/gerasimov', metadata=METADATA_NAME, in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
    Dataset('ru', '/windows/TTSDatasets/ru/klykvin', metadata=METADATA_NAME, in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
    Dataset('ru', '/windows/TTSDatasets/ru/levashev', metadata=METADATA_NAME, in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
    # Dataset('ru', '/windows/TTSDatasets/ru/triple', metadata=METADATA_NAME, in_pattern=IN_PATTERN, out_pattern=OUT_PATTERN),
]

train, val = [], []
speakers_map, languages_map, = {}, {}
dataset = defaultdict(list)


def split_dataset(speaker, items):
    """Split a dataset into train and eval.

    Args:
        items (List[List]): A list of samples. Each sample is a list of `[audio_path, text, ...]`.
    """
    MIN_SIZE = 15
    eval_split_size = min(MIN_SIZE, int(len(items) * 0.1))
    if len(items) < MIN_SIZE:
        print(f" [!{speaker}!] You do not have enough samples ({len(items)}) to train. You need at least {MIN_SIZE} samples.")
        del speakers_map[speaker]
        return [], []
    random.seed(0)
    random.shuffle(items)
    return items[:eval_split_size], items[eval_split_size:]


count_skipped = 0
for ds in DATASETS:
    metadata_path = f'{ds.root_path}/{ds.metadata}'
    with open(metadata_path, 'r', encoding='utf-8') as md:
        lines = md.readlines()

    for line in tqdm(lines):
        line = line.strip().split('|')
        items = {name: item for name, item in zip(ds.in_pattern, line)}
        speaker = items['speaker']

        if not speakers_map.get(speaker):
            speakers_map[speaker] = str(len(speakers_map))
        if not languages_map.get(ds.language):
            languages_map[ds.language] = str(len(languages_map))

        for k in ['wav', 'embed', 'pitch']:
            if items.get(k):
                items[k] = str(Path(ds.root_path, items[k]))

        items['speaker'] = speakers_map[speaker]
        items['language'] = languages_map[ds.language]

        skip = False
        for k in ({'wav', 'embed'} & set(ds.out_pattern)):
            if items.get(k):
                if not os.path.exists(items[k]):
                    skip = True
                    break
        if skip:
            continue

        for k in ['text', 'stress', 'phonemes']:
            if text := items.get(k):
                out_text = ""
                for sym in text:
                    if sym not in symbols:
                        print(f'Skipped "{sym}" from {text}')
                    else:
                        out_text += sym
                items[k] = out_text.replace('_', '')

        dataset[speaker].append([items[k] for k in  ds.out_pattern])

for speaker, items in dataset.items():
    v, t = split_dataset(speaker, items)
    train += t
    val += v

Path(f'filelists/{FLIST_PREFIX}').mkdir(parents=True, exist_ok=True)
with open(f'filelists/{FLIST_PREFIX}/train.txt', 'w', encoding='utf-8') as out:
    random.seed(0)
    random.shuffle(train)
    for line in train:
        out.write('|'.join(line) + '\n')

with open(f'filelists/{FLIST_PREFIX}/val.txt', 'w', encoding='utf-8') as out:
    random.seed(0)
    random.shuffle(val)
    for line in val:
        out.write('|'.join(line) + '\n')


with open(f'filelists/{FLIST_PREFIX}/speakers.json', 'w', encoding='utf-8') as out:
    json.dump(speakers_map, out, indent=4)

with open(f'filelists/{FLIST_PREFIX}/languages.json', 'w', encoding='utf-8') as out:
    json.dump(languages_map, out, indent=4)
