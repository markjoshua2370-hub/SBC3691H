import re
from collections import Counter

def count_words(text):
    """Counts the total number of words in a message."""
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def count_characters(text):
    """Counts the total number of characters."""
    return len(text)

def count_sentences(text):
    """Identifies the number of sentences."""
    sentences = re.split(r'[.!?]+', text)
    # Remove empty strings and strip whitespace
    sentences = [s for s in sentences if s.strip()]
    return len(sentences) if len(sentences) > 1 else 0

def count_syllables(text):
    """Counts syllables based on vowel patterns."""
    vowels = 'aeiouy'
    words = re.findall(r'\b\w+\b', text.lower())
    syllable_count = 0
    for word in words:
        # Remove common silent e
        if word.endswith('e'):
            word = word[:-1]
        # Count vowel groups
        count = 0
        in_vowel_group = False
        for char in word:
            if char in vowels:
                if not in_vowel_group:
                    count += 1
                    in_vowel_group = True
            else:
                in_vowel_group = False
        syllable_count += max(1, count)  # Each word has at least 1 syllable
    return syllable_count

def count_unique_words(text):
    """Counts unique words."""
    words = re.findall(r'\b\w+\b', text.lower())
    return len(set(words))

def get_repeated_words(text):
    """Shows repeated words."""
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    return {word: count for word, count in word_counts.items() if count > 1}

def get_nouns(text):
    """Extracts nouns (simplified - words ending in common noun suffixes)."""
    words = re.findall(r'\b\w+\b', text.lower())
    noun_suffixes = ['tion', 'sion', 'ment', 'ness', 'ity', 'ism', 'ist', 'tion', 'ance', 'ence', 'ing', 'tion', 'sion']
    nouns = []
    for word in words:
        for suffix in noun_suffixes:
            if word.endswith(suffix) and len(word) > 3:
                nouns.append(word)
                break
    return list(set(nouns))

def get_verbs(text):
    """Extracts verbs (simplified - words ending in common verb suffixes)."""
    words = re.findall(r'\b\w+\b', text.lower())
    verb_suffixes = ['ed', 'es', 'ing']
    verbs = []
    for word in words:
        for suffix in verb_suffixes:
            if word.endswith(suffix) and len(word) > 3:
                verbs.append(word)
                break
    return list(set(verbs))

def get_adjectives(text):
    """Extracts adjectives (simplified - words ending in 'ous')."""
    words = re.findall(r'\b\w+\b', text.lower())
    adjectives = []
    for word in words:
        if word.endswith('ous') and len(word) > 4:
            adjectives.append(word)
    return list(set(adjectives))

def get_adverbs(text):
    """Extracts adverbs (simplified - words ending in 'ly')."""
    words = re.findall(r'\b\w+\b', text.lower())
    adverbs = []
    for word in words:
        if word.endswith('ly') and len(word) > 3:
            adverbs.append(word)
    return list(set(adverbs))

def full_analysis(text):
    """Provides a complete breakdown of the message."""
    return {
        'word_count': count_words(text),
        'character_count': count_characters(text),
        'sentence_count': count_sentences(text),
        'syllable_count': count_syllables(text),
        'unique_word_count': count_unique_words(text),
        'repeated_words': get_repeated_words(text),
        'nouns': get_nouns(text),
        'verbs': get_verbs(text),
        'adjectives': get_adjectives(text),
        'adverbs': get_adverbs(text)
}
