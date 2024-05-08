
__author__ = 'Ricardo'
__version__ = '0.1'


def load_prompt_file(prompt_file_path:str):

    prompt_file_path = prompt_file_path
    template = ''

    with open(prompt_file_path, 'r', encoding="utf-8") as archivo:
        template = archivo.read()

    return template
