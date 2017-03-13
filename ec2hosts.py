import json 
import subprocess
import operator
import argparse


def main():
    args = parse_args()

    if args.list:
        host_groups = get_ec2_hosts()
        print_ec2_hosts(host_groups)


def parse_args():
    parser = argparse.ArgumentParser(description='Preprocess ec2 described instances.')
    parser.add_argument('--list', action='store_true', help='list all hosts')
    args = parser.parse_args()
    if not (args.list):
        raise Exception('--list argument must be specified.')
    return args


def aws_describe_instances():
    return subprocess.check_output(["aws", "ec2", "describe-instances"])


def get_ec2_hosts():
    def get_instances(reservation): return reservation['Instances']

    def get_dns_name(instance): return instance['PublicDnsName']

    instances_description = aws_describe_instances()

    groups = json.loads(instances_description)

    instances = reduce(operator.add, map(get_instances, groups['Reservations']))

    names = map(get_dns_name, instances)

    return names


def print_ec2_hosts(host_groups):
    print json.dumps(host_groups, indent=2, sort_keys=True)


if __name__ == '__main__':
    main()

