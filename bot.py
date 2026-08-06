import os
import telebot
import re
from collections import Counter

# Get token from environment variable
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ ERROR: TELEGRAM_BOT_TOKEN environment variable not set!")
    print("Please set it in Railway Dashboard → Variables")
    exit(1)

print("✅ Bot token found! Starting bot...")

bot = telebot.TeleBot(BOT_TOKEN)

# Analysis functions
def count_words(text):
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def count_characters(text):
    return len(text)

def count_sentences(text):
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip()]
    return len(sentences)

def count_syllables(text):
    vowels = 'aeiouy'
    words = re.findall(r'\b\w+\b', text.lower())
    syllable_count = 0
    for word in words:
        if word.endswith('e'):
            word = word[:-1]
        count = 0
        in_vowel_group = False
        for char in word:
            if char in vowels:
                if not in_vowel_group:
                    count += 1
                    in_vowel_group = True
            else:
                in_vowel_group = False
        syllable_count += max(1, count)
    return syllable_count

def count_unique_words(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return len(set(words))

def get_repeated_words(text):
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    return {word: count for word, count in word_counts.items() if count > 1}

# Command handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """
📊 Welcome to the Text Analysis Bot!

Commands:
/word_count - Count words
/character_count - Count characters  
/sentence_count - Count sentences
/syllable_count - Count syllables
/unique_word_count - Count unique words
/repeated_words - Show repeated words
/full_analysis - Complete analysis

Example: /word_count Hello world!
""")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, """
📋 Available Commands:

/word_count - Count words
/character_count - Count characters
/sentence_count - Count sentences
/syllable_count - Count syllables
/unique_word_count - Count unique words
/repeated_words - Show repeated words
/full_analysis - Complete text analysis

Usage: /command Your text here
Example: /word_count This is a test.
""")

@bot.message_handler(commands=['word_count'])
def word_count(message):
    text = message.text.replace('/word_count', '', 1).strip()
    if not text:
        bot.reply_to(message, "❌ Please provide text.\nExample: /word_count Hello world!")
        return
    count = count_words(text)
    bot.reply_to(message, f"📝 Word Count: {count}")

@bot.message_handler(commands=['character_count'])
def character_count(message):
    text = message.text.replace('/character_count', '', 1).strip()
    if not text:
        bot.reply_to(message, "❌ Please provide text.\nExample: /character_count Hello world!")
        return
    count = count_characters(text)
    bot.reply_to(message, f"🔠 Character Count: {count}")

@bot.message_handler(commands=['sentence_count'])
def sentence_count(message):
    text = message.text.replace('/sentence_count', '', 1).strip()
    if not text:
        bot.reply_to(message, "❌ Please provide text.\nExample: /sentence_count Hello world!")
        return
    count = count_sentences(text)
    bot.reply_to(message, f"📄 Sentence Count: {count}")

@bot.message_handler(commands=['syllable_count'])
def syllable_count(message):
    text = message.text.replace('/syllable_count', '', 1).strip()
    if not text:
        bot.reply_to(message, "❌ Please provide text.\nExample: /syllable_count Hello world!")
        return
    count = count_syllables(text)
    bot.reply_to(message, f"🔣 Syllable Count: {count}")

@bot.message_handler(commands=['unique_word_count'])
def unique_word_count(message):
    text = message.text.replace('/unique_word_count', '', 1).strip()
    if not text:
        bot.reply_to(message, "❌ Please provide text.\nExample: /unique_word_count Hello world!")
        return
    count = count_unique_words(text)
    bot.reply_to(message, f"🌟 Unique Word Count: {count}")

@bot.message_handler(commands=['repeated_words'])
def repeated_words(message):
    text = message.text.replace('/repeated_words', '', 1).strip()
    if not text:
        bot.reply_to(message, "❌ Please provide text.\nExample: /repeated_words Hello world!")
        return
    repeated = get_repeated_words(text)
    if not repeated:
        bot.reply_to(message, "♾️ No repeated words found.")
        return
    result = "♾️ Repeated Words:\n"
    for word, count in repeated.items():
        result += f"  • {word}: {count} times\n"
    bot.reply_to(message, result)

@bot.message_handler(commands=['full_analysis'])
def full_analysis(message):
    text = message.text.replace('/full_analysis', '', 1).strip()
    if not text:
        bot.reply_to(message, "❌ Please provide text.\nExample: /full_analysis Hello world!")
        return
    
    result = "📊 Full Text Analysis\n"
    result += "─" * 20 + "\n"
    result += f"📝 Words: {count_words(text)}\n"
    result += f"🔠 Characters: {count_characters(text)}\n"
    result += f"📄 Sentences: {count_sentences(text)}\n"
    result += f"🔣 Syllables: {count_syllables(text)}\n"
    result += f"🌟 Unique Words: {count_unique_words(text)}\n"
    
    repeated = get_repeated_words(text)
    if repeated:
        result += "\n♾️ Repeated Words:\n"
        for word, count in repeated.items():
            result += f"  • {word}: {count} times\n"
    
    bot.reply_to(message, result)

# Handle any other message
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, """
🤖 Use commands to analyze text!

/start - Show welcome
/help - Show commands
/word_count - Count words
/character_count - Count characters
/full_analysis - Complete analysis

Example: /word_count Hello world!
""")

print("🚀 Bot is running and polling...")
bot.polling()
