from django.shortcuts import render_to_response
from domain.decorators import login_and_domain_required
from django.template import RequestContext

from collections import defaultdict
from django.db.models import Max, Min

import datetime
from models import *

def _parse_date(string):
    if isinstance(string, basestring):
        return datetime.datetime.strptime(string, "%Y-%m-%d").date()
    else:
        return string

@login_and_domain_required
def index(request, template='dots/index.html'):
    end_date = _parse_date(request.GET.get('end', datetime.date.today()))
    start_date = _parse_date(request.GET.get('start', end_date-datetime.timedelta(14)))
    patient_id = request.GET.get('patient', None)

    if start_date > end_date:
         end_date = start_date
    elif end_date - start_date > datetime.timedelta(365):
         end_date = start_date + datetime.timedelta(365) 
    dates = []
    date = start_date
    while date <= end_date:
        dates.append(date)
        date += datetime.timedelta(1)

    try:
        patient = Patient.objects.get(id=patient_id)
    except:
        patient = None

    observations = Observation.objects.filter(patient__id=patient_id)
    if observations.count():
        agg = observations.aggregate(Max('date'), Min('date'))
        first_observation = agg['date__min']
        last_observation = agg['date__max']
        del agg
        if end_date < first_observation or last_observation < start_date:
            bad_date_range = True
    total_doses_set = set(observations.values_list('total_doses', flat=True))

    try:
        timekeys = set.union(*map(set, map(Observation.get_time_labels, total_doses_set)))
        timekeys = sorted(timekeys, key=TIME_LABELS.index)
    except:
        timekeys = []

    artkeys = ('ART', 'Non ART')
    
    def group_by_is_art_and_time(date):
        grouping = {}
        for artkey in artkeys:
            by_time = {}
            for timekey in timekeys:
                by_time[timekey] = []
            grouping[artkey] = by_time
        obs = observations.filter(date=date)
        for ob in obs:
            grouping['ART' if ob.is_art else 'Non ART'][ob.get_time_label()].append(ob)
        
        return [(ak, [(tk, sorted(grouping[ak][tk], key=lambda x: x.date)[-1:]) for tk in timekeys]) for ak in artkeys]
    
    start_padding = dates[0].weekday()
    end_padding = 7-dates[-1].weekday() + 1
    dates = [None]*start_padding + dates + [None]*end_padding

    dates = [(date, group_by_is_art_and_time(date)) for date in dates]
    weeks = [dates[7*n:7*(n+1)] for n in range(len(dates)/7)]
    
    patients = Patient.objects.filter(observation__in=Observation.objects.all()).distinct()
    
    context = RequestContext(request, locals())
    {
        'weeks' : weeks,
        'patients' : patients,
        'patient' : patient,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render_to_response(template, context)