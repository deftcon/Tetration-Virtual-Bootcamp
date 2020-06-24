#!/bin/bash
# /home/ciscolab/ansible_ping.sh
/usr/bin/ansible centos -m ping -i /opt/ansible-tetration-sensor/inventory/hosts -e host_key_checking=False
/usr/bin/ansible win -m win_ping -i /opt/ansible-tetration-sensor/inventory/hosts