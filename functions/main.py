from googleapiclient import discovery


def update_dns_record(request):
    """
    Update DNS record set to HTTP request with valid request body.
    This is for updating only, and will not work if the record set
    for the requested hostname does not exist (For obvious reasons)
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    src_ip = request.headers.get("X-Forwarded-For")
    if not src_ip:
        return "No IP provided in headers", 422

    request_json = request.get_json()
    if not request_json:
        return "a request body must be provided", 400

    project = request_json.get("project")
    managed_zone = request_json.get("zone")
    hostname = request_json.get("hostname")

    if not (project and managed_zone and hostname):
        return "project, managed_zone & hostname must all be provided", 400

    hostname_with_dot = hostname.rstrip(".") + "."

    record_set = {
        "kind": "dns#resourceRecordSet",
        "name": hostname_with_dot,
        "type": "A",
        "ttl": 300,
        "rrdatas": src_ip
    }

    try:
        service = discovery.build('dns', 'v1')
        request = service.resourceRecordSets().patch(project=project, managedZone=managed_zone, type="A", name=hostname_with_dot, body=record_set)
        response = request.execute()

        return response, 200
    except Exception as e:
        return "Error updating record. Reason: {}".format(str(e)), 500
