import re


def find_sentence_of_word(text, word):
    """
    This function takes two strings as input and returns a string.

    If the input is not a string, it returns the input.
    If the input is a string, it splits the string by '.' and then returns the sentence containing the word.
    If the word is not in the sentence, it returns the sentence.
    If the word is in the sentence, it returns the sentence containing the word.
    If the word is in the sentence and the word contains '.', it returns the sentence containing the word without the '.'.

    Parameters:
        text (str): The text to be split by '.'
        word (str): The word to be searched in the text

    Returns:
        str: The sentence containing the word or the sentence itself.

    Example:
        find_sentence_of_word('This is a test. This is another.', 'test')

            'This is a test.'
    """
    return_next = False
    previous_sentence = ''
    actual_sentence = ''

    if isinstance(text, str) and isinstance(word, str):
        if not '.' in word:
            text = text.split('.')
            for sentence in text:
                if word in sentence:
                    return sentence
        else:
            text = text.split('.')
            previous_sentence = ''
            return_next = False
            word_without_dot = word.replace('.', '')
            for sentence in text:
                if return_next:
                    actual_sentence = sentence
                    return str(previous_sentence + '.' + actual_sentence)
                if word_without_dot in sentence:
                    return_next = True
                    previous_sentence = sentence
    else:
        if return_next:
            return str(previous_sentence + '.' + actual_sentence)

        return text


def clean_text(text):
    """
        This function takes a string as input and returns a cleaned string.
        The input string is converted to lowercase, non-alphabetical characters are removed,
        and multiples spaces are replaced by single spaces.

        Parameters:
        text (str): The string to be cleaned.

        Returns:
        str: The cleaned string.

        Example:
        clean_text('This is a test string!')

            'this is a test string'
    """
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'[^\w\s]','',text)
        text = re.sub(r'\d+','',text)
        text = re.sub(r'\s+',' ',text)
    return text


def get_nlp_punctuation_marks():
    """
    Returns a list of the punctuation marks used in the Spanish language.

    Parameters:
        None

    Returns:
        list: A list of the punctuation marks used in the Spanish language.

    Example:
        >>> get_nlp_punctuation_marks()

        ['!', '¡', '?', '¿', '%', ',', '...', '.', '…', ':', ';', '<', '>', '"', '·', '$', '%', '&', '/', '(', ')', '=', '\'', '|', '@', '#', '~', '½', '¬', '{', '[' ']', '}', '_', '€', '`', '*', '^', '+', '€', '’', '“', '”', '«', '»', '—']
    """
    return ['!', '¡', '?', '¿', '%', ',', '...', '.', '…', ':', ';', '<', '>', '"', '·', '$', '%', '&', '/', '(', ')', '=', '\'', '|', '@', '#', '~', '½', '¬', '{', '[' ']', '}', '_', '€', '`', '*', '^', '+', '€', '’', '“', '”', '«', '»', '—']
