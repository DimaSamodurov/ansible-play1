#!/usr/bin/env python

import json
import subprocess
import operator
import argparse


class Ec2Hosts(object):
    def instances_description(self):
        if not hasattr(self, '_instances'):
            self._instances = json.loads(self.aws_describe_instances())
        return self._instances

    def aws_describe_instances(self):
        return subprocess.check_output(["aws", "ec2", "describe-instances"])

    def ec2_hosts(self):
        def get_instances(reservation): return reservation['Instances']

        def get_dns_name(instance): return instance['PublicDnsName']

        groups = self.instances_description()

        instances = reduce(operator.add, map(get_instances, groups['Reservations']))

        names = map(get_dns_name, instances)

        return names
    
    # Returns host variables in format {host1: {variables}, host2: {variables}}
    def hostvars(self):
        def get_instances(reservation): return reservation['Instances']

        def get_dns_name(instance): return instance['PublicDnsName']

        groups = self.instances_description()

        instances = reduce(operator.add, map(get_instances, groups['Reservations']))

        arr = {}
        for i in instances:
            arr[i['PublicDnsName']] = i

        return arr
        

    def get_ec2_metadata(self):
        meta = {
            "all": self.ec2_hosts(),
            "_meta": {
                "hostvars": self.hostvars()
            }
        }
        return meta


def parse_args():
    parser = argparse.ArgumentParser(description='Dynamic Inventory retrieving description of EC2 instances.')
    parser.add_argument('--list', action='store_true', help='list all hosts')
    args = parser.parse_args()
    if not args.list:
        parser.print_help()
    return args


def print_ec2_hosts(host_groups):
    print json.dumps(host_groups, indent=2, sort_keys=True)


def main():
    args = parse_args()

    if args.list:
        print_ec2_hosts(Ec2Hosts().get_ec2_metadata())


if __name__ == '__main__':
    main()
