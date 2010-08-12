import csv
from sys import stdin
from pactpatient.models import *

# is there seriously no 'Address 2 - Country'?
HEADER = (
    'PACTID',
    'Given Name',
    'Family Name',
    'CHW Membership',
    'Phone 1 - Type',
    'Phone 1 - Value',
    'Phone 2 - Type',
    'Phone 2 - Value',
    'Phone 3 - Type',
    'Phone 3 - Value',
    'Address 1 - Type',
    'Address 1 - Street',
    'Address 1 - City',
    'Address 1 - Postal Code',
    'Address 1 - Country',
    'Address 2 - Type',
    'Address 2 - Street',
    'Address 2 - City',
    'Address 2 - Postal Code',
    'Provider 1 - Type',
    'Provider 1 - Number',
    'Provider 2 - Type',
    'Provider 2 - Number',
    'Provider 3 - Type',
    'Provider 3 - Number',
    'Provider 4 - Type',
    'Provider 4 - Number',
    'Provider 5 - Type',
    'Provider 5 - Number',
    'Provider 6 - Type',
    'Provider 6 - Number',
    'Provider 7 - Type',
    'Provider 7 - Number',
    'Provider 8 - Type',
    'Provider 8 - Number',
    'Provider 9 - Type',
    'Provider 9 - Number',
)

def run():
    #stdin = open('PACT-csv/patient-data.csv')
    reader = csv.reader(stdin)

    rows = iter(reader)
    header = rows.next()

    if tuple(header) != tuple(HEADER):
        raise Exception("incorrect header")

    patients = []

    structure = (
        ('phone', 3, ('type', 'value')),
        ('address', 2, ('type', 'street', 'city', 'postal code', 'country')),
        ('provider', 9, ('type', 'number')),
    )
    def normalize(s):
        return s.lower().replace(' ',  '_')
    
    for row in rows:
        data = dict(zip(map(normalize, HEADER), row))
        patient = dict()
        for key in map(normalize, ('PACTID', 'Given Name', 'Family Name', 'CHW Membership')):            
            patient[key] = data[key]        
        for key, N, fields in structure:
            patient[key] = []
            for i in range(1,N+1):
                format = "%s %d - %%s" % (key, i)                             
                patient[key].append(tuple([data.get(normalize(format % f), '') for f in fields]))
        
        print patient
        patients.append(patient)

    # patients = [{'pactid':123, 'phone':[{'type':...]}]
    def get_user(first, last):
        users = User.objects.filter(first_name=first_name, last_name=last_name)
        if users.count():
            if users.count() > 1:
                print "Multiple users named %s %s" % (first_name, last_name)
            # This is not a smart way to deal with two people with the same name
            user = users[0]
        else:
            username = '_'.join(map(normalize, (first_name, last_name)))
            while User.objects.filter(username=username):
                username += '_'
            user = User.objects.create_user(username, '', 'demo')
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        return user
    
    for patient in patients:        
        first_name, last_name = patient['given_name'], patient['family_name']
        user = get_user(first_name, last_name)
        
        phones = patient['phone']
        addresses = patient['address']
        chw_membership = patient['chw_membership']        
        providers = patient['provider']
        
        
        
        try:
            pt_model = Patient.objects.get(user=user, sex="f")
        except:
            pt_model = Patient(user=user, sex="f")
        
        pt_model.notes = str([chw_membership,providers])
        pt_model.save()
#        patient.user = user
#        patient.sex="f"
#        patient.save()
        
        
        
        
        
        for phone in phones:                    
            ident = phone[0]
            val = phone[1]
            try:                
                phone_type = IdentifierType.objects.get(description="Phone Number", shortname=ident)
            except:
                phone_type = IdentifierType(description="Phone Number", shortname=ident)
                phone_type.save()
                
            try:                            
                phone_value = PatientIdentifier.objects.get(id_type=phone_type, id_value=val)
            except:
                phone_value = PatientIdentifier(id_type=phone_type, id_value=val)
                phone_value.save()
                
            
            if pt_model.identifiers.all().filter(id_type=phone_type, id_value=val).count() == 0:
                pt_model.identifiers.add(phone_value)
                print "adding phone: " + val

        for addr in addresses:            
            if addr[0] == '' and addr [1] == '' and addr[2] == '':
                continue
            addr_model = Address.objects.get_or_create(type=addr[0], street1=addr[1], city=addr[2], state="MA", postal_code=addr[3])[0]            
            if pt_model.address.all().filter(id=addr_model).count() == 0:
                print "adding address: " + addr_model.type + " " + addr_model.street1
                pt_model.address.add(addr_model)
            
       
                
        
        #dmyung:  ok we're just going guns a blazing to make our pact users, surely we will make this cleaner for future generations
        try:
            pact_identifier_type  = IdentifierType.objects.get(description="PACT Internal Identifier", shortname="PACTID")
        except:
            pact_identifier_type  = IdentifierType(description="PACT Internal Identifier", shortname="PACTID")
            pact_identifier_type.save()
                       
        if pt_model.identifiers.all().filter(id_type=pact_identifier_type, id_value=patient['pactid']).count() == 0:
            try:
                pact_id = PatientIdentifier.objects.get(id_type=pact_identifier_type, id_value=patient['pactid'])
            except:
                pact_id = PatientIdentifier(id_type=pact_identifier_type, id_value=patient['pactid'])
                pact_id.save()
            pt_model.identifiers.add(pact_id)
                
        
        
        
        
        
        
        
