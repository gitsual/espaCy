import os


def get_cache():
    """
        This function checks if the file is empty, if it is, it creates inside the pattern of the 'caché.txt' file.
        If the file is not empty, it reads the file and returns the content of the file.
        :return: The content of the file.

    Example:
        >>> get_cache()
        ['1,2,3,4,5,6,7,8,9,10', '1,2,3,4,5,6,7,8,9,10', '1,2,3,4,5,6,7,8,9,10', '1,2,3,4,5,6,7,8,9,10']
    """
    if file_is_empty():
        return initialize_table([], False)
    else:
        return read_table()


def update_cache(cache, verbose):
    """
    Writes the content of the cache dict passed as a parameter in the caché.txt file
    :param cache: The cache dict
    :param verbose: The verbose boolean

    Example:
        >>> update_cache({'a': 'b', 'c': 'd'}, True)
        Cache updated
    """
    open('/'.join(os.getcwd().split('/')[:-1]) + '/cache/caché.txt', 'w').truncate(0)
    initialize_table(cache, verbose)


def read_file():
    """
    Open or create the 'cache.txt' file and store its content line by line in a list of strings

    :return: list of strings

    Example:
        >>> read_file()
        ['https://www.google.com', 'https://www.youtube.com']
    """
    file = open_file()
    content = file.readlines()
    file.close()
    return [line.strip() for line in content]


def check_file():
    """
    This function checks if the file 'caché.txt' exists in the directory above the current one.

    :return: True if the file exists, False otherwise.

    Example:
        >>> check_file()
        True
    """
    return os.path.isfile('/'.join(os.getcwd().split('/')[:-1]) + '/cache/caché.txt')


def open_file():
    """
    This function opens the cache file if it exists, if not it creates it.
    It returns the file object.

    Example:
        >>> open_file()
        <_io.TextIOWrapper name='/home/user/cache/caché.txt' mode='r' encoding='UTF-8'>
    """
    if check_file():
        return open('/'.join(os.getcwd().split('/')[:-1]) + '/cache/caché.txt', 'r')
    else:
        file = open('/'.join(os.getcwd().split('/')[:-1]) + '/cache/caché.txt', 'w')
        file.close()
        return open('/'.join(os.getcwd().split('/')[:-1]) + '/cache/caché.txt', 'r+')


def write_file():
    """
    This function opens a file in the cache directory and returns it.
    It is used to store the results of the queries.

    Example:
        >>> write_file()
        <_io.TextIOWrapper name='/home/user/cache/caché.txt' mode='a' encoding='UTF-8'>
    """
    return open('/'.join(os.getcwd().split('/')[:-1]) + '/cache/caché.txt', 'a')


def read_table():
    """
    Reads the table from the file and returns a dictionary with the following structure:
        {
            word: {
                spacy_tag_pattern: {
                    corrected_rae_pos: {
                        phrase_context: {
                            phrase_context_content
                        }
                    }
                }
            }
        }
º
    Example:
        {
            'casa': {
                'DET NOUN ADJ': {
                    'ADJ': {
                        'de Casa Vieja'
                        }
                    }
                }
            }
        }

        It means:
            If the word is 'casa'
            And its pos is 'NOUN'
            And its preceded by a word which pos is 'DET'
            And its proceded by a word which pos is 'ADJ'
            Its corrected pos is 'ADJ'
            Example phrase for this context: 'de Casa Vieja'
    """
    file = read_file()
    header = 0
    cache = {}
    last_line = []
    for line in file:
        if header > 2:
            new_line = list(filter(None, line.replace(' ', '').split('|')))

            if (len(new_line) - 1) > 0:
                # word
                if not new_line[0]:
                    new_line[0] = last_line[0]
                    if (len(new_line) - 1) > 1:
                        # spacy_tag_pattern
                        if not new_line[1]:
                            new_line[1] = last_line[1]
                            if (len(new_line) - 1) > 2:
                                # corrected_rae_pos
                                if not new_line[2]:
                                    new_line[2] = last_line[2]
                                    if (len(new_line) - 1) > 3:
                                        # phrase_context
                                        if not new_line[3]:
                                            new_line[3] = last_line[3]

            cache = load_cache(new_line, cache)
            last_line = new_line

        header += 1

    return cache


