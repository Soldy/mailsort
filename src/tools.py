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

def addressFix(addr_: str|dict)->dict[str, str]:
    addr = {}
    if type(addr_) is str:
        addr = addressSplitter(addr_)
    elif  type(addr_) is dict:
        addr = addr_
    return addr

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

def addressFormatCheck(addr_: str|dict[str,str|bool|list[str]])->bool:
    req_keys = ['name','address', 'alias','domain','email_correct']
    addr = addressFix(addr_)
    for k in req_keys:
        if k not in addr:
           return False
    return True

def addressesToList(addr_list_: list[str|dict])->list:
    out = []
    for i in addr_list_:
        addr = addressFix(i)
        if addressFormatCheck(addr):
            out.append(addr)
    return out

def addressesToDict(addr_list_: list[str|dict])->dict:
    out = {}
    serial = 0
    for i in addressesToList(addr_list_):
        out[str(serial)] = i
        serial = serial + 1
    return out

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

def headerSubjectGet(lines: list[str])->str:
    for i in range(len(lines)):
        line = (lines[i].rstrip().lstrip()).split(':')
        if line[0][:7] == 'Subject':
           del line[0]
           return (':'.join(line)).rstrip().lstrip()
    return ''

def headerAddressGet(lines: list[str])->dict[str,dict[str,str|int]]:
    keys = address_types.keys()
    types = address_types
    out = {
       'line':{}
    }
    print(keys)
    finded = 0
    for k in keys:
        out['line'][k] = -1
    for i in range(len(lines)):
        line = (lines[i].rstrip().lstrip()).split(':')
        for k in keys:
            t = types[k]
            if line[0][:len(t)] == t and out['line'][k] == -1:
                out[k] = addressSplitter(line[1].rstrip().lstrip())
                out['line'][k] = i
                finded = finded + 1
            if finded == len(keys):
                 break
    return out

def headerGet(lines: list[str])->list[str]: 
    return lines[:headerSize(lines)]

def bodyGet(lines: list[str])->list[str]: 
    return lines[headerSize(lines)+1:]

def addressString(addr: dict)->str:
    return (
        ' '.join(addr['name']) +
        ' <'+
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
