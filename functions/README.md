# Cloud Functions for DNS record set update

## Description

This is the code of the Cloud Function deployment for updaing Cloud DNS's record set.

## Environment

Python 3.9+

## Dependencies
```python
google-api-python-client==2.39.0
```

## Note

- This function is for updating only, and will not work if the record set for the requested hostname does not exist (For obvious reasons)
- **IMPORTANT** - Please ensure only allowing authenticated calls when deploying the function, otherwise very bad things can happen.
- **IMPORTANT** - Please ensure the function's service account does have proper permission to update record sets in Cloud DNS.