from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from .serializers import HoursSerializer
from .models import Hours
from rest_framework.response import Response
from .analyze import analyze
from datetime import datetime, timedelta
import nltk


# Route, mit der die verschiedenen Projekt-IDs abgerufen werden, damit sie im Frontend zur Auswahl stehen können
# Wird beim Aufruf der Software im Browser bereits gecallt
# Weiterhin wird hier der Stoppwort-Korpus bereits geladen, damit er für eine anschließende Analyse bereitsteht
@api_view()
def distinct_project_ids(request):
    try:
        nltk.download('stopwords')
    except:
        print('Could not update stopword nltk_data package relevant for LDA-Analysis')

    # Resultierende Projekt-IDs absteigend sortieren, da neuere und höhere Projekt-IDs für Analysen aufgrund von mehr
    # Inhalt relevanter sind
    project_ids = Hours.objects.order_by('-project_id').values_list('project_id', flat=True).distinct()
    return Response({"project_ids": project_ids})


# Mithilfe dieser Funktion sollen die verschiedenen Datenbankeinträge aus der Hours-Tabelle zu bestimmten Zeiträumen
# gruppiert werden. Dazu erwartet die Funktion die eigentlichen Objekte der Datenbank, die Zeitspanne, nach der gruppiert
# werden soll, sowie das Start- und Enddatum, welches für die Analyse eingestellt wurde.
def group_for_timespan(hours, timespan, start, end):
    # initialisieren
    time_ranges = []
    start = datetime.strptime(start, '%Y-%m-%d')
    end = datetime.strptime(end, '%Y-%m-%d')
    temp_start = start
    time_add = timedelta(days=timespan)
    count = 1
    empty = True

    # Zeitspannen hinzufügen bis die gesamte Range ausgeschöpft wurde. Vor der letzten Zeitspanne wird gestoppt.
    while temp_start + time_add <= end:
        time_ranges.append({'start': temp_start, 'stop': temp_start + time_add})
        temp_start += time_add

    # Die letzte Zeitspanne hinzufügen, da diese verglichen mit den
    # anderen höchstwahrscheinlich nicht vollständig sein wird.
    time_ranges.append({'start': temp_start, 'stop': end})

    # Zeitspannen sind vorhanden, nun die Datenbankeinträge jeweils auf die Zeitspannen anpassen und deren Texte
    # in die Zeitspannen-Objekte übernehmen, um so die Gruppierung der Texte auf die Zeitspanne zu bekommen
    for ti in time_ranges:
        temp_hours = hours.filter(start__gte=ti['start'], stop__lte=ti['stop'])
        comment_text = ''
        reflection_text = ''
        # sowohl die Comment-Spalte als auch die Reflection-Spalte werden genutzt und konkateniert
        for hour in temp_hours:
            comment_text += str(hour.comment)
            comment_text += ' '
            reflection_text += str(hour.reflection)
            reflection_text += ' '

        ti['comment'] = comment_text
        ti['reflection'] = reflection_text
        # count dient hier lediglich als Index und ID
        ti['id'] = count
        count += 1

    # Checken, ob alle gefundenen Datenbankeinträge keine Texte hatten, um Fehlermeldung fürs Frontend vorzubereiten
    for entry in time_ranges:
        if entry['comment'] != '' or entry['reflection'] != '':
            empty = False
            break

    return time_ranges, empty

