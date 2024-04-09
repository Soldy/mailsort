import re

address_types = {
    'from':'From',
    'to':'To',
    'cc':'Cc',
    'bcc':'Bcc',
    'replay-to':'Replay-To',
    'in-replay-to':'In-Replay-To'
}

def emailSplitter(email: str)->dict[str, str]:
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

def addressSplitter(address: str)->dict[str, str]:
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

def addressesSplitter(address: str | list[str])->list[dict[str,str]]:
    if str(address) == 'None':
        return []
    out = []
    addresses = []
    if type(address) == list:
        for i in range(len(address)):
            addresses = [*addresses, *str(address[i]).split(',')]
    else:
            addresses = str(address).split(',')
    for address in addresses:
        out.append(addressSplitter(address))
    return out

def addressCheck(sample: str, address: str)->bool:
    splitted = addressesSplitter(address)
    for addr in splitted:
        if sample == addr['address'] :
            return True
    return False


def domainCheck(sample: str, address: str)->bool:
    splitted = addressesSplitter(address)
    for addr in splitted:
        if sample == addr['domain'] :
            return True
    return False

def headerSize(lines: list[str])->int:
    header_size = -1
    for i in range(len(lines)):
        line = (lines[i].rstrip().lstrip()).split(':')
        if len(line) > 1:
            header_size = header_size + 1
        if 2 > len(line):
            return header_size
    return header_size

def headerGet(lines: list[str])->list[str]: 
    return lines[:headerSize(lines)]

def bodyGet(lines: list[str])->list[str]: 
    return lines[headerSize(lines)+1:]

def addressString(addr: dict)->str:
    return (
        ' '.join(addr['name']) +
        '<'+
        addr['address'] +
        '>\n'
    )

def headerAddress(addr: dict)->list[str]:
    types = address_types
    keys = types.keys()
    out = []
    for k in keys:
        if k in addr and addr[k]['email_correct'] == True:
           
            out.append(
              types[k] + ':' +
              addressString(addr[k])
            )
    return out

def headerSubject(sub: str)->str:
    return (
      'Subject: '+
      sub +
      '\n'
    )

def merger(addr: dict, subject: str, body: list[str])->list[str]:
    return [
      *headerAddress(addr),
      subject,
      '\n',
      *body
    ]

