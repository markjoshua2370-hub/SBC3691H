from analysis import (
    count_words, count_characters, count_sentences, count_syllables,
    count_unique_words, get_repeated_words, get_nouns, get_verbs,
    get_adjectives, get_adverbs, full_analysis
)

def start_message():
    """Welcome message for /start command."""
    return """
📊 Welcome to the Text Analysis Bot!

This bot can analyze your text messages and provide detailed statistics.

Available commands:
/start - Show this welcome message
/help - Display available commands
/word_count - Count the number of words
/character_count - Count the number of characters
/sentence_count - Count the number of sentences
/syllable_count - Count the number of syllables
/unique_word_count - Count unique words
/repeated_words - Show repeated words
/nouns - Extract nouns
/verbs - Extract verbs
/adjectives - Extract adjectives
/adverbs - Extract adverbs
/full_analysis - Get a complete analysis of the message

Just send any command followed by the text you want to analyze:
Example: /word_count Hello world!
"""

def help_message():
    """Help message for /help command."""
    return """
📋 Available Commands:

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

Usage: Send command followed by text
Example: /word_count This is a sample text.
"""

def handle_word_count(text):
    """Handler for /word_count command."""
    if not text:
        return "📝 Please provide text to count words.\nExample: /word_count This is a test."
    count = count_words(text)
    return f"📝 **Word Count:** {count}"

def handle_character_count(text):
    """Handler for /character_count command."""
    if not text:
        return "🔠 Please provide text to count characters.\nExample: /character_count This is a test."
    count = count_characters(text)
    return f"🔠 **Character Count:** {count}"

def handle_sentence_count(text):
    """Handler for /sentence_count command."""
    if not text:
        return "📄 Please provide text to count sentences.\nExample: /sentence_count This is a test. This is another sentence."
    count = count_sentences(text)
    return f"📄 **Sentence Count:** {count}"

def handle_syllable_count(text):
    """Handler for /syllable_count command."""
    if not text:
        return "🔣 Please provide text to count syllables.\nExample: /syllable_count This is a test."
    count = count_syllables(text)
    return f"🔣 **Syllable Count:** {count}"

def handle_unique_word_count(text):
    """Handler for /unique_word_count command."""
    if not text:
        return "🌟 Please provide text to count unique words.\nExample: /unique_word_count This is a test test."
    count = count_unique_words(text)
    return f"🌟 **Unique Word Count:** {count}"

def handle_repeated_words(text):
    """Handler for /repeated_words command."""
    if not text:
        return "♾️ Please provide text to find repeated words.\nExample: /repeated_words This is a test test."
    repeated = get_repeated_words(text)
    if not repeated:
        return "♾️ No repeated words found."
    result = "♾️ **Repeated Words:**\n"
    for word, count in repeated.items():
        result += f"  • {word}: {count} times\n"
    return result

def handle_nouns(text):
    """Handler for /nouns command."""
    if not text:
        return "👑 Please provide text to extract nouns.\nExample: /nouns The information about the situation is important."
    nouns = get_nouns(text)
    if not nouns:
        return "👑 No nouns found."
    return f"👑 **Nouns:**\n" + "\n".join(f"  • {noun}" for noun in nouns)

def handle_verbs(text):
    """Handler for /verbs command."""
    if not text:
        return "🏃 Please provide text to extract verbs.\nExample: /verbs The player scored the goal."
    verbs = get_verbs(text)
    if not verbs:
        return "🏃 No verbs found."
    return f"🏃 **Verbs:**\n" + "\n".join(f"  • {verb}" for verb in verbs)

def handle_adjectives(text):
    """Handler for /adjectives command."""
    if not text:
        return "☁️ Please provide text to extract adjectives.\nExample: /adjectives The courageous team played well."
    adjectives = get_adjectives(text)
    if not adjectives:
        return "☁️ No adjectives found."
    return f"☁️ **Adjectives:**\n" + "\n".join(f"  • {adj}" for adj in adjectives)

def handle_adverbs(text):
    """Handler for /adverbs command."""
    if not text:
        return "💨 Please provide text to extract adverbs.\nExample: /adverbs The team played brilliantly."
    adverbs = get_adverbs(text)
    if not adverbs:
        return "💨 No adverbs found."
    return f"💨 **Adverbs:**\n" + "\n".join(f"  • {adv}" for adv in adverbs)

def handle_full_analysis(text):
    """Handler for /full_analysis command."""
    if not text:
        return "🔍 Please provide text for full analysis.\nExample: /full_analysis This is a test message."
    analysis = full_analysis(text)
    
    result = "📊 **Full Text Analysis**\n\n"
    result += f"📝 Words: {analysis['word_count']}\n"
    result += f"🔠 Characters: {analysis['character_count']}\n"
    result += f"📄 Sentences: {analysis['sentence_count']}\n"
    result += f"🔣 Syllables: {analysis['syllable_count']}\n"
    result += f"🌟 Unique Words: {analysis['unique_word_count']}\n"
    
    if analysis['repeated_words']:
        result += "\n♾️ **Repeated Words:**\n"
        for word, count in analysis['repeated_words'].items():
            result += f"  • {word}: {count} times\n"
    
    if analysis['nouns']:
        result += "\n👑 **Nouns:**\n" + "\n".join(f"  • {noun}" for noun in analysis['nouns'])
    
    if analysis['verbs']:
        result += "\n\n🏃 **Verbs:**\n" + "\n".join(f"  • {verb}" for verb in analysis['verbs'])
    
    if analysis['adjectives']:
        result += "\n\n☁️ **Adjectives:**\n" + "\n".join(f"  • {adj}" for adj in analysis['adjectives'])
    
    if analysis['adverbs']:
        result += "\n\n💨 **Adverbs:**\n" + "\n".join(f"  • {adv}" for adv in analysis['adverbs'])
    
    return result
