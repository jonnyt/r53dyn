# https://runnable.com/docker/python/dockerize-your-python-application

import os
import time
import helpers

working_path = os.path.dirname(os.path.abspath(__file__))


def init():

    if 'AWS_A_RECORD_NAME' not in os.environ:
        raise EnvironmentError(
            "Environment variable AWS_A_RECORD_NAME is missing!")

    if 'AWS_ACCESS_KEY_ID' not in os.environ:
        raise EnvironmentError(
            "Environment variable AWS_ACCESS_KEY_ID is missing!")

    if 'AWS_SECRET_ACCESS_KEY' not in os.environ:
        raise EnvironmentError(
            "Environment variable AWS_SECRET_ACCESS_KEY is missing!")

    if 'AWS_HOSTED_ZONE_ID' not in os.environ:
        raise EnvironmentError(
            "Environment variable AWS_HOSTED_ZONE_ID is missing!")

    if 'SLEEP_SEC' not in os.environ:
        os.environ['SLEEP_SEC'] = '360'


def main():

    init()

    # on start always update our IP
    ip = helpers.get_public_ip()
    print(f"Public IP is {ip}")
    # update ip

    while (True):
        record_name = os.environ['AWS_A_RECORD_NAME']
        zone_id = os.environ['AWS_HOSTED_ZONE_ID']
        ip = helpers.get_public_ip()
        print(f"Public IP is {ip}")
        r53_ip = helpers.get_r53_a_record_val(zone_id, record_name)
        print(f"Route 53 IP is {r53_ip}")

        if (ip != r53_ip):
            print(f"Updating IP")
            update_file = helpers.generate_upsert_json(
                ip, record_name, working_path)
            res = helpers.update_r53_a_record(zone_id, update_file)
            print(f"Route 53 update returned {res['ChangeInfo']['Status']}")

        time.sleep(int(os.environ['SLEEP_SEC']))


if __name__ == "__main__":
    main()
