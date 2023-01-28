import google.auth
import os
from google.cloud import storage
from google.cloud import exceptions
import json
import base64

class GcpCache(object):
    """
    Cache implemented using a GCP Bucket.
    
    """
    def __init__(self):
        service_account_base64 = os.environ.get("GCP_CACHE_SERVICE_ACCOUNT_BASE64")
        if not service_account_base64:
            raise Exception("GCP_CACHE_SERVICE_ACCOUNT_BASE64 not set")
        service_account = base64.b64decode(service_account_base64)
        if not service_account:
            raise Exception("Service account not decodable")
        service_account_dict = json.loads(service_account)
        credentials = google.oauth2.service_account.Credentials.from_service_account_info(
            service_account_dict)
        self.client = storage.Client(project=credentials.project_id, credentials=credentials)
        self.bucket = self.client.bucket('gcp-chat-cache')
        
        
    def set(self, key, value, ttl):
        """
        TODO: TTL is ignored for now
        """
        blob = self.bucket.blob('{}.txt'.format(self._format_key(key)))
        blob.upload_from_string(value)
    
    def get(self, key):
        try:
            return self.bucket.blob('{}.txt'.format(self._format_key(key))).download_as_string()
        except exceptions.NotFound:
            # expected if element not in cache
            return None
    
    def exists(self, key):
        return self.bucket.blob('{}.txt'.format(self._format_key(key))).exists()
    
    def _format_key(self, key):
        return key.replace(" ", "_")
