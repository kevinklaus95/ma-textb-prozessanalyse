"""
import pandas
from fuzzywuzzy import fuzz
from pprint import pprint
from .lda import LDADataset


def dictionary_analyze(content,
                       filter_high_word_occ=0.6,
                       filter_no_word_entries=True,
                       ignore_capitalization=False,
                       stemmer_language='german',
                       stopword_language='',
                       word_min_length=0,
                       filter_numbers=False,
                       positive_text=''
                       ):

    dataset = LDADataset()
    dataset = dataset.build(content,
                            ignore_capitalization=ignore_capitalization,
                            stemmer_language=stemmer_language,
                            stopword_language=stopword_language,
                            word_min_length=word_min_length,
                            filter_numbers=filter_numbers,
                            filter_high_word_occ=filter_high_word_occ,
                            filter_no_word_entries=filter_no_word_entries,
                            positive_text=positive_text
                            )

    # Wörterbuch einlesen
    df = pandas.read_csv('analyzer/woerterbuch.csv')

    entry_text_dict = dataset.entry_text_dict

    for entry in content:

        id = entry['id']

        words = entry_text_dict[id]

        counters = {'Warm': 0, 'Kalt': 0}

        # für jeden Token im Dokument
        for token in words:
            # für jede Zeile im Wörterbuch
            text = str(token).lower()
            for index, row in df.iterrows():
                warm = str(row.Warm).lower()
                kalt = str(row.Kalt).lower()
                if text.lower() == warm.lower() or fuzz.ratio(
                        text.lower(), warm.lower()) > 80:
                    counters['Warm'] += 1
                if text.lower() == kalt.lower() or fuzz.ratio(
                        text.lower(), kalt.lower()) > 80:
                    counters['Kalt'] += 1

        entry['counters'] = counters

    pprint(content)

    return content
"""
