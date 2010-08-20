from django.db.models import *
from pactpatient.models import Patient
from receiver.models import Submission

import simplejson
import time, datetime

# Create your models here.
ADHERENCE_CHOICES = (
    ("empty", "Empty"),
    ("partial", "Partial"),
    ("full", "Full"),
)
METHOD_CHOICES = (
    ("pillbox", "Pillbox"),
    ("direct", "Direct"),
    ("self", "Self"),
)
class Observation(Model):
    submission = ForeignKey(Submission, null=True)  # fix
    patient = ForeignKey(Patient, null=True)        # fix
    date = DateField(blank=False, null=False)
    is_art = BooleanField() # is Anti Retroviral Treatment
    adherence = CharField(max_length=10, choices=ADHERENCE_CHOICES)
    method = CharField(max_length=10, choices=METHOD_CHOICES)
    note = CharField(max_length=100, null=True, blank=True)
    dose_number = IntegerField()
    total_doses = IntegerField()
    
    def __repr__(self):
        return u"dots.models.Observation(%s)" % (', '.join(
            ["%s=%r" % (field, getattr(self, field)) for field in self._meta.get_all_field_names()]))
    @classmethod
    def from_json(cls, json, patient, submission):
        data = simplejson.loads(json)
        days = data['days']
        last_date = _date_from_string(data['anchor'])
        models = []
        dates = [last_date - datetime.timedelta(n) for n in reversed(range(len(days)))]
        for date, day in zip(dates, days):
            for drug, is_art in zip(day, (False, True)):
                total_doses = len(drug)
                for dose_number, observation in enumerate(drug):
                    try:
                        adherence, method = observation
                        note = None
                    except:
                        adherence, method, note = observation
                    if adherence != 'unchecked':
                        models.append(
                            Observation(
                                submission=submission, patient=patient,
                                date=date, is_art=is_art, adherence=adherence, method=method,
                                note=note, dose_number=dose_number, total_doses=total_doses
                            )
                        )
                    
        return models
def _date_from_string(s):
    """
    >>> _date_from_string("18 Aug 2010 04:00:00 GMT")
    datetime.date(2010, 8, 18)
    """
    return datetime.date(*time.strptime(s, "%d %b %Y %H:%M:%S %Z")[:3])
    
import signals