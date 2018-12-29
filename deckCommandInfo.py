import itertools

# Sorted mana costs


manaCostDictionary = {}
for i in range (0, 21):
    try:
        with open("textCardDatabase/"+str(i)+"manas.txt") as f:
            cards = f.readlines()
            cards = [x.strip() for x in cards]
            manaCostDictionary[int("{}".format(i))] = cards
        f.close()
    except FileNotFoundError:
        None


# Card copies IDs

with open("textCardDatabase/"+"cardCopiesIDs.txt") as f:
    cardCopiesIDsList = f.readlines()
cardCopiesIDsList = [x.strip() for x in cardCopiesIDsList] # Removes lines like \n
cardCopiesIDsDictionary = dict(itertools.zip_longest(*[iter(cardCopiesIDsList)] * 2, fillvalue="")) # Turns list into dictionary
cardCopiesIDsDictionary = {v: k for k, v in cardCopiesIDsDictionary.items()} # Inverts dictionary
f.close()


# Card IDs

with open("textCardDatabase/"+"cardIDs.txt") as f:
    cardIDsList = f.readlines()
cardIDsList = [x.strip() for x in cardIDsList]
cardIDsDictionary = dict(itertools.zip_longest(*[iter(cardIDsList)] * 2, fillvalue=""))
cardIDsDictionary = {v: k for k, v in cardIDsDictionary.items()}
f.close()
