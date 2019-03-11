# German Friend
## A Telegram bot to help you with the everyday ~~German~~ translating struggle.

Okay, so. I've never really made any Telegram bots, this is a first for me.
So yea, this may be *really bad*. 

The idea behind it came when I was struggling to read a book in German and I wanted to do something else. So the next day I decided I was going to make a Telegram bot in under 24 hours. This monstruosity is the final product (or at least the alpha? hehe)

This bot **does not translate words/sentences**. It looks them up in a dictionary. 

### How to install:

I highly recommend doing this in a virtualenv:
- if you're on Windows, run:

```
pip install -r requirements.txt
```
- if you're on Linux/MacOS, run:
```
pip3 install -r requirements.txt
```

### Commands implemented so far:

- start: just pings the bot to check if it's running
- help: shows help
- lookup: looks up a word or phrase in dictcc

### TODO

- something with images would be nice.
- cleaner GUI
- known bug that i havent fixed yet: strings are literally parsed. So a single word with single quotation marks won't be a good query
- maybe try a different translating method, a good API would be cool...
- files that only have one occurrence are useless.