def load_cache(columns, cache):
    """
    Loads the cache from the file.

    Parameters:
        columns (list): A list of columns from the file.
        cache (dict): The cache to be loaded.

    Returns:
        cache (dict): The cache loaded from the file.

    Example:
        >>> load_cache(['word', 'spacy_tag_pattern', 'rae_pos', 'phrase_context'], {})

        {'word': {'spacy_tag_pattern': {'rae_pos': 'phrase_context' : {}}}}}
    """
    rae_pos = ''
    spacy_tag_pattern = ''
    if (len(columns) - 1) > 0:
        word = columns[0]
        if (len(columns) - 1) > 1:
            spacy_tag_pattern = columns[1]
            if (len(columns) - 1) > 2:
                rae_pos = columns[2]
                if (len(columns) - 1) > 3:
                    phrase_context = columns[3]
                else:
                    phrase_context = ''
            else:
                rae_pos = ''
        else:
            spacy_tag_pattern = ''
    else:
        word = ''

    try:
        if not cache[word]:
            word_dict = {}
            cache[word] = word_dict
        else:
            word_dict = cache[word]
    except:
        word_dict = {}
        cache[word] = word_dict

    try:
        if not word_dict[spacy_tag_pattern]:
            key_dict = {}
            word_dict[spacy_tag_pattern] = key_dict
        else:
            key_dict = word_dict[spacy_tag_pattern]
    except:
        key_dict = {}
        word_dict[spacy_tag_pattern] = key_dict


    try:
        if isinstance(key_dict[rae_pos], list):
            key_dict[rae_pos].append(phrase_context)
        else:
            key_dict[rae_pos] = [phrase_context]
    except:
        if rae_pos:
            key_dict[rae_pos] = [phrase_context]

    return cache


def file_is_empty():
    """
    This function checks if the file is empty or not.
    It takes no arguments.
    It returns True if the file is empty, False otherwise.

    Example:
        >>> file_is_empty()
        True
    """
    file = open_file()
    content = file.readlines()
    file.close()
    return len(content) == 0


def initialize_table(cache, verbose):
    """

    Initializes the cache table.

    Parameters
    ----------
    cache : list
        A list of lists, where each list is a row in the cache table.
    verbose : bool
        If True, prints the table to the console.
    """
    file = write_file()
    rows = get_rows()
    table = create_table(rows, cache)

    for line in table:

        line += '\n'
        file.write(line.expandtabs(1))
        if verbose:
            print(str(line.replace('\n', '')))

    file.close()


def get_rows():
    """
    This function returns a list of column names for the output  file.

    :return: A list of column names for the output CSV file.

    Example:
        >>> get_rows()

        ['word', 'spacy_tag_pattern', 'corrected_rae_pos', 'phrase_contexts']
    """
    return [
        'word',
        'spacy_tag_pattern',
        'corrected_rae_pos',
        'phrase_contexts'
    ]


def create_row_with_text(list, margin):
    """
    This function creates a row of text with the given list of words.
    The row is created with the given margin.
    The row is returned as a string.

    Example:

        >>> create_row_with_text(['a', 'b', 'c'], 2)

            '| a  | b  | c  |'
    """
    row = '| '

    for word in list:
        spaces = margin - len(word)
        if spaces <= 0:
            spaces = 1
        row += word + (' ' * spaces) + '| '
    row = row[:-1]
    return row


def create_row_decoration(row):
    """
    This function creates a row decoration for a grid.
    A row decoration is a line that separates a row of the grid.
    It consists of '+', '-' and '|'.

    Example:
        >>> create_row_decoration('| a  | b  | c  |')

            '+----+----+----+'

    :param row: A string of '+', '-', and '|' characters.
    :return: A string of '+', '-' and '|' characters.
    """
    decoration = ''
    for row_char in row:
        if row_char == '|':
            decoration += '+'
        else:
            decoration += '-'

    return decoration


