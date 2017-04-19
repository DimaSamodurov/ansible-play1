import json
import subprocess
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

# Plugin filters out EC2 instances based on tags match criteria
# {{ lookup('ec2instances', {'tags': ['test1']}) }}.
class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        meta = self.inventory_meta(variables["inventory_file"])
        #import pdb; pdb.set_trace()
        return []


    def inventory_meta(self, inventory_file):
        return json.loads(subprocess.check_output([inventory_file, "--list"]))