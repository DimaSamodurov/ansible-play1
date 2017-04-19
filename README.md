# Creating sample Dynamic Inventory and a plugin for Ansible

## Configuration
Sample uses your local AWS configuration, e.g. `~/.aws/config` and `~/.aws/credentials`

## Inventory usage

    # To display the help
    ./ec2hosts.py
    # To describe aws instances
    ./ec2hosts.py --list


## Plugin usage

Within the playbook you can filter out hosts to be processed:

    hosts: "{{ lookup('ec2instances', {'Project': 'MyProject'}) }}"

## Run the playbook

    ansible-playbook hello-playbook.yml -vv