# In dieser Funktion werden die eigentlichen Analysen angestoßen. LDA und Wörterbuch werden beide durch diese Route
# gestartet. Dazu wird ein POST-Request benötigt, welcher die entsprechende Projekt-ID für den zu analysierenden Fall,
# das Start- und Enddatum für die zu filternden Texte, die entsprechende Konfiguration der Analyse und die gewählte
# Zeitspanne beinhalten muss.
@api_view(['POST'])
def start_analysis(request):

    project_id = request.data.get('chosenCaseId', None)
    start_date = request.data.get('start', None)
    end_date = request.data.get('end', None)
    config = request.data.get('config', {})
    timespan = int(config.get('timespan', 0))

    # Prüfen, ob Zeitspanne gewählt wurde. Wenn Zeitspanne 0, keine zeitliche Gruppierung vornehmen, sondern die Einträge
    # mit ihrem jeweiligen Zeitpunkt zurückliefern

    if timespan is 0:
        hours = Hours.objects.filter(project_id=project_id, start__gte=start_date, stop__lte=end_date)\
            .values('comment', 'reflection', 'id', 'start', 'stop')
        empty = True if len(hours) == 0 else False
    # Wenn Zeitspanne gewählt wurde, soll hier die Gruppierung der Texte auf diese Zeitspanne erfolgen
    else:
        hours, empty = group_for_timespan(
            Hours.objects.filter(project_id=project_id, start__gte=start_date, stop__lte=end_date), timespan,
            start_date, end_date)
    # Wenn an diesem Punkt bereits klar ist, dass die Texte leer sind - antworte dem Frontend mit einem 204-Status
    if empty:
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    # Aufruf der Analyse-Funktion mit allen nötigen Parametern für das Preprocessing und der eigentlichen Analyse
    result = analyze(hours,
                         dirichlet_alpha=float(config['dirichletAlpha']),
                         dirichlet_eta=float(config['dirichletEta']),
                         n_topics=int(config['numberOfTopics']),
                         n_iter=int(config['numberOfIterations']),
                         random_state=int(config['randomSeed']),
                         n_top_words=int(config['displayedTopicsTopWords']),
                         n_top_topics=int(config['numberOfDisplayedTopTopics']),
                         filter_high_word_occ=float(config['removeHighFrequentWords']),
                         filter_no_word_entries=True,
                         ignore_capitalization=config['ignoreCapitalization'],
                         stemmer_language='german' if config['stemming'] else '',
                         stopword_language='german' if config['removeStopwords'] else '',
                         word_min_length=int(config['minimalWordLength']),
                         filter_numbers=config['removeNumbers'],
                         dictionary=config['dictionary'],
                         positive_text='')

    # Antwort ans Frontend mit den analysierten Texten, den Ergebnissen und den gefundenen Wörtern im Wörterbuch
    return Response(
        {'hours': hours,
         'lda_result': result['lda_result'],
         'dictionary_result': result['dictionary_result'],
         'warm_words': result['warm_words'],
         'cold_words': result['cold_words']
         })

# Ähnlicher Aufbau zu oberer Funktion, hier allerdings mit Freitexten ohne Datenbank-Anbindung für Analysen, die on-the-
# fly gemacht werden sollen
@api_view(['POST'])
def start_custom_analysis(request):

    config = request.data.get('config', {})
    custom_text = request.data.get('customText', '')

    result = analyze([{'id': 1, 'comment': custom_text, 'reflection': ''}],
                         dirichlet_alpha=float(config['dirichletAlpha']),
                         dirichlet_eta=float(config['dirichletEta']),
                         n_topics=int(config['numberOfTopics']),
                         n_iter=int(config['numberOfIterations']),
                         random_state=int(config['randomSeed']),
                         n_top_words=int(config['displayedTopicsTopWords']),
                         n_top_topics=int(config['numberOfDisplayedTopTopics']),
                         filter_high_word_occ=1,
                         filter_no_word_entries=True,
                         ignore_capitalization=config['ignoreCapitalization'],
                         stemmer_language='german' if config['stemming'] else '',
                         stopword_language='german' if config['removeStopwords'] else '',
                         word_min_length=int(config['minimalWordLength']),
                         filter_numbers=config['removeNumbers'],
                         dictionary=config['dictionary'],
                         positive_text='')

    return Response(
        {'hours': [{'id': 0, 'comment': custom_text, 'reflection': ''}],
         'lda_result': result['lda_result'],
         'dictionary_result': result['dictionary_result'],
         'warm_words': result['warm_words'],
         'cold_words': result['cold_words']})

class HoursView(viewsets.ModelViewSet):
    serializer_class = HoursSerializer
    queryset = Hours.objects.all()
