# ┌───────────────────────────────────────────┐
# │ Sample code to generate a dictionary file │
# └───────────────────────────────────────────┘
# import json
# target_len_words = set()
# with open('./words_dictionary.json', 'r') as f:
#     wordlist = json.load(f)
# for word in wordlist:
#     if len(word) == TERMLE_LEN:
#         target_len_words.add(word)

# print("Current Dictionary Length: ", len(target_len_words))
# with open('dictionary.json', 'w') as w:
#     json.dump(list(target_len_words), w)
