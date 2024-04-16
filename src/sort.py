import tools
import mailbox




class Sort:
    def __init__(self):
        self._mailboxes = {}
        self._filters = []
        self._rooler = {
            'EmailFrom'            : self._EmailFrom,
            'EmailTo'              : self._EmailTo,
            'EmailCc'              : self._EmailCc,
            'EmailToCc'            : self._EmailToCc,
            'DomainFrom'           : self._DomainFrom,
            'DomainTo'             : self._DomainTo,
            'DomainCc'             : self._DomainCc,
            'DomainToCc'           : self._DomainToCc,
            'EmailFromEmailTo'     : self._EmailFromEmailTo,
            'EmailFromEmailCc'     : self._EmailFromEmailCc,
            'EmailFromEmailToCc'   : self._EmailFromEmailToCc,
            'EmailFromDomainTo'    : self._EmailFromDomainTo,
            'EmailFromDomainCc'    : self._EmailFromDomainCc,
            'EmailFromDomainToCc'  : self._EmailFromDomainToCc,
            'DomainFromEmailTo'    : self._DomainFromEmailTo,
            'DomainFromEmailCc'    : self._DomainFromEmailCc,
            'DomainFromEmailToCc'  : self._DomainFromEmailToCc,
            'DomainFromDomainTo'   : self._DomainFromDomainTo,
            'DomainFromDomainCc'   : self._DomainFromDomainCc,
            'DomainFromDomainToCc' : self._DomainFromDomainToCc
        }
    def add(self, rule: str, values: list[str], target: str):
        self._filters.append({
            'rule' : rule,
            'values' : values,
            'target' : target
        })
        self._openBox(target)
    def addComplex(self, rule: str, values: list[list[str]], target):
        for first in range(len(values[0])):
            for second in range(len(values[1])):
                self.add(rule, [values[0][first], values[1][second]], target)

    def _openBox(self, box: str):
        if box not in self._mailboxes:
            self._mailboxes[box] = mailbox.Maildir(box, factory=None)
    def _copy (self, key: str, source: str, target: str):
        self._mailboxes[source].lock()
        self._mailboxes[target].lock()
        self._mailboxes[target].add(self._mailboxes[source][key])
        self._mailboxes[source].remove(key)
        self._mailboxes[source].flush()
        self._mailboxes[target].flush()
        self._mailboxes[source].unlock()
        self._mailboxes[target].unlock()
    def _EmailFrom(self, values: list[str], details: dict[str, str])->bool:
        return tools.addressCheck(values[0], details['from'])
    def _EmailTo(self, values: list[str], details: dict[str, str])->bool:
        return tools.addressCheck(values[0], details['to'])
    def _EmailCc(self, values: list[str], details: dict[str, str])->bool:
        return tools.addressCheck(values[0], details['cc'])
    def _EmailToCc(self, values: list[str], details: dict[str, str])->bool:
        return tools.addressCheck(values[0], [details['to'], details['cc']])
    def _DomainFrom(self, values: list[str], details: dict[str, str])->bool:
        return tools.domainCheck(values[0], details['from'])
    def _DomainTo(self, values: list[str], details: dict[str, str])->bool:
        return tools.domainCheck(values[0], details['to'])
    def _DomainCc(self, values: list[str], details: dict[str, str])->bool:
        return tools.domainCheck(values[0], details['cc'])
    def _DomainToCc(self, values: list[str], details: dict[str, str])->bool:
        return tools.domainCheck(values[0], [details['to'], details['cc']])
    def _EmailFromEmailTo(self, values: list[str], details: dict[str, str])->bool:
        if tools.addressCheck(values[0], details['from']):
            return tools.addressCheck(values[1], details['to'])
        return False
    def _EmailFromEmailCc(self, values: list[str], details: dict[str, str])->bool:
        if tools.addressCheck(values[0], details['from']):
            return tools.addressCheck(values[1], details['cc'])
        return False
    def _EmailFromEmailToCc(self, values: list[str], details: dict[str, str])->bool:
        if tools.addressCheck(values[0], details['from']):
            return tools.addressCheck(values[1], [details['to'], details['cc']])
        return False
    def _DomainFromEmailTo(self, values: list[str], details: dict[str, str])->bool:
        if tools.domainCheck(values[0], details['from']):
            return tools.addressCheck(values[1], details['to'])
        return False
    def _DomainFromEmailCc(self, values: list[str], details: dict[str, str])->bool:
        if tools.domainCheck(values[0], details['from']):
            return tools.addressCheck(values[1], details['cc'])
        return False
    def _DomainFromEmailToCc(self, values: list[str], details: dict[str, str])->bool:
        if tools.domainCheck(values[0], details['from']):
            return tools.addressCheck(values[1], [details['to'], details['cc']])
        return False
    def _EmailFromDomainTo(self, values: list[str], details: dict[str, str])->bool:
        if tools.domainCheck(values[0], details['from']):
            return tools.addressCheck(values[1], details['to'])
        return False
    def _EmailFromDomainCc(self, values: list[str], details: dict[str, str])->bool:
        if tools.domainCheck(values[0], details['from']):
            return tools.addressCheck(values[1], details['cc'])
        return False
    def _EmailFromDomainToCc(self, values: list[str], details: dict[str, str])->bool:
        if tools.domainCheck(values[0], details['from']):
            return tools.addressCheck(values[1], [details['to'], details['cc']])
        return False
    def _DomainFromDomainTo(self, values: list[str], details: dict[str, str])->bool:
        if tools.domainCheck(values[0], details['from']):
            return tools.domainCheck(values[1], details['to'])
        return False
    def _DomainFromDomainCc(self, values: list[str], details: dict[str, str])->bool:
        if tools.domainCheck(values[0], details['from']):
            return tools.domainCheck(values[1], details['cc'])
        return False
    def _DomainFromDomainToCc(self, values: list[str], details: dict[str, str])->bool:
        if tools.domainCheck(values[0], details['from']):
            return tools.domainCheck(values[1],[details['to'], details['cc']])
        return False
    def _checks(self, box: str, key: str)->str:
        details = {
            'from' : self._mailboxes[box][key]['from'],
            'to'   : self._mailboxes[box][key]['to'],
            'cc'   : self._mailboxes[box][key]['cc'],
            'bcc'  : self._mailboxes[box][key]['bcc']
        }
        for rule in range(len(self._filters)):
            if self._rooler[self._filters[rule]['rule']](self._filters[rule]['values'], details):
                return self._filters[rule]['target']
        return box
    def filtering(self, box: str)->int:
        self._openBox(box)
        count = 0
        serial = 0
        for key in self._mailboxes[box].iterkeys():
            result = self._checks(box, key)
            serial += 1
            if result != box:
                self._copy(key, box, result)
                count += 1
        return count
