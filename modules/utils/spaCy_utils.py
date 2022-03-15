# pip3 install spacy
import spacy
import spacy.tokens

from modules.utils.vanilla_utils import clean_text


def string_tokenizer(text, word_delimiters, debug_mode):
    """
    This function takes a string and a list of delimiters as inputs.
    It returns a list of strings, each string being a token of the input string.

    Inputs:
        text: a string
        word_delimiters: a list of strings
        debug_mode: a boolean

    Output:
        tokenized_sentence: a list of strings

    Example:
        text = "Hello, world!"
        word_delimiters = [' ', ',', '!']
        debug_mode = False
        tokenized_sentence = string_tokenizer(text, word_delimiters, debug_mode)
        print(tokenized_sentence)
    """

    # Returning list initialization
    tokenized_sentence = []

    doc = string_sintactical_analysis__initialize_spacy_doc(debug_mode, text, word_delimiters)

    # Text printing in debug mode
    if debug_mode:
        print("\nANALYSIS\n")

    # Going through the list
    for token in doc:
        # Text printing in debug mode
        if debug_mode:
            print("\t", token.text, token.pos_, token.dep_, token.head.text)

        if token.text != '' or token.text != ' ':
            # Push each token inside a list
            tokenized_sentence.append(str(token.text))

    return tokenized_sentence


def string_sintactical_analysis(text, word_delimiters, debug_mode):
    """
    This function takes a string and returns a list of strings, each string being a token of the input string.

    Parameters:
        text (string): The string to be analyzed.
        word_delimiters (string): A string containing all the characters that will be considered as word delimiters.
        debug_mode (boolean): A boolean indicating if the function should print the analysis in the console.

    Returns:
        sintactically_analized_phrase (list): A list of strings, each string being a token of the input string.

    Example:
        string_sintactical_analysis("This is a test.", "", True)

            ANALYSIS
                This POS_A DEP_A HEAD_A
                is POS_B DEP_B HEAD_B
                a POS_C DEP_C HEAD_C
                test POS_D DEP_D HEAD_D
                . POS_E DEP_E HEAD_E

            ['POS_A', 'POS_B', 'POS_C', 'POS_D', 'POS_E']
    """
    # Returning list initialization
    sintactically_analized_phrase = []

    doc = string_sintactical_analysis__initialize_spacy_doc(text, word_delimiters, debug_mode)

    # Text printing in debug mode
    if debug_mode:
        print("\nANALYSIS\n")

    # Going through the list
    for token in doc:
        # Text printing in debug mode
        if debug_mode:
            print("\t", token.text, token.pos_, token.dep_, token.head.text)

        if token.text != '' or token.text != ' ':
            # Push each token inside a list
            sintactically_analized_phrase.append(str(token.pos_))

    return sintactically_analized_phrase


def string_sintactical_analysis__initialize_spacy_doc(text, word_delimiters, debug_mode):
    """
    Initializes a spacy doc object from a text.

    Example:
        initialize_spacy_doc('Hola, ¿cómo estás?', ' ', True)

    :param text: The text to be processed.
    :param word_delimiters: The word delimiters to be used.
    :param debug_mode: Boolean that turns on the code comments
    :return: A spacy doc object.
    """
    # Load the model and create an nlp object
    nlp = spacy.load("es_core_news_md")

    if isinstance(text, list):
        new_text = ''
        last = 0
        for phrase in text:
            if last == (len(phrase) - 1):
                new_text += phrase
            else:
                new_text += phrase + ' '
            last += 1

        text = new_text

    tokens = text.split(word_delimiters)
    words_t = list(filter(None, [t.strip() for t in tokens]))

    # Text printing in debug mode
    if debug_mode:
        print(str(words_t))

    doc_feed = string_sintactical_analysis__initialize_spacy_doc__get_doc_feed(nlp, words_t)

    # Process the text passed to this method as a parameter
    doc = nlp(doc_feed)

    return doc


def string_sintactical_analysis__initialize_spacy_doc__get_doc_feed(nlp, words_t):
    """
        This function takes a list of words and returns a string of those words
        concatenated together with spaces.

        Parameters:
            nlp: A spaCy Language object.
            words_t: A list of strings.

        Returns:
            A string of the words in the list concatenated with spaces.

        Example:
            get_doc_feed(nlp, ['hello', 'world'])

                'hello world'
    """
    doc_feed = ''
    doc_raw_feed = spacy.tokens.Doc(nlp.vocab, words=words_t)
    doc_feed_count = 0
    doc_feed_length = len(doc_raw_feed)

    for element in doc_raw_feed:
        if doc_feed_count != doc_feed_length - 1:
            doc_feed += str(element) + ' '
        else:
            doc_feed += str(element)

        doc_feed_count += 1

    return doc_feed


def find_word_pos_and_surroundings(text, word):
    """

        This function takes a text and a word and returns the previous, actual and next words of the text.

        Parameters:
        text (str): The text to be analysed.
        word (str): The word to be found in the text.

        Returns:
        list: A list with the previous, actual and next words of the text.

        Example:

            find_word_pos_and_surroundings('Esto es una prueba', 'prueba')

            [['una', 'DET'], ['prueba', 'NOUN'], ['', '']]
    """
    nlp = spacy.load("es_core_news_md")

    if isinstance(text, str):
        text = clean_text(text)
        text = nlp(text)

    previous_token_text = ''
    actual_token_text = ''
    next_token_text = ''

    previous_token_pos = ''
    actual_token_pos = ''
    next_token_pos = ''

    found = False

    if isinstance(text, str) or (text != '' and text is not None):
        for token in text:
            if found:
                next_token_text = token.text
                next_token_pos = token.pos_
                break
            if token.text == word:
                actual_token_text = token.text
                actual_token_pos = token.pos_
                found = True
            if not found:
                previous_token_text = token.text
                previous_token_pos = token.pos_

    return [[previous_token_text, previous_token_pos], [actual_token_text, actual_token_pos],
            [next_token_text, next_token_pos]]


def unpack_word_pos_and_surroundings(word_pos_and_surroundings):
    """
        This function takes a word_pos_and_surroundings tuple and returns the
        word, pos, and the surrounding words.

        Parameters:
            word_pos_and_surroundings: A tuple of the form (word, pos,
                                       (left_word, left_pos),
                                       (right_word, right_pos))

        Returns:
            word: The word
            pos: The part of speech
            left_word: The word to the left of the word
            left_pos: The part of speech of the word to the left of the word
            right_word: The word to the right of the word
            right_pos: The part of speech of the word to the right of the word

        Example:
            unpack_word_pos_and_surroundings(("hello", "NOUN"), ("my", "PROPN"), ("friend", "NOUN")))

                ("hello", "NOUN", "my", "PROPN", "friend", "NOUN")
    """
    return word_pos_and_surroundings[0][0], word_pos_and_surroundings[0][1], \
           word_pos_and_surroundings[1][0], word_pos_and_surroundings[1][1], \
           word_pos_and_surroundings[2][0], word_pos_and_surroundings[2][1]
