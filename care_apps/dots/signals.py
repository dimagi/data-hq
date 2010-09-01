from corehq.apps.receiver.models import Attachment
from django.db.models.signals import post_save

def process(sender, instance, created, **kwargs):
    print "7788"
post_save.connect(process, sender=Attachment)
