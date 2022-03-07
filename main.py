import json

from access_token import create_self_signed_token, get_access_token
import requests

from environs import Env

env = Env()
env.read_env()

# required variables
cf_endpoint = env("FUNCTION_URL")
service_account_keyfile = env("SERVICE_ACCOUNT_KEYFILE")
hostname = env("HOSTNAME")
project = env("PROJECT")
zone = env("ZONE")


def main():
    # open keyfile and read content
    with open(service_account_keyfile, 'r') as f:
        credentials = json.loads(f.read())

    sa_email = credentials.get('client_email')
    private_key = credentials.get('private_key')

    # get access token
    ss_token = create_self_signed_token(cf_endpoint, sa_email, private_key)
    access_token = get_access_token(ss_token)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    body = {
        "project": project,
        "zone": zone,
        "hostname": hostname
    }

    # send request to cloud function to update Cloud DNS record set
    response = requests.post(cf_endpoint, headers=headers, json=body)
    print(response)
    print(response.content)
    print("done.")


if __name__ == "__main__":
    main()
