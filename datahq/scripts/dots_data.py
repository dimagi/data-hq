from dots.models import *
try:
    from sensitive_dots_data import data
    def run():
        for row in data:
            row['submission'] = None
            Observation.from_json(**row)
except:
    def run():
        print """
create file scripts/sensitive_dots_data.py
and edit so it looks like this:

data = [
    {
        'provider': 'ab123',
        'patient': 'a533faeef5ef54df8f73565056977568',
        'json': 'really long json string'
    },
    ...
]

"""