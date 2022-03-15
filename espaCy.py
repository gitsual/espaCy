from modules.cache.espaCy_cache import get_cache
from modules.utils.spaCy_utils import string_tokenizer, string_sintactical_analysis, get_nlp_punctuation_marks


def espacy(word, word_pos, phrase):
    """
    This function takes in a word, its part of speech, and the phrase it is in.
    It then checks to see if the word is in the cache, and if it is, it returns
    the part of speech that the word should be. If the word is not in the cache,
    it returns the original part of speech.

    Parameters:
        word (str): The word to be checked
        word_pos (str): The part of speech of the word
        phrase (str): The phrase the word is in

    Returns:
        corrected_pos (str): The corrected part of speech

    Example:
        >>> espacy('el', 'DET', 'el perro')

        'DET'


        >>> espacy('perro', 'NOUN', 'el perro')

        'NOUN'
    """
    cache = get_cache()

    corrected_pos = word_pos

    if word in cache.keys():
        corrected_pos = get_corrected_pos(word, word_pos, phrase, cache)

    if not isinstance(corrected_pos, str) or corrected_pos == '':
        corrected_pos = word_pos

    return corrected_pos


def get_corrected_pos(word, word_pos, phrase, cache):
    """
    This function is a part of the cache system. It is used to get the corrected pos of a word
    from the cache.

    Parameters:
        word (str): The word to be corrected.
        word_pos (str): The pos of the word to be corrected.
        phrase (str): The phrase where the word is.
        cache (dict): The cache dictionary.

    Returns:
        word_pos (str): The corrected pos of the word.

    Example:
        >>> get_corrected_pos('casa', 'NOUN', 'Esta es la casa de Maria', cache)

        'NOUN'
    """

    tokenized_phrase = string_tokenizer(phrase, ''.join(get_nlp_punctuation_marks()), False)
    analyzed_phrase = string_sintactical_analysis(phrase, ''.join(get_nlp_punctuation_marks()), False)
    next_word_pos, previous_word_pos = get_surrounding_words_pos(word, tokenized_phrase, analyzed_phrase)
    spacy_tag_pattern = pack_words(previous_word_pos, word_pos, next_word_pos)

    if (spacy_tag_pattern in cache[word].keys()) or (spacy_tag_pattern.replace(' ', '\t') in cache[word].keys()) or (spacy_tag_pattern.replace(' ', '') in cache[word].keys()):
        word_pos = get_corrected_pos_from_cache(cache, spacy_tag_pattern, word)

    return word_pos


def get_corrected_pos_from_cache(cache, spacy_tag_pattern, word):
    """
    This function takes a cache and a spacy tag pattern as inputs.
    It returns the first key in the cache[word][spacy_tag_pattern] that is a valid key.
    If no such key exists, it returns None.

    Example:
        >>> cache = {'the': {'DET': {'DT': True, 'PDT': True, 'WDT': True}, 'PRP$': {'PRP$': True}, 'WP': {'WP': True}}}
        >>> spacy_tag_pattern = 'DET'
        >>> get_corrected_pos_from_cache(cache, spacy_tag_pattern, 'the')

        'DT'
    """
    spacy_tag_pattern_keys = cache[word][spacy_tag_pattern.replace(' ', '')]
    iterator = iter(spacy_tag_pattern_keys)

    return iterator.__next__()


def analize_syntactically(text_to_analyze):
    """
    This function takes a string as input and returns a string as output.

    The input string is a text to be analyzed syntactically.
    The input string is analyzed using the string_sintactical_analysis function.
    The output string is a text with the tags of the syntactic analysis of the input text.
    The output string is built by concatenating the tags of the syntactic analysis of the input string.

    Example:
        >>> analize_syntactically('The dog is sleeping.')

        'DET NOUN VERB DET NOUN .'
    """
    spacy_tag_pattern = ''
    syntactical_analysis = string_sintactical_analysis(text_to_analyze, '.', False)
    for tag_pattern in syntactical_analysis:
        spacy_tag_pattern += tag_pattern + ' '
    spacy_tag_pattern = spacy_tag_pattern[:-1]
    return spacy_tag_pattern


def pack_words(previous, word, next):
    """
    This function takes three strings as arguments and returns a single string.

    Example:
        >>> pack_words('John', 'likes', 'to')

        'John likes to'

    :param previous: The string that appears immediately before the current word.
    :param word: The current word.
    :param next: The string that appears immediately after the current word.
    :return: A single string containing the three input strings separated by single spaces.
    """
    text_to_analyze = ''
    if previous:
        text_to_analyze += previous + ' '
    text_to_analyze += word
    if next:
        text_to_analyze += ' ' + next
    return text_to_analyze


def get_surrounding_words_pos(word, tokenized_phrase, analyzed_phrase):
    """
    This function takes a word and a phrase and returns the next and previous word of the given word in the given phrase.
    The function takes the phrase and tokenizes it into words, then it analyses the words and returns the next and previous
    word of the given word.

    Example:
        >>> get_surrounding_words_pos('the', 'the quick brown fox jumps over the lazy dog', ['AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG', 'HH', 'II', 'JJ'])

        ('BB', 'FF')

    :param word: The word to find the next and previous word of.
    :param tokenized_phrase: The phrase to search in.
    :param analyzed_phrase: The analyzed phrase.
    :return: The next and previous word of the given word in the given phrase.
    """

    get_next = False
    finish = False

    next = ''
    previous = ''

    if not finish:
        for token, token_pos in zip(tokenized_phrase, analyzed_phrase):
            if get_next:
                next = token_pos
                finish = True
                break
            if token == word:
                get_next = True

            if not get_next:
                previous = token_pos

    return next, previous


if __name__ == '__main__':
    print(espacy('femenino', 'Descripción esquemática del ciclo sexual femenino', 'NOUN'))
