import requests
import cfnresponse
from requests import Response
from cloudflare_provisioner.models import DnsRecord
from cloudflare_provisioner.cloudflare import Cloudflare


def create_dns_record(record: DnsRecord) -> Response:
    """Creates a DNS record

    Args:
        record (DnsRecord): the DNS record to create

    Returns:
        Response: the response from the Cloudflare API
    """
    cf = Cloudflare()
    response = cf.add_dns_record(record)
    return response


def update_dns_record(record_id: str, record: DnsRecord) -> Response:
    """Updates a DNS record

    Args:
        record_id (str): the physical ID of the record
        record (DnsRecord): the data to update

    Returns:
        Response: the response from the Cloudflare API
    """
    cf = Cloudflare()
    response = cf.update_dns_record(record_id, record)
    return response


def delete_dns_record(record_id: str, record: DnsRecord) -> Response:
    """Deletes a DNS record

    Args:
        record_id (str): the physical ID of the record
        record (DnsRecord): the record to delete

    Returns:
        Response: the response from the Cloudflare API
    """
    cf = Cloudflare()
    response = cf.delete_dns_record(record_id, record)
    return response


def handler(event, context):
    """Handles the event sent by Cloudformation when
    a Custom::CloudflareDnsRecord resource is Create, Updated or Deleted

    Args:
        event: the CloudFormation event
        context: the Lambda function context
    """
    action = event['RequestType']
    print(f"Action requested by CloudFormation: {action}")
    record = DnsRecord.from_properties(event['ResourceProperties'])
    print(f"DNS Record: {record}")

    try:
        if action == 'Create':
            response = create_dns_record(record)
            response.raise_for_status()
        elif action == 'Update':
            record_id = event['PhysicalResourceId']
            response = update_dns_record(record_id, record)
            response.raise_for_status()
        else:
            record_id = event['PhysicalResourceId']
            response = delete_dns_record(record_id, record)
            response.raise_for_status()
    except requests.HTTPError as e:
        print(f"Failure {e}")
        print(response.json())
        cfnresponse.send(event, context, cfnresponse.FAILED, response.json())
        exit(1)
    except Exception as e:
        print(f"Failure: {e}")
        cfnresponse.send(event, context, cfnresponse.FAILED, e)
        exit(1)

    record_id = response.json()['result']['id']
    print("Operation performed successfully.")
    print(f"Record ID: {record_id}")
    cfnresponse.send(
        event,
        context,
        cfnresponse.SUCCESS,
        response.json(),
        record_id
    )


# Use this for debugging
if __name__ == '__main__':
    import json
    with open('tests/events/create_dns_record.json', 'r') as fp:
        event = json.load(fp)
        handler(event, None)
