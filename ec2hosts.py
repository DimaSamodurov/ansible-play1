#!/usr/bin/env python

import json
import subprocess
import operator
import argparse


class Ec2Hosts(object):
    def aws_instances_description(self):
        if not hasattr(self, 'instances'):
            self.instances = json.loads(self.aws_describe_instances())
        return self.instances

    def aws_describe_instances(self):
        return subprocess.check_output(["aws", "ec2", "describe-instances"])

    def get_ec2_hosts(self):
        def get_instances(reservation): return reservation['Instances']

        def get_dns_name(instance): return instance['PublicDnsName']

        groups = self.aws_instances_description()

        instances = reduce(operator.add, map(get_instances, groups['Reservations']))

        names = map(get_dns_name, instances)

        return names

    def get_ec2_metadata(self):
        meta = {
            "all": self.get_ec2_hosts(),
            "_meta": self.aws_instances_description()
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
