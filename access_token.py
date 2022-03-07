from datetime import datetime, timezone, timedelta

import jwt
import requests


def create_self_signed_token(audience, sa_email, private_key):
    """
    Generate a self-signed JWT for obtaining access token from Google.
    Refer to
    https://cloud.google.com/functions/docs/securing/authenticating#generating_tokens_manually
    :param audience: the URL/URI to be called later
    :param sa_email: service account email
    :param private_key: private key of the service account key
    :return: a self signed JWT
    """
    current_time = datetime.now(tz=timezone.utc)
    jwt_payload = {
        "target_audience": audience,
        "iss": sa_email,
        "sub": sa_email,
        "exp": current_time + timedelta(seconds=30),
        "iat": current_time,
        "aud": "https://www.googleapis.com/oauth2/v4/token"
    }
    return jwt.encode(jwt_payload, private_key, algorithm="RS256")


def get_access_token(self_signed_token):
    """
    Exchange self-signed JWT for a Google-signed JWT used as access token.
    Refer to
    https://cloud.google.com/functions/docs/securing/authenticating#generating_tokens_manually
    :param self_signed_token :self signed token
    :return: access token
    """
    headers = {
        "Authorization": "Bearer {}".format(self_signed_token),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    body = "grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion={}".format(self_signed_token)
    response = requests.post("https://www.googleapis.com/oauth2/v4/token", headers=headers, data=body)
    response_json = response.json()
    return response_json.get('id_token')
