import hashlib
from domain.models import Domain, Membership
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

def create_user_and_domain(username='brian', 
                           password='test',
                           domain_name='mockdomain'):
    """Creates a domain 'mockdomain' and a web user with name/pw 
       'brian'/'test'.  Returns these two objects in a tuple 
       as (domain, user).  The parameters are configurable."""
    try:
        domain = Domain.objects.get(name=domain_name)
        print "WARNING: tried to create domain %s but it already exists!" % domain_name
        print "Are all your tests cleaning up properly?"
    except Domain.DoesNotExist:
        # this is the normal case
        domain = Domain(name=domain_name, is_active=True)
        domain.save()
    
    try:
        user = User.objects.get(username=username)
        print "WARNING: tried to create user %s but it already exists!" % username
        print "Are all your tests cleaning up properly?"
        # update the pw anyway
        user.password = _get_salted_pw(password)
        user.save()
    except User.DoesNotExist:
        user = User()
        user.username = username
        # here, we mimic what the django auth system does
        # only we specify the salt to be 12345
        user.password = _get_salted_pw(password)
        
        user.save()
        
        # update the domain mapping using the Membership object
        mem = Membership()
        mem.domain = domain         
        mem.member_type = ContentType.objects.get_for_model(User)
        mem.member_id = user.id
        mem.is_active = True
        mem.save()
                
    return (user, domain)
                                
def _get_salted_pw(password, salt="12345"):
    hashed_pass = hashlib.sha1(salt+password).hexdigest()
    return 'sha1$%s$%s' % (salt, hashed_pass)
        