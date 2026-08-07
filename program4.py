pg = input("Enter a paragraph: ")

punctuation = ".,!?;:'\"()-[]{}<>/\\@#$%^&*_+=|`~"

clean_text = ""
for ch in pg:
    if ch not in punctuation:
        clean_text += ch
    else:
        clean_text += " "

print("\nParagraph without punctuation:")
print(clean_text)

words = clean_text.split()

word_list = []
for word in words:
    word_list.append(word.lower())

print("\n1. Total number of words:", len(word_list))

unique_words = []
for word in word_list:
    if word not in unique_words:
        unique_words.append(word)

print("2. Number of unique words:", len(unique_words))

max_len = len(word_list[0])
for word in word_list:
    if len(word) > max_len:
        max_len = len(word)

print("3. Longest word(s):")
for word in unique_words:
    if len(word) == max_len:
        print(word)

min_len = len(word_list[0])
for word in word_list:
    if len(word) < min_len:
        min_len = len(word)

print("4. Shortest word(s):")
for word in unique_words:
    if len(word) == min_len:
        print(word)

print("5. Words appearing more than once:")
found = False
for word in unique_words:
    count = 0
    for w in word_list:
        if word == w:
            count += 1
    if count > 1:
        print(word, "->", count, "times")
        found = True

if not found:
    print("No repeated words")

sorted_words = sorted(unique_words)
print("\nWords in alphabetical order:")
for word in sorted_words:
    print(word)

search = input("\nEnter a word to search: ").lower()

positions = []
for i in range(len(word_list)):
    if word_list[i] == search:
        positions.append(i)

if positions:
    print("Word found at positions:", positions)
else:
    print("Word not found.")