import pandas
from urllib.request import urlopen
import json
import ssl
import time
import csv

from django.core.management.base import BaseCommand, CommandError

def prepare_word_for_url(word):
    chars = {'ö': 'oe', 'ä': 'ae', 'ü': 'ue', 'Ö': 'Oe', 'Ä': 'Ae', 'Ü': 'Ue', 'ß': 'ss', ' ': ''}
    for char in chars:
        word = str(word).replace(char, chars[char])
    return word


class Command(BaseCommand):
    help = 'Enriches the current dictionary by calling OpenTheSaurus API. Result is saved to woerterbuch_new.csv'

    def handle(self, *args, **options):
        # Wörterbuch einlesen
        df = pandas.read_csv('analyzer/woerterbuch.csv')

        # Startset besteht aus den Saatwörtern im Wörterbuch
        warm_words = [str(word[1]) for word in df['Warm'].iteritems()]
        cold_words = [str(word[1]) for word in df['Kalt'].iteritems()]

        # initiiere Listen für Anreicherung
        new_warm_words = []
        new_cold_words = []

        # Counter für maximale Anzahl an API Calls
        api_counter = 0

        # SSL Context für API Calls
        gcontext = ssl.SSLContext()

        # Warme Wörter anreichern
        for word in warm_words:

            url = f'https://www.openthesaurus.de/synonyme/search?q={prepare_word_for_url(word)}&format=application/json'
            print("Suche für:", word)

            if api_counter < 50:
                serialized_data = urlopen(url, context=gcontext).read()
                api_counter += 1
            else:
                print('Sleep 60 seconds, too many requests...')
                time.sleep(60)
                api_counter = 0

            data = json.loads(serialized_data)
            for group in data['synsets']:
                for term in group['terms']:
                    if term['term'] in warm_words or term['term'] in new_warm_words:
                        continue
                    else:
                        print('Neues warmes Wort: ', term['term'])
                        new_warm_words.append(str(term['term']))


        # Kalte Wörter anreichern
        for word in cold_words:
            url = f'https://www.openthesaurus.de/synonyme/search?q={prepare_word_for_url(word)}&format=application/json'
            print("Suche für:", word)

            if api_counter < 50:
                serialized_data = urlopen(url, context=gcontext).read()
                api_counter += 1
            else:
                print('Sleep 60 seconds, too many requests...')
                time.sleep(60)
                api_counter = 0

            data = json.loads(serialized_data)
            for group in data['synsets']:
                for term in group['terms']:
                    if term['term'] in cold_words or term['term'] in new_cold_words:
                        continue
                    else:
                        print('Neues kaltes Wort: ', term['term'])
                        new_cold_words.append(str(term['term']))

        # altes Wörterbuch mit neuen Wörtern konkatenieren
        warm_words = warm_words + new_warm_words
        cold_words = cold_words + new_cold_words

        # Ergebnis sortieren
        warm_words.sort()
        cold_words.sort()

        # Listen gleich lang machen, um zip zu vereinfachen
        if len(warm_words) >= len(cold_words):
            while len(warm_words) != len(cold_words):
                cold_words.append('')
        else:
            while len(warm_words) != len(cold_words):
                warm_words.append('')

        # Schreibe neue Listen in CSV
        with open('analyzer/woerterbuch_angereichert.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(zip(warm_words, cold_words))

# TODO code clean up