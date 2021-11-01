def mid(word):
    r=len(word)%2
    if r==1:
        l=round(len(word)/2)
        return word[l-1:-(l-1)]
    else:
        return(" ")
print(mid("lav"))