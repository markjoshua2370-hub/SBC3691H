import telebot
from config import BOT_TOKEN
from commands import (
    start_message, help_message,
    handle_word_count, handle_character_count, handle_sentence_count,
    handle_syllable_count, handle_unique_word_count, handle_repeated_words,
    handle_nouns, handle_verbs, handle_adjectives, handle_adverbs,
    handle_full_analysis
)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, start_message())

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, help_message())

@bot.message_handler(commands=['word_count'])
def word_count(message):
    text = message.text.replace('/word_count', '', 1).strip()
    bot.reply_to(message, handle_word_count(text))

@bot.message_handler(commands=['character_count'])
def character_count(message):
    text = message.text.replace('/character_count', '', 1).strip()
    bot.reply_to(message, handle_character_count(text))

@bot.message_handler(commands=['sentence_count'])
def sentence_count(message):
    text = message.text.replace('/sentence_count', '', 1).strip()
    bot.reply_to(message, handle_sentence_count(text))

@bot.message_handler(commands=['syllable_count'])
def syllable_count(message):
    text = message.text.replace('/syllable_count', '', 1).strip()
    bot.reply_to(message, handle_syllable_count(text))

@bot.message_handler(commands=['unique_word_count'])
def unique_word_count(message):
    text = message.text.replace('/unique_word_count', '', 1).strip()
    bot.reply_to(message, handle_unique_word_count(text))

@bot.message_handler(commands=['repeated_words'])
def repeated_words(message):
    text = message.text.replace('/repeated_words', '', 1).strip()
    bot.reply_to(message, handle_repeated_words(text))

@bot.message_handler(commands=['nouns'])
def nouns(message):
    text = message.text.replace('/nouns', '', 1).strip()
    bot.reply_to(message, handle_nouns(text))

@bot.message_handler(commands=['verbs'])
def verbs(message):
    text = message.text.replace('/verbs', '', 1).strip()
    bot.reply_to(message, handle_verbs(text))

@bot.message_handler(commands=['adjectives'])
def adjectives(message):
    text = message.text.replace('/adjectives', '', 1).strip()
    bot.reply_to(message, handle_adjectives(text))

@bot.message_handler(commands=['adverbs'])
def adverbs(message):
    text = message.text.replace('/adverbs', '', 1).strip()
    bot.reply_to(message, handle_adverbs(text))

@bot.message_handler(commands=['full_analysis'])
def full_analysis(message):
    text = message.text.replace('/full_analysis', '', 1).strip()
    bot.reply_to(message, handle_full_analysis(text))

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, """
I can analyze text for you! Use one of these commands:

/word_count - Count words
/character_count - Count characters
/sentence_count - Count sentences
/syllable_count - Count syllables
/unique_word_count - Count unique words
/repeated_words - Show repeated words
/nouns - Extract nouns
/verbs - Extract verbs
/adjectives - Extract adjectives
/adverbs - Extract adverbs
/full_analysis - Complete text analysis

Example: /word_count Hello world!
""")

print("Bot is starting...")
bot.polling()
