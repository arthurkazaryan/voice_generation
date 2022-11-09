from TTS.utils.synthesizer import Synthesizer

synthesizer = None

def predict(voice: str, text: str) -> str:
    global synthesizer
    if synthesizer is None:
        synthesizer = Synthesizer(
            '../coqui-vits/best_model_66120.pth',
            '../coqui-vits/config.json',
            tts_languages_file=None,
            tts_speakers_file='../coqui-vits/speakers.pth',
            vocoder_config=None,
            vocoder_checkpoint=None,
            encoder_config=None,
            encoder_checkpoint=None,
            use_cuda=True
        )

    wav = synthesizer.tts(
        text=text,
        speaker_name=voice,
        language_name=None,
        speaker_wav=None,
        reference_wav=None,
        style_wav=None,
        style_text=None,
        reference_speaker_name=None,
    )

    synthesizer.save_wav(wav, 'aud.wav')
    return 'aud.wav'