def recognize_table(list):
    """
    This function checks if the input list is a table or not.
    It returns True if it is a table, False otherwise.
    A table is defined as a list of strings, where each string contains a '|' character.
    The table can also contain '+' and '-' characters, which are used to define the outer edges of the table.

    Parameters:
        list (list): A list of strings.

    Returns:
        bool: True if the list is a table, False otherwise.

    Examples:
        >>> recognize_table(['|', '|', '|'])
        True
        >>> recognize_table(['+', '|', '+', '|', '+'])
        True
        >>> recognize_table(['+', '|', '+', '|', '+', '|'])
        False
        >>> recognize_table(['+', '|', '+', '|', '+', '|', '+'])
        True
        >>> recognize_table(['+', '|', '+', '|', '+', '|', '+', '|'])
        False
    """
    for line in list:
        if '|' not in line and ('+' not in line or '-' not in line):
            return False
    return True


def clean_list(list):
    """
    This function takes a list as input and returns a new list with the following transformations:
        1. All newlines are removed
        2. All tabs are removed
        3. All pipe characters are removed
        4. All pound signs are removed
        5. All hyphens are removed

    Example:
        Input: ['a\nb', 'c\t', 'd|e']
        Output: ['ab', 'c', 'de']
    """
    return [line.replace('\n', '').replace('\t', '').replace('|', '').replace('#', '').replace('-', '') for line in list]


def get_margin(dict_content):
    """
    This function returns the margin of the longest phrase in the dictionary.
    The margin is the number of characters that should be added to the
    right of the longest phrase in the dictionary in order to make the
    dictionary file look nice.

    Parameters
    ----------
    dict_content : dict
        A dictionary containing the content of the dictionary file.

    Returns
    -------
    margin : int
        The margin of the longest phrase in the dictionary.

    Examples
    --------
        >>> dict_content = {'word': {'spacy_tag_pattern': {'rae_pos': ['phrase1', 'phrase2']}}}
        >>> get_margin(dict_content)
            8

        >>> dict_content = {'word': {'spacy_tag_pattern': {'rae_pos': ['phrase1', 'phrase2', 'phrase3']}}}
        >>> get_margin(dict_content)
            12

        >>> dict_content = {'word': {'spacy_tag_pattern': {'rae_pos': ['phrase1', 'phrase2', 'phrase3', 'phrase4']}}}
        >>> get_margin(dict_content)
            16
    """
    margin = 1

    for word in dict_content:
        word_dict = dict_content[word]
        for spacy_tag_pattern in word_dict:
            key_dict = word_dict[spacy_tag_pattern]
            for rae_pos in key_dict:
                for phrase in key_dict[rae_pos]:
                    if (len(phrase) + 1) > margin:
                        margin = len(phrase) + 1 + (phrase.count('\t') * 4)

    return margin


def create_table(rows_list, dict_content):
    """
    This function creates a table from a list of rows.
        It also takes a dictionary as an argument.
            The dictionary contains the content of the table.
                The keys of the dictionary are the headers of the table.
                The values of the dictionary are the content of the table.

    The function returns a list of rows.
        The first row is the header of the table.
        The second row is the content of the table.
        The third row is the decoration of the table.

    The function also returns a margin.
        The margin is the length of the longest word in the table.

    The function also returns a dictionary.
        The dictionary contains the content of the table.
            The keys of the dictionary are the headers of the table.
            The values of the dictionary are the content of the table.

    Parameters:
        rows_list: A list of rows.
        dict_content: A dictionary of the content of the table.

    Returns:
        table: A list of rows.
        margin: The length of the longest word in the table.
        dict_content: A dictionary of the content of the table.

    Example:
        >>> create_table(['header1', 'header2'], {'header1': 'content1', 'header2': 'content2'})

        [['header1', 'header2'], ['content1', 'content2'], ['--------', '--------']]
    """
    table = []

    if dict_content:
        margin = get_margin(dict_content)
        dict_content_list = parse_dict_to_espacy_cache_format(dict_content, margin)

    else:
        margin = 1
        dict_content_list = []

    rows = create_row_with_text(rows_list, margin)
    decoration = create_row_decoration(rows)

    table.append(decoration)
    table.append(rows)
    table.append(decoration)

    if dict_content_list:
        for element in dict_content_list:

            if not element in table:
                element = element
                table.append(element)

    return table


