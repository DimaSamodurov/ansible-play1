import json 
import subprocess
import operator


def get_ec2_hosts():
    def get_instances(reservation): return reservation['Instances']

    def get_dns_name(instance): return instance['PublicDnsName']

    instances_description = subprocess.check_output(["aws", "ec2",  "describe-instances"])

    dict = json.loads(instances_description)

    instances = reduce(operator.add, map(get_instances, dict['Reservations']))

    names = map(get_dns_name, instances)

    return names

print get_ec2_hosts()