import re

def emailSplitter(email:str)->dict:
    out = {
        'alias':'',
        'domain':'',
        'email_correct':False
    }
    if email == '':
        return out
    splitted = email.split('@')
    if len(splitted) > 0:
        out['alias'] = splitted[0]
    if len(splitted) > 1:
        out['domain'] = splitted[1]
    if len(splitted) == 2:
        out['email_correct'] = True
    return out

def addressSplitter(address:str)->dict:
    out = {
        'name':[],
        'address':''
    }
    address = re.sub('"', "", str(address))
    splitted = address.split(' ')
    out['address'] = re.sub("<|>", "", splitted[len(splitted) - 1])
    for i in range(len(splitted)-1):
        out['name'].append(splitted[i])
    return out | emailSplitter(out['address'])

def addressesSplitter(address:str)->list:
    if str(address) == 'None':
        return []
    out = []
    addresses = str(address).split(',')
    for addr in addresses:
        out.append(addressSplitter(addr))
    return out
