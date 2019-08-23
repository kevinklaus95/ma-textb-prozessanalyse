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
    help = \
        'Enriches the current dictionary by calling OpenTheSaurus API. Result is saved to woerterbuch_inhalt_angereichert.csv'

    def handle(self, *args, **options):
        # Wörterbuch einlesen
        df = pandas.read_csv('analyzer/woerterbuch_inhalt.csv')

        # Startset besteht aus den Saatwörtern im Wörterbuch
        home_words = [str(word[1]) for word in df['Lebensort'].iteritems()]
        school_words = [str(word[1]) for word in df['Bildungsort'].iteritems()]

        # initiiere Listen für Anreicherung
        new_home_words = []
        new_school_words = []

        # Counter für maximale Anzahl an API Calls
        api_counter = 0

        # SSL Context für API Calls
        gcontext = ssl.SSLContext()

        # Warme Wörter anreichern
        for word in home_words:

            # Setze URL für aktuelles Seedwort
            url = f'https://www.openthesaurus.de/synonyme/search?q={prepare_word_for_url(word)}&format=application/json'
            print("Suche für:", word)

            # Wenn noch keine 50 Requests hintereinander gemacht wurden, setze Request ab und erhöhe Counter
            if api_counter < 50:
                serialized_data = urlopen(url, context=gcontext).read()
                api_counter += 1
            # Wenn 50 Requests erreicht wurden, warte 60 Sekunden und führe Request dann aus.
            # Resette den Counter anschließend.
            else:
                print('Sleep 60 seconds, too many requests...')
                time.sleep(60)
                serialized_data = urlopen(url, context=gcontext).read()
                api_counter = 1

            # Parse das Ergebnis als JSON
            data = json.loads(serialized_data)
            # Für jede Gruppe von Synsets im Ergebnis-JSON
            for group in data['synsets']:
                # Für jedes Wort im Synset
                for term in group['terms']:
                    # Checken, ob Wort in den warmen Seedwörtern oder in den neu angereicherten Wörtern für Lebensort ist
                    # Wenn ja, weiter mit dem nächsten Wort
                    if term['term'] in home_words or term['term'] in new_home_words:
                        continue
                    # Wenn nicht, füge das Wort zu der neuen Wortliste hinzu
                    else:
                        print('Neues Wort für Lebensort: ', term['term'])
                        new_home_words.append(str(term['term']))


        # Wörter für Bildungsort anreichern - gleiche Prozedur wie bei den warmen Wörtern.
        for word in school_words:
            url = f'https://www.openthesaurus.de/synonyme/search?q={prepare_word_for_url(word)}&format=application/json'
            print("Suche für:", word)

            if api_counter < 50:
                serialized_data = urlopen(url, context=gcontext).read()
                api_counter += 1
            else:
                print('Sleep 60 seconds, too many requests...')
                time.sleep(60)
                serialized_data = urlopen(url, context=gcontext).read()
                api_counter = 0

            data = json.loads(serialized_data)
            for group in data['synsets']:
                for term in group['terms']:
                    if term['term'] in school_words or term['term'] in new_school_words:
                        continue
                    else:
                        print('Neues Wort für Bildungsort: ', term['term'])
                        new_school_words.append(str(term['term']))

        # altes Wörterbuch (Seedwörter) mit neuen Wörtern konkatenieren
        home_words = home_words + new_home_words
        school_words = school_words + new_school_words

        # Ergebnis sortieren
        home_words.sort()
        school_words.sort()

        # Listen gleich lang machen, um zip zu vereinfachen
        if len(home_words) >= len(school_words):
            while len(home_words) != len(school_words):
                school_words.append('')
        else:
            while len(home_words) != len(school_words):
                home_words.append('')

        # Spaltenköpfe ergänzen
        school_words.insert(0, "Bildungsort")
        home_words.insert(0, "Lebensort")

        # Schreibe neue Listen in CSV
        with open('analyzer/woerterbuch_inhalt_angereichert.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(zip(home_words, school_words))