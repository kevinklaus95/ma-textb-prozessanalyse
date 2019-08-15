import numpy as np
import snowballstemmer
from nltk.corpus import stopwords as nltkstopwords

# LDADataset Klasse - wurde zu 80-90% aus Scarlett übernommen und nur zu den nötigsten Teilen auf diese Anwendung
# umgebaut. Die Umbauten bezogen sich besonders auf das Umbenennen von Variablen, die suggerierten,
# dass es sich bei den Daten um Foliensätze handelt.

class LDADataset:
    '''
    Holding all data necessary for LDA analysis
    '''

    def __init__(self):

        self.vocab = []
        self.entries = []
        self.dataset = None
        self.filtered_high_word_occurrences = []
        self.filtered_toshortwords = []
        self.filtered_stopwords = []
        self.filtered_numbers = []
        self.filtered_no_word_entries = []
        self.filtered_no_positive_words = []
        self.stemmer_map = dict()
        self.entry_text_dict = dict()

    def build(self,
              content,
              ignore_capitalization=False,
              stemmer_language='german',
              stopword_language='',
              word_min_length=0,
              filter_numbers=False,
              filter_high_word_occ=0.6,
              filter_no_word_entries=True,
              positive_text=''):
        '''
        Initializes LDA datastructure from lessons content
        :param lessons: content
        :param stemmer_language: language for stemming words
        :param filter_high_word_occ: percentage of maximum allowed occurrence of a word. Set to 1 for no filtering
        :param filter_no_word_entries: if True filteres entries without any word in it. Empty pages or pages with image only
        :return:
        '''
        # Filter setup
        try:
            stemmer = snowballstemmer.stemmer(stemmer_language)
            print('Stemming %s' % stemmer_language)
        except:
            stemmer = False

        try:
            stopwords = nltkstopwords.words(stopword_language)
            print('Filtering stopwords %s' % stopword_language)
        except:
            stopwords = False

        # if a positive text exists this is cleaned up for filtering (with no positive filter text of course)
        if positive_text:
            print('Filtering text by positive text!')
            positive_text = self.__clean_text(
                ignore_capitalization=ignore_capitalization,
                filter_numbers=filter_numbers,
                word_min_length=word_min_length,
                stemmer=stemmer,
                stopwords=stopwords,
                positive_filter=False,
                text=positive_text
            )

        # build dict {entry_entry:[cleaned_up_word_array]}
        self.entry_text_dict = dict()
        # cleanup and prepare text of documents from lesson
        for entry in content:

            id = entry['id']

            word_array = self.__clean_text(
                ignore_capitalization=ignore_capitalization,
                filter_numbers=filter_numbers,
                word_min_length=word_min_length,
                stemmer=stemmer,
                stopwords=stopwords,
                positive_filter=positive_text,
                text=entry['comment'] + ' ' + entry['reflection']
            )

            self.entry_text_dict[id] = word_array

            if not id in self.entries:
                self.entries.append(id)

            for word in word_array:
                if not word in self.vocab:
                    self.vocab.append(word)

        # filter high occurrence of words using all documents
        if filter_high_word_occ < 1.0:
            self.__filter_high_word_occurrences(filter_high_word_occ, filter_no_word_entries)
        else:
            print('Skipping filtering of high word occurrences')

        self.__build_occurrencematrix()

        return self

    def __clean_text(self, ignore_capitalization=False, filter_numbers=False, word_min_length=0, stemmer=False,
                     stopwords=False, positive_filter=False, text=''):
        '''Cleans given text of symbols, numbers, stopwords, and performs stemming if necessary'''
        if (ignore_capitalization): text = text.lower()

        text = text.replace('\n', ' ').replace('<br>', ' ')  # remove newlines
        text = text.translate({ord(c): "" for c in "\"!@#$%^&*()[]{};:,./<>?\|`'~-=_+"})  # remove symbols
        text = text.split()

        # apply filters
        cleaned_text = []
        for word in text:

            if filter_numbers and word.isdigit():
                if word not in self.filtered_numbers:
                    self.filtered_numbers.append(word)

            elif stopwords and word.lower() in stopwords:
                if word not in self.filtered_stopwords:
                    self.filtered_stopwords.append(word)

            elif word_min_length and len(word) < word_min_length:
                if word not in self.filtered_toshortwords:
                    self.filtered_toshortwords.append(word)

            else:
                cleaned_text.append(word)

        # stemming - keep an unstemmed reference array (used to provide stemming map)
        if stemmer:
            unstemmed = cleaned_text[:]
            cleaned_text = stemmer.stemWords(cleaned_text)
            for i, stemmed_word in enumerate(cleaned_text):
                self.stemmer_map[unstemmed[i]] = stemmed_word

        if positive_filter:
            positive_text = []
            for i, word in enumerate(cleaned_text):
                if word not in positive_filter:

                    if stemmer:
                        word = unstemmed[i]

                    if not word in self.filtered_no_positive_words:
                        self.filtered_no_positive_words.append(word)

                else:
                    positive_text.append(word)
            cleaned_text = positive_text

        return cleaned_text

    def __filter_high_word_occurrences(self, percent_low_pass, filter_no_word_entries):
        '''
        Removes all words that occurr in high percent of entries
        :param percent_low_pass: percent for low pass filtering
        :param filter_no_word_entries: if True emtpy entries are removed afterwards
        :return:
        '''
        for word in self.vocab:
            occurrence = 0
            for text in self.entry_text_dict.values():
                if word in text:
                    occurrence += 1

            if occurrence / len(self.entries) > percent_low_pass:
                self.filtered_high_word_occurrences.append(word)
                self.vocab = [good_word for good_word in self.vocab if good_word != word]

        if len(self.filtered_high_word_occurrences) > 0:
            print('Removing words with over %s percent occurrence: %s' % (
                percent_low_pass * 100, self.filtered_high_word_occurrences))

            for bad_word in self.filtered_high_word_occurrences:
                for entry in self.entries[
                             :]:  # iterating through copy of entries cause entries may be removed by filter_no_word_entries
                    dirty_text = self.entry_text_dict[entry]
                    clean_text = [good_word for good_word in dirty_text if good_word != bad_word]
                    self.entry_text_dict[entry] = clean_text

                    if filter_no_word_entries and len(clean_text) == 0:
                        print('Removing %s after filtering high occurrence words. No text left' % entry)
                        del (self.entry_text_dict[entry])
                        self.entries = [good_entry for good_entry in self.entries if good_entry != entry]
                        self.filtered_no_word_entries.append(entry)

    def __build_occurrencematrix(self):
        '''
        Building dataset. entry x word matrix marking occurrences
        #       word1  word2   word3..
        #entry1 1       0       0
        #entry2 1       3       0
        #entry3 0       1       2
        #...
        '''
        print('Building occurrence matrix with %s entries and %s words' % (len(self.entries), len(self.vocab)))
        self.dataset = np.zeros(shape=(len(self.entries), len(self.vocab)), dtype='int64')

        for entry_i, entry in enumerate(self.entries):
            for word in self.entry_text_dict[entry]:
                self.dataset[entry_i][self.vocab.index(word)] += 1