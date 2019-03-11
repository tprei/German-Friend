from bs4 import BeautifulSoup as sp
import re
import requests
import argparse

with open('query.txt', 'w+') as f:
    pass
with open('first_result.txt', 'w+'):
    pass

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

class QueryError(Exception):
    def __str__(self):
        return f'Sorry, couldn\'t find any results'

class PairError(Exception):
    def __str__(self):
        return f'Sorry, this language pair is not yet available'

# dict.cc lookup class
class Query:

    # format: input_language output_language word_to_be_translated (this function is used with the command line arguments)
    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('input_lang', type=str, help = 'Language to be translated from')
        parser.add_argument('output_lang', type=str, help = 'Language to be translated to')
        parser.add_argument('word', type=str, help = 'Word to be translated') 
        args = parser.parse_args()
        
        if args.input_lang == args.output_lang:
            raise ArgumentError
        if args.input_lang not in languages:
            raise InputError(args.input_lang)
        if args.output_lang not in languages:
            raise InputError(args.output_lang)
         
        self.input = args.input_lang
        self.output = args.output_lang
        self.word = args.word
    
    # class constructor (works just like the parse_args func, but you gotta input the data as arguments and not through command line)
    def __init__(self, input_lang, output_lang, word): 
        self.input = input_lang
        self.output = output_lang
        self.word = word

    # making html request that is yet to be parsed. The object info is: (input-language, output-language, word)
    def make_request(self): 
        # html request
        url = f'https://{self.input}{self.output}.dict.cc/?s={self.word}'
        r = requests.get(url, headers={'User-agent': 'Chrome/72.0.3626.121'})

        # parsing stuff
        soup = sp(r.text, 'html.parser')
        results = soup.findAll('tr', id = re.compile('^tr'))

        # in case dict cc doesnt support this pair
        if soup.title.text == 'Sorry!':
            raise PairError

        # in case nothing was found
        if len(results) == 0:
            raise QueryError

        # parsing field from the left (input-lang) and the right (output-lang) to be displayed correctly
        if self.input == 'de':
            with open('query.txt', 'a') as f:
                f.write(f'{self.output}{60*" "}{self.input}\n')
        else:
            with open('query.txt', 'a') as f:
                f.write(f'{self.input}{60*" "}{self.output}\n')

        for result in results[:30]:
            text_results = result.findAll('td', {'class': 'td7nl'})
            input_field = text_results[0].findAll('a')
            output_field = text_results[1].findAll('a')

            if result == results[0]:
                for text_field in input_field:
                    with open('first_result.txt', 'a') as f2:
                        f2.write(f'{text_field.text.strip() }')
                with open('first_result.txt', 'a') as f2:
                    f2.write('\n==\n')

                for text_field in output_field:
                    with open('first_result.txt', 'a') as f2:
                        f2.write(f'{text_field.text.strip() }')

            # making things more readable
            inplen = 0
            for text_field in input_field:
                with open('query.txt', 'a') as f:
                    f.write(f'{text_field.text.strip()} ')
                inplen+=len(text_field.text)+1

            with open('query.txt', 'a') as f:
                f.write((60-inplen)*'.' + ' ')
            
            for text_field in output_field:
                with open('query.txt', 'a') as f:
                    f.write(f'{text_field.text.strip()} ')

            with open('query.txt', 'a') as f:
                f.write('\n')
            try:
                if not result.next_sibling.next_sibling.has_attr('id'):
                    with open('query.txt', 'a') as f:
                        f.write('\n' + result.next_sibling.next_sibling.text + '\n')
                        f.write(60*'_'+'\n'+'\n')
            except:
                continue
 
