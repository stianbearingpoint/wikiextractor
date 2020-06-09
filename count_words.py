import os
import json
import re
from collections import Counter, OrderedDict
from itertools import chain

def get_words(filename):
    word_regex = r'[A-Za-zøæåÆØÅ]+'
    capitalized_regex = r'(\.|^|<|"|\'|\(|\[|\{)\s*' + word_regex
    with open(filename, encoding="utf8") as file:
        for line in file:
            line = re.sub(capitalized_regex, '', line)
            for word in re.findall(word_regex, line):
                yield word.lower()


def count_words(words, out_filename='norwegian_word_count.json'):
    
    counts = Counter(words)
    # make output file human readable
    counts_list = list(counts.items())
    counts_list.sort(key=lambda i: counts[i[0]], reverse=True)
    counts_ord_dict = OrderedDict(counts_list)
    with open(out_filename, 'w') as outfile:
        json.dump(counts_ord_dict, outfile, indent=4)

if __name__ == "__main__":
    rootdir = 'output'
    counter = 0
    all_words_generator = None
    for subdir, dirs, files in os.walk(rootdir):
        for f in files:
            filename = os.path.join(subdir, f)
            counter += 1
            if not all_words_generator:
                all_words_generator = get_words(filename)
            else:
                all_words_generator = chain(all_words_generator, get_words(filename))
        if counter >=2:
            break
    count_words(all_words_generator)
