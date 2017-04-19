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
# {{ lookup('ec2instances', {'Project': 'cms'}) }}.
class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        meta = self.inventory_meta(variables["inventory_file"])
        hostvars = meta['_meta']['hostvars']

        matched_hosts = [k for k, v in hostvars.iteritems() if self.tags_matched(terms, v['Tags'])]

        return matched_hosts

    def tags_matched(self, terms, tags):
        for term in terms:
            for name, value in term.iteritems():
                for tag in tags:
                    if tag['Key'] == name and tag['Value'] == value:
                        return True
        return False

    def inventory_meta(self, inventory_file):
        return json.loads(subprocess.check_output([inventory_file, "--list"]))
