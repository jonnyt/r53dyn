import boto3
import subprocess
import re
import os
import json


def get_public_ip():
    result = subprocess.run(['curl', '-s', 'http://checkip.dyndns.org/'],
                            stdout=subprocess.PIPE).stdout.decode('utf-8')
    m = re.search(r'^.*: ((\d+\.?)+)', result)
    ip = m.group(1)
    return ip


def get_r53_a_record_val(zone_id, name):
    client = boto3.client('route53')
    try:
        response = client.list_resource_record_sets(
            HostedZoneId=zone_id,
            StartRecordName=name,
            StartRecordType='A'
        )

        # filter on A records
        a_recordsets = [
            set for set in response['ResourceRecordSets'] if set['Type'] == 'A']
        # we only support a single resource record at the moment
        first_record = a_recordsets[0]['ResourceRecords'][0]
        return first_record['Value']
    except Exception as e:
        print(e)


def generate_upsert_json(ip, record_name, path):
    template = path + '/template_A.json'

    with open(template, 'r') as file:
        json_data = json.load(file)
        json_data['Changes'][0]['ResourceRecordSet']['Name'] = record_name
        json_data['Changes'][0]['ResourceRecordSet']['ResourceRecords'][0]['Value'] = ip

    update_file = f"{path}/{ip}.json"

    with open(update_file, 'w+') as update:
        json.dump(json_data, update)

    return update_file


def update_r53_a_record(zone_id, path):
    client = boto3.client('route53')
    try:
        with open(path, 'r') as file:
            json_data = json.load(file)
            response = client.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch=json_data
            )
        print(response)
        return response
    except Exception as e:
        print(e)
