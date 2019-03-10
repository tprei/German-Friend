from bs4 import BeautifulSoup as sp
import requests
import argparse

languages = {
    'en': 'english',
    'de': 'german',
    'fr': 'french',
    'pt': 'portuguese',
    'ru': 'russian',
    'it': 'italian',
    'es': 'spanish'
}

# raised when user inputs two equal languages (the one to be translated from and the one to be translated to
class ArgumentError(Exception):
    def __str__(self):
        return f'Sorry, input and output languages have to be different from each other.'

# raised when user inputs a wrong language code or one that doesnt exist in the languages dict
class InputError(Exception):
    def __init__(self, lang):
        self.lang = lang

    def __str__(self):
        return f'Sorry, {self.lang} is not an accepted language. Available languages are:\n{languages}\n Remember to use language codes in the input)'

# dict.cc lookup class
class Query:

    # format: input_language output_language word_to_be_translated
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('input_lang', type=str, help = 'Language to be translated from')
        parser.add_argument('output_lang', type=str, help = 'Language to be translated to')
        parser.add_argument('word', type=str, help = 'Word to be translated') 
        args = parser.parse_args()
        
        if args.input_lang == args.output_lang:
            raise ArgumentError
        if (args.input_lang not in languages):
            raise InputError(args.input_lang)
        if (args.output_lang not in languages):
            raise InputError(args.output_lang)
         
        self.input = args.input_lang
        self.output = args.output_lang
        self.word = args.word

    # making html request that is yet to be parsed. The object info is: (input-language, output-language, word)
    def make_request(self): 
        url = f'https://{self.input}-{self.output}.dict.cc/?s={self.word}'
        r = requests.get(url)
        print(url)


if __name__ == '__main__':
    input_query = Query()
    input_query.make_request()
 
