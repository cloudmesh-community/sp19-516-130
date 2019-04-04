
http://norvig.com/spell-correct.html

https://ai.googleblog.com/2006/08/all-our-n-gram-are-belong-to-you.html

https://www.clips.uantwerpen.be/pages/pattern-en#parser

http://norvig.com/mayzner.html



import ngram
ngram.NGram.compare('beef','beaf',N=1)


import nltk
nltk.edit_distance("humpty", "dumpty")


import difflib
a = 'Thanks for calling America Expansion'
b = 'Thanks for calling American Express'
seq = difflib.SequenceMatcher(None,a,b)
d = seq.ratio()*100
print(d)





import re
from collections import Counter
def words(text): return re.findall(r'\w+', text.lower())
def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N
def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)
def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])
def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)
def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)
def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
correction('speling')




https://github.com/norvig/pytudes/blob/master/py/spell.py

https://github.com/norvig/pytudes/blob/master/py/lettercount.py

https://github.com/phatpiglet/autocorrect

https://github.com/mattalcock/blog/blob/master/2012/12/5/python-spell-checker.rst

https://datascience.blog.wzb.eu/2016/07/13/autocorrecting-misspelled-words-in-python-using-hunspell/

http://scottlobdell.me/2015/02/writing-autocomplete-engine-scratch-python/

https://www.kaggle.com/cpmpml/spell-checker-using-word2vec

https://stackoverflow.com/questions/13928155/spell-checker-for-python

https://www.kaggle.com/c/spell-checker-nyu-cds/data

https://www.kaggle.com/reppic/toxic-comment-spell-checked-data/data

https://www.kaggle.com/hajkgriroryan/spell-py

