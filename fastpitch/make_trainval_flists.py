from pathlib import Path
import json
import random
from tqdm import tqdm
from pydub import AudioSegment

MIN_AUDIO_LENGTH = 0.5
MAX_AUDIO_LENGTH = 12
FLIST_PREFIX = 'ru_align'


class DS:
    def __init__(self, base_dir, metafile=None, speaker=None, pattern='wav|pitch|text|speaker'):
        self.base_dir = base_dir
        self.metafile = metafile
        self.speaker = speaker
        self.pattern = pattern


# DATASETS = [
#     # DS('/storage/zolkin/VCTK', 'metadata_pitch.csv'),
#     DS('/storage/zolkin/LJS/LJSpeech-1.1', 'metadata_v3_pitch.csv', 'LJSpeech', 'wav|pitch|text'),
#     DS('/storage/zolkin/hifi_clean', 'filelist_92_pitch.txt'),
#     # DS('/storage/zolkin/hifi_clean', 'filelist_6097_pitch.txt'),
#     # DS('/storage/zolkin/hifi_clean', 'filelist_9017_pitch.txt'),
#     # DS('/storage/zolkin/audiobooks/en_male_smith_m', 'metadata_pitch.csv', 'smith_m', 'wav|pitch|text'),
#     # DS('/storage/zolkin/audiobooks/en_male_snelson_r', 'metadata_pitch.csv', 'snelson_r', 'wav|pitch|text')
# ]
DATASETS = [
    DS('/home/zolkin/datasets/ru/natasha', 'marks_pitch.txt', 'natasha', 'wav|pitch|text'),
    DS('/home/zolkin/datasets/ru/ruslan', 'marks_pitch.txt', 'ruslan', 'wav|pitch|text'),
    DS('/home/zolkin/datasets/ru/ru-books-clean-1', 'metadata_pitch.csv'),
    DS('/home/zolkin/datasets/ru/ru-books-clean-2', 'metadata_pitch.csv'),
    # DS('/home/zolkin/datasets/ru/presentations', 'metadata_pitch.csv')
]
train, val = [], []
speakers_map, dataset = {}, {}
out_pattern = 'wav|pitch|text|speaker'


def split_dataset(items):
    """Split a dataset into train and eval.

    Args:
        items (List[List]): A list of samples. Each sample is a list of `[audio_path, text, ...]`.
    """
    eval_split_size = min(500, int(len(items) * 0.1))
    # assert eval_split_size > 0, " [!] You do not have enough samples to train. You need at least 100 samples."
    random.seed(0)
    random.shuffle(items)
    return items[:eval_split_size], items[eval_split_size:]


count_skipped = 0
for ds in DATASETS:
    with open(Path(ds.base_dir, ds.metafile), 'r', encoding='utf-8') as inp:
        lines = inp.readlines()

    for line in tqdm(lines):
        obj = {}
        for k, v in zip(ds.pattern.split('|'), line.strip().split('|')):
            obj[k] = v
        speaker = ds.speaker or obj['speaker']
        if not speakers_map.get(speaker):
            speakers_map[speaker] = str(len(speakers_map))
        for k in ['wav', 'mel', 'pitch', 'align']:
            if obj.get(k):
                obj[k] = str(Path(ds.base_dir, obj[k]))
        obj['speaker'] = speakers_map[speaker]
        if wav := obj.get('wav'):
            segment = AudioSegment.from_wav(wav)
            if not (MIN_AUDIO_LENGTH < segment.duration_seconds <= MAX_AUDIO_LENGTH):
                # print(wav, segment.duration_seconds)
                count_skipped += 1
                continue

        if not dataset.get(speaker):
            dataset[speaker] = []

        dataset[speaker].append([obj[k] for k in out_pattern.split('|')])

for speaker, items in dataset.items():
    v, t = split_dataset(items)
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

print('Skipped audios:', count_skipped)