def clean_rows(rows, margin):
    """
    This function cleans the rows of a table.

    It takes a list of rows, and a margin, and returns a list of cleaned rows.

    The margin is the number of spaces between the columns.

    The function will remove any extra spaces between the columns, and add spaces to the right if needed.

    The function will also remove any extra spaces at the end of the rows.

    The function will also remove any extra spaces at the beginning of the rows.

    Parameters:
        rows (list): A list of rows.
        margin (int): The number of spaces between the columns.

    Returns:
        list: A list of cleaned rows.

    Example:
        >>> clean_rows(['| a | b | c |', '| a | b | c |', '| a | b | c |'], 2)

        ['| a | b | c |', '| a | b | c |', '| a | b | c |']
    """

    cleaned_rows = []

    previous_row = ''

    for line in rows:
        actual_row = list(filter(None, line.replace(' ', '').split('|')))

        new_row = '| '

        if previous_row:
            if actual_row:
                if previous_row[0]:
                    if actual_row[0]:
                        if previous_row[0] == actual_row[0]:
                            new_row += (' ' * margin) + '| '
                        else:
                            new_row += actual_row[0] + (' ' * (margin - len(actual_row[0]))) + '| '
        else:
            # first
            if actual_row:
                new_row += actual_row[0] + (' ' * (margin - len(actual_row[0]))) + '| '

        if previous_row:
            if actual_row:
                if len(previous_row) > 1:
                    if previous_row[1]:
                        if actual_row[1]:
                            if previous_row[1] == actual_row[1]:
                                new_row += (' ' * margin) + '| '
                            else:
                                new_row += actual_row[1] + (' ' * (margin - len(actual_row[1]))) + '| '
        else:
            # First
            if actual_row:
                if len(actual_row) > 1:
                    new_row += actual_row[1] + (' ' * (margin - len(actual_row[1]))) + '| '

        if previous_row:
            if actual_row:
                if len(previous_row) > 2:
                    if previous_row[2]:
                        if actual_row[2]:
                            if previous_row[2] == actual_row[2]:
                                new_row += (' ' * margin) + '| '
                            else:
                                new_row += actual_row[2] + (' ' * (margin - len(actual_row[2]))) + '| '
        else:
            # First
            if actual_row:
                if len(actual_row) > 2:
                    new_row += actual_row[2] + (' ' * (margin - len(actual_row[2]))) + '| '

        if previous_row:
            if actual_row:
                if len(previous_row) > 3:
                    if previous_row[3]:
                        if actual_row[3]:
                            if previous_row[3] == actual_row[3]:
                                new_row += (' ' * margin) + '| '
                            else:
                                new_row += actual_row[3] + (' ' * (margin - len(actual_row[3]))) + '| '
        else:
            # First
            if actual_row:
                if len(actual_row) > 3:
                    new_row += actual_row[3] + (' ' * (margin - len(actual_row[0]))) + '| '

        cleaned_rows.append(new_row[:-1])

        previous_row = actual_row

    return cleaned_rows


def parse_dict_to_espacy_cache_format(dict_content, margin):
    """
    This function takes a dictionary of the form:
    {
        "word": {
            "spacy_tag_pattern": {
                "rae_pos": [
                    "phrase"
                ]
            }
        }
    }
    and returns a list of rows, where each row is a list of strings.
    The first row is a header row, and the rest are rows of data.
    The data rows are created by iterating through the dictionary,
    and creating a row for each word, spacy_tag_pattern, rae_pos, phrase
    combination.
    The margin is the number of spaces to add to the left of each row.
    The function returns a list of rows, where each row is a list of strings.

    Example:

    dict_content = {
        "word": {
            "spacy_tag_pattern": {
                "rae_pos": [
                    "phrase"
                ]
            }
        }
    }

    margin = 2

    parse_dict_to_espacy_cache_format(dict_content, margin)

    returns:

    [
        [
            "word",
            "spacy_tag_pattern",
            "rae_pos",
            "phrase"
        ],
        [
            "  word",
            "spacy_tag_pattern",
            "rae_pos",
            "phrase"
        ]
    ]
    """
    rows = []
    for word in dict_content:
        word_dict = dict_content[word]
        for spacy_tag_pattern in word_dict:
            key_dict = word_dict[spacy_tag_pattern]
            for rae_pos in key_dict:
                for phrase in key_dict[rae_pos]:
                    if not create_row_with_text([word, spacy_tag_pattern, rae_pos, phrase], margin) in rows:
                        rows.append(create_row_with_text([word, spacy_tag_pattern, rae_pos, phrase], margin))


    return clean_rows(rows, margin)

