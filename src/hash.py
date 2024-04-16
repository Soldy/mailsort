import json
import hashlib

        
class Hasher:
    def __init__(self):
        self._rule_string = ''
        self._rules = []
    def add(self, rule: str, values: list[str], target: str):
        self._rules.append({
            'rule' : rule,
            'values' : values,
            'target' : target
        })
    def getHash():
        self._rule_string = json.dumps(self._rules)
        hashlib.sha3_512(
          self._rule_string.encode('utf-8')
        ).hexdigest()
