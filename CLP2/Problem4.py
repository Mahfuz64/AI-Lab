def count_word_occurrences(text):
    words = text.lower().split()  
    word_count = {}

    for word in words:
        word = word.strip(".,!?")  

        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count

text = "This is a sample text. This text is just a sample."
print(count_word_occurrences(text))