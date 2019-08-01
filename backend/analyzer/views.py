from rest_framework import viewsets
from rest_framework.decorators import api_view
from .serializers import HoursSerializer
from .models import Hours
from rest_framework.response import Response
from .analyze import analyze
from datetime import datetime, timedelta
from pprint import pprint


@api_view()
def distinct_project_ids(request):
    project_ids = Hours.objects.order_by('project_id').values_list('project_id', flat=True).distinct()
    return Response({"project_ids": project_ids})


def group_for_timespan(hours, timespan, start, end):
    time_ranges = []
    start = datetime.strptime(start, '%Y-%m-%d')
    end = datetime.strptime(end, '%Y-%m-%d')
    temp_start = start
    time_add = timedelta(days=timespan)
    count = 1

    # add all the time ranges that fit into the whole range and break before the last one
    while temp_start + time_add <= end:
        time_ranges.append({'start': temp_start, 'stop': temp_start + time_add})
        temp_start += time_add

    # add the last one which will typically not be complete
    time_ranges.append({'start': temp_start, 'stop': end})

    # got the time ranges, can now filter the hours for these time ranges and add the text to the time_ranges to extend the dicts
    for ti in time_ranges:
        temp_hours = hours.filter(start__gte=ti['start'], stop__lte=ti['stop'])
        text = ''
        for hour in temp_hours:
            text += str(hour.comment)
            text += ' '
        ti['comment'] = text
        ti['id'] = count
        count += 1

    #pprint(time_ranges)

    return time_ranges

@api_view(['POST'])
def start_analysis(request):

    project_id = request.data.get('chosenCaseId', None)
    start_date = request.data.get('start', None)
    end_date = request.data.get('end', None)
    config = request.data.get('config', {})
    timespan = int(config.get('timespan', 0))

    if timespan is 0:
        hours = Hours.objects.filter(project_id=project_id, start__gte=start_date, stop__lte=end_date)\
            .values('comment', 'id', 'start', 'stop')
    else:
        hours = group_for_timespan(
            Hours.objects.filter(project_id=project_id, start__gte=start_date, stop__lte=end_date), timespan,
            start_date, end_date)

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
                         positive_text='')

    return Response(
        # {'hours': hours, 'lda_result': mock_lda, 'dictionary_result': mock_dict})
        {'hours': hours,
         'lda_result': result['lda_result'],
         'dictionary_result': result['dictionary_result'],
         'warm_words': result['warm_words'],
         'cold_words': result['cold_words']
         })


@api_view(['POST'])
def start_custom_analysis(request):

    config = request.data.get('config', {})
    custom_text = request.data.get('customText', '')

    result = analyze([{'id': 1, 'comment': custom_text}],
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
                         positive_text='')

    return Response(
        {'hours': [{'id': 0, 'comment': custom_text}],
         'lda_result': result['lda_result'],
         'dictionary_result': result['dictionary_result'],
         'warm_words': result['warm_words'],
         'cold_words': result['cold_words']})

class HoursView(viewsets.ModelViewSet):
    serializer_class = HoursSerializer
    queryset = Hours.objects.all()
