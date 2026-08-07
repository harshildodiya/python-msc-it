para = input("Enter a paragraph: ")

words = para.split()
unique = set(words)
longest = max(words, key=len)
shortest = min(words, key=len)

print("\n Words in the paragraph:")
print(words)
print("\n Total number of words:", len(words))
print("Number of unique words:",unique)

print("Longest word:", longest)

print("Shortest word:", shortest)
duplicate = []
for word in unique:
    if words.count(word) > 1:
        duplicate.append(word)
print("Words more than once:", duplicate)
alphabetical = sorted(words)
print("Words in alphabetical order:",alphabetical)