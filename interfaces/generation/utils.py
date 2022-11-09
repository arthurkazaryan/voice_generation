import requests

TTS_HOST = 'localhost'
TTS_PORT = 7861
TTS_API_PUSH = '/api/v1/generation/push'
TTS_API_STATUS = '/api/v1/generation/status'
TTS_API_DOWNLOAD = '/api/v1/generation/download'


def post_generation(text: str, voice: str):

    data = {'text': text, 'voice': voice}
    request = requests.post(
        url=f"http://{TTS_HOST}:{TTS_PORT}{TTS_API_PUSH}",
        params=data
    )

    return request


def get_generation_status(task_id: str):

    request_status = requests.post(url=f"http://{TTS_HOST}:{TTS_PORT}{TTS_API_STATUS}",
                                   params={'task_id': task_id})

    return request_status


def get_generation_audio(audio_path: str):

    request_file = requests.get(url=f"http://{TTS_HOST}:{TTS_PORT}{TTS_API_DOWNLOAD}",
                                params={'audio_path': audio_path})

    return request_file
