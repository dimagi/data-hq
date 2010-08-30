from dots.models import *
from BeautifulSoup import BeautifulStoneSoup
import sys, glob
import settings

def data_from_stream(stream):
    soup = BeautifulStoneSoup(stream.read())
    username = soup.find('meta').find('username').renderContents()
    patient_id = soup.find('case').find('case_id').renderContents()
    dots = soup.find('case').find('dots').renderContents()

    return username, patient_id, dots

def run():
    data = {}
    path = settings.RECEIVER_ATTACHMENT_PATH
    filenames = glob.glob(path+'/*.xml')
    for filename in filenames:
        try:
            with open(filename) as stream:
                kwargs = dict(zip(('provider', 'patient', 'json'), data_from_stream(stream)))
            kwargs['submission'] = None
            Observation.from_json(**kwargs)
            print filename
        except:
            continue