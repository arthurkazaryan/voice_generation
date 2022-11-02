import os

from trainer import Trainer, TrainerArgs

from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.vits import Vits, VitsArgs, VitsAudioConfig, CharactersConfig
from TTS.tts.utils.speakers import SpeakerManager
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor

output_path = os.path.dirname(os.path.abspath(__file__))
# dataset_config = BaseDatasetConfig(formatter="all_in_one", language="ru", path='/home/zolkin/datasets/ru')

dataset_config = BaseDatasetConfig(
    formatter="all_in_one", meta_file_train="", language="ru", path=os.path.join(output_path, "/home/zolkin/datasets/ru")
)

# dataset_configs = [
    # BaseDatasetConfig(formatter="wav_emb_text_spk", language="ru", path='/home/zolkin/datasets/ru/ru-books-clean-1'),
    # BaseDatasetConfig(formatter="wav_emb_text_spk", language="ru", path='/home/zolkin/datasets/ru/ru-books-clean-2'),
    # BaseDatasetConfig(formatter="wav_emb_text_spk", language="ru", path='/home/zolkin/datasets/ru/ruslan'),
    # BaseDatasetConfig(formatter="wav_emb_text_spk", language="ru", path='/home/zolkin/datasets/ru/natasha'),
    # BaseDatasetConfig(formatter="wav_emb_text_spk", language="ru", path='/home/zolkin/datasets/ru/gerasimov'),
    # BaseDatasetConfig(formatter="wav_emb_text_spk", language="ru", path='/home/zolkin/datasets/ru/klykvin'),
    # BaseDatasetConfig(formatter="wav_emb_text_spk", language="ru", path='/home/zolkin/datasets/ru/levashev'),
    # BaseDatasetConfig(formatter="wav_emb_text_spk", language="ru", path='/home/zolkin/datasets/ru/triple'),
# ]

audio_config = VitsAudioConfig(
    sample_rate=22050, win_length=1024, hop_length=256, num_mels=80, mel_fmin=0, mel_fmax=None
)

vitsArgs = VitsArgs(
    use_speaker_embedding=True,
)

config = VitsConfig(
    model_args=vitsArgs,
    audio=audio_config,
    run_name="ru_multispeaker",
    batch_size=32,
    eval_batch_size=16,
    batch_group_size=5,
    num_loader_workers=4,
    num_eval_loader_workers=4,
    run_eval=True,
    test_delay_epochs=-1,
    epochs=1000,
    text_cleaner="ru_cleaners",
    use_phonemes=False,
    phoneme_language="ru",
    phoneme_cache_path=os.path.join(output_path, "phoneme_cache"),
    compute_input_seq_cache=True,
    print_step=25,
    print_eval=False,
    mixed_precision=False,
    max_text_len=325,  # change this if you have a larger VRAM than 16GB
    output_path=output_path,
    datasets=dataset_config,
    characters=CharactersConfig(
        characters_class="TTS.tts.models.vits.VitsCharacters",
        pad="<PAD>",
        eos="<EOS>",
        bos="<BOS>",
        blank="<BLNK>",
        characters="\"!'(),-.:;?абвгдежзийклмнопрстуфхцчшщъыьэюяё+",
        punctuations="\"!'(),-.:;? ",
        phonemes=None,
    ),
    test_sentences=[
        ["Я думаю, что этот стартап действительно удивительный.", "0", None, "ru"],
        ["Я думаю, что этот стартап действительно удивительный.", "1", None, "ru"],
        ["Я думаю, что этот стартап действительно удивительный.", "2", None, "ru"],
        ["Я думаю, что этот стартап действительно удивительный.", "3", None, "ru"],
    ],
    cudnn_benchmark=False,
)

# INITIALIZE THE AUDIO PROCESSOR
# Audio processor is used for feature extraction and audio I/O.
# It mainly serves to the dataloader and the training loggers.
ap = AudioProcessor.init_from_config(config)

# INITIALIZE THE TOKENIZER
# Tokenizer is used to convert text to sequences of token IDs.
# config is updated with the default characters if not defined in the config.
tokenizer, config = TTSTokenizer.init_from_config(config)

# LOAD DATA SAMPLES
# Each sample is a list of ```[text, audio_file_path, speaker_name]```
# You can define your custom sample loader returning the list of samples.
# Or define your custom formatter and pass it to the `load_tts_samples`.
# Check `TTS.tts.datasets.load_tts_samples` for more details.
train_samples, eval_samples = load_tts_samples(
    dataset_config,
    eval_split=True,
    eval_split_max_size=config.eval_split_max_size,
    eval_split_size=config.eval_split_size,
)

# init speaker manager for multi-speaker training
# it maps speaker-id to speaker-name in the model and data-loader
speaker_manager = SpeakerManager()
speaker_manager.set_ids_from_data(train_samples + eval_samples, parse_key="speaker_name")
config.model_args.num_speakers = speaker_manager.num_speakers

# init model
model = Vits(config, ap, tokenizer, speaker_manager)

# init the trainer and 🚀
trainer = Trainer(
    TrainerArgs(),
    config,
    output_path,
    model=model,
    train_samples=train_samples,
    eval_samples=eval_samples,
)
trainer.fit()
