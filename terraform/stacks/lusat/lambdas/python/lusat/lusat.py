#! /usr/bin/env python

import argparse
from datetime import datetime
from modules.collector import EC2Collector, ENICollector, VPCCollector, SGCollector, LBCollector


def handler(event, context):
    print("Received event: {}".format(event))
    print(str(datetime.now()) + ' cloud-lusat running for: '+str(event))
    SGCollector(event)
    ENICollector(event)
    VPCCollector(event)
    EC2Collector(event)
    LBCollector(event)
    print(str(datetime.now()) + ' cloud-lusat DONE for: '+str(event))


def main(args):
    if args.get('inv') == 'ec2':
        print(str(datetime.now()) + ' cloud-lusat running for: '+str(args))
        EC2Collector(args)
        print(str(datetime.now()) + ' cloud-lusat DONE for: '+str(args))

    if args.get('inv') == 'vpc':
        print(str(datetime.now()) + ' cloud-lusat running for: '+str(args))
        VPCCollector(args)
        print(str(datetime.now()) + ' cloud-lusat DONE for: '+str(args))

    if args.get('inv') == 'eni':
        print(str(datetime.now()) + ' cloud-lusat running for: '+str(args))
        ENICollector(args)
        print(str(datetime.now()) + ' cloud-lusat DONE for: '+str(args))

    if args.get('inv') == 'sg':
        print(str(datetime.now()) + ' cloud-lusat running for: '+str(args))
        SGCollector(args)
        print(str(datetime.now()) + ' cloud-lusat DONE for: '+str(args))

    if args.get('inv') == 'lb':
        print(str(datetime.now()) + ' cloud-lusat running for: '+str(args))
        LBCollector(args)
        print(str(datetime.now()) + ' cloud-lusat DONE for: '+str(args))

    if args.get('inv') == 'all':
        print(str(datetime.now()) + ' cloud-lusat running for: '+str(args))
        SGCollector(args)
        ENICollector(args)
        VPCCollector(args)
        EC2Collector(args)
        LBCollector(args)
        print(str(datetime.now()) + ' cloud-lusat DONE for: '+str(args))


if __name__ == '__main__':
    print("Automated tool to get inventory information and push to ELK 'inventory' index.")
    Dago_parser = argparse.ArgumentParser()
    Dago_parser.version = 'version: 1.0 - cloud-lusat Security Inventory Collector'

    Dago_parser.add_argument(
        '-a', help='aws account to use', dest='account_id', type=str, required=True)
    Dago_parser.add_argument(
        '-r', help='aws role to assume', dest='role_assume', type=str, required=True)
    Dago_parser.add_argument('-inv', action='store', choices=[
                             'ec2', 'vpc', 'sg', 'eni', 'iam', 'all', 'lb'], help='type of inventory that you whant to collect', type=str)
    Dago_parser.add_argument('-v', action='version',
                             help="show version script")

    args = Dago_parser.parse_args()
    event_map = {'account_id': args.account_id,
                 'role_assume': args.role_assume, 'inv': args.inv}

    main(event_map)
