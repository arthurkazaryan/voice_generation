""" from https://github.com/keithito/tacotron """

'''
Defines the set of symbols used in text input to the model.

The default is a set of ASCII characters that works well for English or text that has been run through Unidecode. For other data, you can modify _characters. See TRAINING_DATA.md for details. '''
from .cmudict import valid_symbols


# Prepend "@" to ARPAbet symbols to ensure uniqueness (some are the same as uppercase letters):
_arpabet = ['@' + s for s in valid_symbols]


def get_symbols(symbol_set='english_basic'):
    if symbol_set == 'english_basic':
        _pad = '_'
        _punctuation = '!\'(),.:;? '
        _special = '-'
        _letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        symbols = list(_pad + _special + _punctuation + _letters) + _arpabet
    elif symbol_set == 'english_basic_lowercase':
        _pad = '_'
        _punctuation = '!\'"(),.:;? '
        _special = '-'
        _letters = 'abcdefghijklmnopqrstuvwxyz'
        symbols = list(_pad + _special + _punctuation + _letters) + _arpabet
    elif symbol_set == 'english_expanded':
        _punctuation = '!\'",.:;? '
        _math = '#%&*+-/[]()'
        _special = '_@©°½—₩€$'
        _accented = 'áçéêëñöøćž'
        _letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        symbols = list(_punctuation + _math + _special + _accented + _letters) + _arpabet
    elif symbol_set == 'ipa':
        _pad = '_'
        _punctuation = "!'(),.:;?\" "
        _special = '-'
        _stress = '+'

        # DEFAULT SET OF IPA PHONEMES
        # Phonemes definition (All IPA characters)
        _vowels = "iyɨʉɯuɪʏʊeøɘəɵɤoɛœɜɞʌɔæɐaɶɑɒᵻ"
        _non_pulmonic_consonants = "ʘɓǀɗǃʄǂɠǁʛ"
        _pulmonic_consonants = "pbtdʈɖcɟkɡqɢʔɴŋɲɳnɱmʙrʀⱱɾɽɸβfvθðszʃʒʂʐçʝxɣχʁħʕhɦɬɮʋɹɻjɰlɭʎʟ"
        _suprasegmentals = "ˈˌːˑ"
        _other_symbols = "ʍwɥʜʢʡɕʑɺɧʲ ͡"
        _diacrilics = "ɚ˞ɫ"
        _phonemes = _vowels + _non_pulmonic_consonants + _pulmonic_consonants + _suprasegmentals + _other_symbols + _diacrilics

        symbols = list(set(list(_pad + _special + _stress + _punctuation + _phonemes)))

    elif symbol_set == 'russian_basic':
        _pad = '_'
        _punctuation = "!'(),.:;?\" "
        _special = '-'
        _stress = '+'
        _letters = "абвгдежзийклмнопрстуфхцчшщъыьэюяёє"

        symbols = list(_pad + _special + _stress + _punctuation + _letters)
    else:
        raise Exception("{} symbol set does not exist".format(symbol_set))

    return symbols


def get_pad_idx(symbol_set='english_basic'):
    if symbol_set in {'english_basic', 'english_basic_lowercase', 'ipa', 'russian_basic'}:
        return 0
    else:
        raise Exception("{} symbol set not used yet".format(symbol_set))
