# Dynamic Cloud DNS

Simple yet secure Python script to update DNS record in Google Cloud DNS according to your current IP address.

## Features
- Google API Clients & `gcloud` not required
- Updates Cloud DNS record using your current IP address
- Uses service account based authentication

## What does it do exactly?

This script updates a pre-defined DNS type "A" record in Google Cloud DNS according to the current public IP address of the caller. (i.e. your machine)

When combined with a scheduler, this effectively acts as a Dynamic DNS (DDNS) service for Google Cloud DNS.

## Installation

1. Deploy the Cloud Functions (`/functions` of this repo) and grant it permissions to change Cloud DNS resources.
2. Create a service account for the script and grant it permission to invoke Cloud Functions.
3. Generate a new JSON keyfile of the created service account and store it into your machine.
4. Install all necessary python packages (i.e. `pip install -r requirements.txt`)

## How to use

1. Create and fill in the variables required in `.env` file. Refer to `.env.template`.
2. `python3 main.py` (or `python main.py` if you are using `virtualenv`)
3. (optional) Set a crontab to regularly update the DNS record set!