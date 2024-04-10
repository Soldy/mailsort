import sys
import time
import mailsort.tools as tools

def addressInput(type_:str, addr_list_:dict[str,str])->dict[str,str]:
    correct = False 
    out = ''
    while not correct:
        print('Select '+type_+'address:\n')
        for i in addr_list_.keys():
            print(i)
            print(
              ' '+
              i+
              '. '+
              tools.addressString(addr_list_[i])
            )
        resp = input(type_+' :')
        if resp in addr_list_.keys():
           out = addr_list_[resp]
        else: 
           out = tools.addressSplitter(resp)
        correct = out['email_correct']
    return out

def loadMail(file_name_:str)->list[str]:
    lines = []
    print(file_name_)
    with open(file_name_, "r") as f:
        lines = f.readlines()
        print(lines)
        f.close()
    return lines

def saveMail(file_name_:str, full_mail_:list[str]):
    with open(file_name_, "w") as f:
       for line in full_mail_:
           f.write(line)
       f.close()
