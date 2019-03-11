import time
import logging
import dict
import telebot
from telebot import util

btoken = 'my_token'
bot = telebot.AsyncTeleBot(token = btoken)

help_msg = """Hi, I'm the *German Friend Bot*. 
I'm a simple bot that's designed for looking up words in other languages
(*mainly German*, since I use the `dict.cc` website for my lookups).

If you'd like to lookup a word, just type:
`/lookup <input_lang> <output_lang> <word>`

Where,
`<input_lang>` is the language you'd like to translate *from*
`<output_lang>` is the language you'd like to translate *to*
`<word>` is the word itself (you can also input a phrase, but you gotta use quotation marks around it, like this: 'this is a phrase' ).

and `<input_lang>, <output_lang>` must be one of the following codes:

```
German: de
English: en
French: fr
Italian: it
Portuguese: pt
Russian: ru
```
Keep in mind not all pairs are possible since dict.cc hasn't yet made them all available.

"""

bad_request = """
The query was *unsucessful*.
Maybe you used the wrong formatting.

To /lookup, use the following format:
`/lookup <input_lang> <output_lang> <word>`

Where,
`<input_lang>` is the language you'd like to translate *from*
`<output_lang>` is the language you'd like to translate *to*
`<word>` is the word itself.

PS: <input_lang> and <output_lang> *must* be different.
"""

def clear_files():
    with open('first_result.txt', 'w+') as f:
        f.write('')
    with open('query.txt', 'w+') as f:
        f.write('')
    return

@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.reply_to(msg, 'Hey! I\'m over here')
    
@bot.message_handler(commands=['help'])
def helpm(msg):
    bot.reply_to(msg, help_msg, parse_mode = 'Markdown')

@bot.message_handler(commands=['lookup'])
def lookup(msg):

    clear_files()

    #arguments = list['/lookup', 'input_lang', 'output_lang', 'word']
    arguments = msg.text.split(' ', 3)
    
    if len(arguments) < 4:
        bot.send_message(msg.chat.id, 'Wrong formatting, see /help for more information on the /lookup command')
        return

    arguments = list((x.strip() for x in arguments))

    if arguments[1] == arguments[2]:
        bot.send_message(msg.chat.id, '<input_lang> and <output_lang> must be different')
    elif isinstance(arguments[1], str) and len(arguments[1]) == 2 and isinstance(arguments[2], str) and len(arguments[2]) == 2:
        lookup_query = dict.Query(arguments[1], arguments[2], arguments[3])
        try:
            lookup_query.make_request()
        except dict.QueryError:
            bot.send_message(msg.chat.id, 'There were no results for that query.')
        except dict.PairError:
            bot.send_message(msg.chat.id, 'Sorry, this language pair is yet not available in dict.cc')
        finally:
            text = open('first_result.txt', 'rb').read()
            bot.send_message(msg.chat.id, text)
            details = open('query.txt', 'rb')
            bot.send_document(msg.chat.id, details)
    else:
        bot.send_message(msg.chat.id, 'The languages in the /lookup command must be a two-character code, see /help for more information.')
        

bot.polling(none_stop=False, interval=0, timeout=20)
