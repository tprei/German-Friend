from bs4 import BeautifulSoup as sp
import re
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
        # html request
        url = f'https://{self.input}{self.output}.dict.cc/?s={self.word}'
        r = requests.get(url, headers={'User-agent': 'Chrome/72.0.3626.121'})

        # parsing stuff
        soup = sp(r.text, 'html.parser')
        results = soup.findAll('tr', id = re.compile('^tr'))

        if(soup.title.text == 'Sorry!'):
            print('This language pair is not supported at the moment.')
            return

        # in case nothing was found
        if(len(results) == 0):
            print('No results found for that word.')
            return
        
        # parsing field from the left (input-lang) and the right (output-lang) to be displayed correctly
        if(self.input == 'de'):
            print(f'{self.output}{60*" "}{self.input}')
        else:
            print(f'{self.input}{60*" "}{self.output}')
        for result in results[:25]:
            text_results = result.findAll('td', {'class': 'td7nl'})
            input_field = text_results[0].findAll('a')
            output_field = text_results[1].findAll('a')
            
            # making things more readable
            inplen = 0
            for text_field in input_field:
                print(f'{text_field.text.strip()} ', end='')
                inplen+=len(text_field.text)+1

            print((60-inplen)*'.', end=' ')
            
            for text_field in output_field:
                print(f'{text_field.text.strip()} ', end='')

            print('')
            try:
                if(not result.next_sibling.next_sibling.has_attr('id')):
                    print('\n' + result.next_sibling.next_sibling.text)
                    print(60*'_'+'\n')
            except:
                continue


if __name__ == '__main__':
    input_query = Query()
    input_query.make_request()
 
