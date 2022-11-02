
class Dataset:
    LANGUAGES = {'ru', 'en', 'es', 'it'}
    AVAILABLE_PATTERNS = {
        'wav',
        'mel', 'pitch',
        'speaker', 'embed',
        'text', 'stress', 'phonemes',
        'language', 'score'
    }
    DEPENDENCY_MAP = {
        'mel': 'wav',
        'embed': 'wav',
        'stress': 'text',

        'wav': 'wav',
        'text': 'text',
        'speaker': 'speaker',
        'score': 'score',
        'phonemes': 'stress'
    }

    def __init__(
        self,
        language,
        root_path,
        metadata='metadata.csv',
        in_pattern='wav|text|speaker',
        out_pattern='wav|embed|stress|speaker',
    ):
        self.language = language
        if language not in self.LANGUAGES:
            raise Exception(f'This language ({language}) not supported, available languages:', self.LANGUAGES)
            
        self.in_pattern = in_pattern.split('|')
        self.out_pattern = out_pattern.split('|')

        diff = set(self.in_pattern + self.out_pattern) - self.AVAILABLE_PATTERNS
        if diff:
            raise Exception('Check your "in" or "out" patterns', diff)

        self.root_path = root_path
        self.metadata = metadata
