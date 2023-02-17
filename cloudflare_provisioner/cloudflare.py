import os
import json
import requests
from requests import Response
from cloudflare_provisioner.models import DnsRecord


BASE_URL = 'https://api.cloudflare.com/client/v4'


class Cloudflare:
    """A Cloudflare API client
    """
    def __init__(self):
        self.token = self._get_api_token()
        self.headers = {'Authorization': f"Bearer {self.token}"}

    def _get_api_token(self) -> str:
        headers = {
            "X-Aws-Parameters-Secrets-Token": os.environ.get('AWS_SESSION_TOKEN')
        }
        secretsmanager_extension_endpoint = "http://localhost:2773/secretsmanager/get?secretId="
        secret_name = os.getenv('CLOUDFLARE_API_TOKEN_SECRET_NAME')

        response = requests.get(
            secretsmanager_extension_endpoint + secret_name,
            headers=headers
        )
        secret_string = json.loads(response.text)['SecretString']
        return secret_string

    def add_dns_record(self, record: DnsRecord) -> Response:
        """Adds a DNS record

        Args:
            record (DnsRecord): the record to add

        Returns:
            Response: the response
        """
        print("adding a dns record")
        endpoint = f"/zones/{record.zone_id}/dns_records"
        resp = requests.post(
            BASE_URL + endpoint,
            json=record.to_json(),
            headers=self.headers
        )
        return resp

    def delete_dns_record(self, record_id: str, record: DnsRecord) -> Response:
        """Deletes a DNS record

        Args:
            record_id (str): the record id
            record (DnsRecord): the record to delete

        Returns:
            Response: the response
        """
        print("deleting a dns record")
        endpoint = f"/zones/{record.zone_id}/dns_records/{record_id}"
        resp = requests.delete(
            BASE_URL + endpoint,
            headers=self.headers
        )
        return resp

    def update_dns_record(self, record_id: str, record: DnsRecord) -> Response:
        """Updates a DNS record

        Args:
            record_id (str): the record id
            record (DnsRecord): the record to update

        Returns:
            Response: the response
        """
        print("updating a dns record")
        endpoint = f"/zones/{record.zone_id}/dns_records/{record_id}"
        resp = requests.put(
            BASE_URL + endpoint,
            headers=self.headers,
            json=record.to_json()
        )
        return resp
