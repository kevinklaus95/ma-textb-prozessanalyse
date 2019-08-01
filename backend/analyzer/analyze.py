import numpy as np
import lda
# text processing
import snowballstemmer
import nltk
from pprint import pprint
import pandas
from fuzzywuzzy import fuzz
from nltk.corpus import stopwords as nltkstopwords


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
                text=entry['comment']
            )

            print(word_array)

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


def analyze(content,
                dirichlet_alpha=0.1,
                dirichlet_eta=0.01,
                n_topics=3,
                n_iter=1500,
                random_state=1,
                n_top_words=8,
                n_top_topics=3,
                filter_high_word_occ=0.6,
                filter_no_word_entries=True,
                ignore_capitalization=False,
                stemmer_language='german',
                stopword_language='',
                word_min_length=0,
                filter_numbers=False,
                positive_text=''):
    '''
    Does lda analyzes on lesson content
    :param lesson_id: id of lesson
    :param n_topics: number of topics
    :param n_iter: number of iterations
    :param random_state: dont know
    :param n_top_words: number of top words in distribution to output
    :return:
    '''
    data = LDADataset()
    data = data.build(content,
                              ignore_capitalization=ignore_capitalization,
                              stemmer_language=stemmer_language,
                              stopword_language=stopword_language,
                              word_min_length=word_min_length,
                              filter_numbers=filter_numbers,
                              filter_high_word_occ=filter_high_word_occ,
                              filter_no_word_entries=filter_no_word_entries,
                              positive_text=positive_text)

    model = lda.LDA(n_topics=n_topics, n_iter=n_iter, random_state=random_state, alpha=dirichlet_alpha,
                    eta=dirichlet_eta)
    model.fit(data.dataset)
    topic_word = model.topic_word_  # topic x word probability distribution matrix
    doc_topic = model.doc_topic_  # entry x topic probability distribution matrix

    output = dict()
    output['vocabulary'] = data.vocab
    output['entries'] = dict()
    output['topics'] = dict()
    output['is_normalized'] = dict()

    # filtered values
    output['filtered'] = dict()
    if (len(data.filtered_high_word_occurrences)):
        output['filtered']['filtered_high_word_occ'] = data.filtered_high_word_occurrences
    if (len(data.filtered_no_word_entries)):
        output['filtered']['no_word_entries'] = data.filtered_no_word_entries
    if (len(data.filtered_stopwords)):
        output['filtered']['stopwords'] = data.filtered_stopwords
    if (len(data.filtered_numbers)):
        output['filtered']['numbers'] = data.filtered_numbers
    if (len(data.filtered_no_positive_words)):
        output['filtered']['no_positive_words'] = data.filtered_no_positive_words
    if (len(data.filtered_toshortwords)):
        output['filtered']['to_short_words'] = data.filtered_toshortwords

    if (len(data.stemmer_map)):
        output['stemmer_map'] = data.stemmer_map

    # building dict for all entries
    for i, entry_name in enumerate(data.entries):
        output['entries'][entry_name] = dict()
        output['entries'][entry_name]['position'] = i

    # building output for entry x word occurrences
    for entry_i, row in enumerate(data.dataset):
        output['entries'][data.entries[entry_i]]['word_occurrence'] = row.tolist()

    # building output for entry x topic probabilities
    for entry_i, row in enumerate(doc_topic):
        topic_probability = dict()
        for topic_i, probability in enumerate(row):
            topic_probability['Topic' + str(topic_i)] = float(probability)
        output['entries'][data.entries[entry_i]]['topic_probabilities'] = topic_probability

    # collection of topics and their distribution over words
    for entry_i, entry_distri in enumerate(doc_topic):
        doc_topics = np.array(range(n_topics))[np.argsort(entry_distri)][:-n_top_topics - 1:-1].tolist()
        output['entries'][data.entries[entry_i]]['top_topics'] = ['Topic' + str(topic_n) for topic_n in doc_topics]

    # verifying is_normalized of topic probabilities per entry (sum = 1)
    output['is_normalized']['entry_topic_probabilities'] = True
    for entry_i in range(len(data.entries)):
        probability_sum = sum(doc_topic[entry_i, :])
        output['entries'][data.entries[entry_i]]['is_normalized'] = dict()
        output['entries'][data.entries[entry_i]]['is_normalized']['probability_sum'] = probability_sum
        if abs(probability_sum - np.float64(1.0)) > 1e-10:
            output['is_normalized']['entry_topic_probabilities'] = False
            output['entries'][data.entries[entry_i]]['is_normalized']['normalized'] = False
            # print("Sum(topic probabilities) of entry: %s = %s" % (entry_i, probability_sum))
        else:
            output['entries'][data.entries[entry_i]]['is_normalized']['normalized'] = True

    # building dict for all topics
    for i in range(n_topics):
        output['topics']['Topic' + str(i)] = dict()

    # building output for topic x word probabilities
    for topic_i, row in enumerate(topic_word):
        word_probability = dict()
        for vocab_i, probability in enumerate(row):
            word_probability[data.vocab[vocab_i]] = float(probability)
        output['topics']['Topic' + str(topic_i)]['word_probabilities'] = word_probability

    # collection of topics and their distribution over words
    for i, topic_distri in enumerate(topic_word):
        topic_words = np.array(data.vocab)[np.argsort(topic_distri)][:-n_top_words - 1:-1].tolist()
        output['topics']['Topic' + str(i)]['top_words'] = topic_words

    # verifying is_normalized of word probabilities per topic (sum = 1)
    output['is_normalized']['topic_word_probabilities'] = True
    for i in range(n_topics):
        probability_sum = sum(topic_word[topic_i, :])
        output['topics']['Topic' + str(i)]['is_normalized'] = dict()
        output['topics']['Topic' + str(i)]['is_normalized']['probability_sum'] = probability_sum
        if abs(probability_sum - np.float64(1.0)) > 1e-10:
            output['is_normalized']['topic_word_probabilities'] = False
            output['topics']['Topic' + str(i)]['is_normalized']['normalized'] = True
            # print("Sum(word probabilities) of topic: %s = %s" % (topic_i, probability_sum))
        else:
            output['topics']['Topic' + str(i)]['is_normalized']['normalized'] = True

    print('LDA Done, starting Dictionary')

    # Wörterbuch einlesen
    df = pandas.read_csv('analyzer/woerterbuch.csv')

    entry_text_dict = data.entry_text_dict

    cold_words = list()
    warm_words = list()

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
                        text.lower(), warm.lower()) > 90:
                    print("Warm:", text)
                    counters['Warm'] += 1
                    warm_words.append(text)
                if text.lower() == kalt.lower() or fuzz.ratio(
                        text.lower(), kalt.lower()) > 90:
                    print("Kalt:", text)
                    counters['Kalt'] -= 1
                    cold_words.append(text)

        entry['counters'] = counters

    print('Dictionary done!')

    return dict(lda_result=output, dictionary_result=content, cold_words=cold_words, warm_words=warm_words)
