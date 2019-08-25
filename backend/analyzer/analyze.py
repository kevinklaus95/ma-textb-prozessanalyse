import numpy as np
import lda
import pandas
from .dataset import LDADataset

# Die Analyze-Funktion übernimmt die eigentliche Analyse im Server. Der erste Teil ist die LDA-Analyse, die zu 90%
# aus scarlett übernommen wurde. Es wurde lediglich an der Übergabe und den Formaten der Daten soweit etwas geändert,
# dass die Analyse ohne Fehler zu werfen wieder Ergebnisse produzieren konnte.
# Im zweiten Teil der Analyse wird die Wörterbuchanalyse durchgeführt.
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
            emotion_dictionary='simple',
            content_dictionary='simple',
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

    # Daten vorbereiten
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

    # LDA Analyse abgeschlossen, Wörterbuchanalyse startet
    print('LDA Done, starting Emotion Dictionary')

    # Wörterbuch einlesen - abhängig vom gewählten Parameter entweder das einfache oder das angereicherte WB
    if emotion_dictionary == 'simple':
        df = pandas.read_csv('analyzer/woerterbuch_emotion.csv')
    else:
        df = pandas.read_csv('analyzer/woerterbuch_emotion_angereichert.csv')

    # Datengrundlage auch hier die vorbereiteten Daten der LDA-Analyse, kein neues Preprocessing notwendig
    entry_text_dict = data.entry_text_dict

    # aus den Spalten der Wörterbücher sollen Dicts gemacht werden, die das Auslesen der Tokens extrem erleichtern
    cold_word_dict = pandas.Series('Kalt', index=df.Kalt).to_dict()
    warm_word_dict = pandas.Series('Warm', index=df.Warm).to_dict()

    # initiiere Listen, die später mit gefundenen Wörtern gefüllt werden
    cold_words = list()
    warm_words = list()

    # für jeden Eintrag (Zeitspannen)
    for entry in content:

        id = entry['id']

        # finde den entsprechenden Text in den vorbereiteten Texten
        # try - except ist für den Vergleichsfall - in manchen Fällen kann hier eine ID nicht vergeben sein.
        try:
            words = entry_text_dict[id]
        except KeyError:
            words = []

        # initiiere Counter für die Anzahl der gefundenen kalten und warmen Wort
        counters = {'Warm': 0, 'Kalt': 0}

        # für jeden Token im Dokument
        for token in words:
            text = str(token)
            # Prüfe, ob die Spalte der warmen Wörter im Wörterbuch das Wort enthält
            # dazu wird lediglich gecheckt, ob der Key im Dict vorhanden ist, womit eine performante Analyse
            # auch bei großen Wörterbüchern garantiert werden kann
            if text in warm_word_dict:
                print("Warm:", text)
                # Counter um 1 erhöhen und das Wort in die Liste der gefundenen Wörter hinzufügen
                counters['Warm'] += 1
                warm_words.append(text)
            # Für kalte Wörter genauso wiederholen
            if text in cold_word_dict:
                print("Kalt:", text)
                counters['Kalt'] -= 1
                cold_words.append(text)
        entry['emotion_counters'] = counters

    # Wörterbuchanalyse abgeschlossen
    print('Emotion Dictionary done, starting Content Dictionary...')

    # Wörterbuch einlesen - abhängig vom gewählten Parameter entweder das einfache oder das angereicherte WB
    if content_dictionary == 'simple':
        df = pandas.read_csv('analyzer/woerterbuch_inhalt.csv')
    else:
        df = pandas.read_csv('analyzer/woerterbuch_inhalt_angereichert.csv')

    # Datengrundlage auch hier die vorbereiteten Daten der LDA-Analyse, kein neues Preprocessing notwendig
    entry_text_dict = data.entry_text_dict

    # aus den Spalten der Wörterbücher sollen Dicts gemacht werden, die das Auslesen der Tokens extrem erleichtern
    school_word_dict = pandas.Series('Bildungsort', index=df.Bildungsort).to_dict()
    home_word_dict = pandas.Series('Lebensort', index=df.Lebensort).to_dict()

    # initiiere Listen, die später mit gefundenen Wörtern gefüllt werden
    school_words = list()
    home_words = list()

    # für jeden Eintrag (Zeitspannen)
    for entry in content:

        id = entry['id']

        # finde den entsprechenden Text in den vorbereiteten Texten
        # try - except ist für den Vergleichsfall - in manchen Fällen kann hier eine ID nicht vergeben sein.
        try:
            words = entry_text_dict[id]
        except KeyError:
            words = []

        # initiiere Counter für die Anzahl der gefundenen kalten und warmen Wort
        counters = {'Lebensort': 0, 'Bildungsort': 0}

        # für jeden Token im Dokument
        for token in words:
            text = str(token)
            # Prüfe, ob die Spalte der warmen Wörter im Wörterbuch das Wort enthält
            # dazu wird lediglich gecheckt, ob der Key im Dict vorhanden ist, womit eine performante Analyse
            # auch bei großen Wörterbüchern garantiert werden kann
            if text in home_word_dict:
                print("Lebensort:", text)
                # Counter um 1 erhöhen und das Wort in die Liste der gefundenen Wörter hinzufügen
                counters['Lebensort'] += 1
                home_words.append(text)
            # Für kalte Wörter genauso wiederholen
            if text in school_word_dict:
                print("Bildungsort:", text)
                counters['Bildungsort'] += 1
                school_words.append(text)
        entry['content_counters'] = counters

    # Ergebnis zurückliefern
    return dict(lda_result=output,
                emotion_dictionary_result=content,
                content_dictionary_result=content,
                cold_words=cold_words,
                warm_words=warm_words,
                school_words=school_words,
                home_words=home_words
                )
