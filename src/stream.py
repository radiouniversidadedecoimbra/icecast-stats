import requests
import base64
import xmltodict
import json

from collections import Counter

class Stream:

    def __init__(self, url, mount, port=80, prefix="http"):
        self.url = url
        self.mount = mount
        self.port = port
        self.prefix = prefix

        self.usr = "USER"
        self.psw = "PASS"

    def request_status(self):
        """Get status from Icecast2 server"""

        # Create Base64 key for request header
        key_str = f"{self.usr}:{self.psw}"
        key_b64 = base64.b64encode(bytes(key_str, 'utf-8'))
        key = key_b64.decode('utf-8')

        # Define request header
        hdr = {"Authorization": f"Basic {key}"}

        # Request URL
        url = f"{self.prefix}://{self.url}:{self.port}/admin/listclients?mount={self.mount}"

        return requests.get(url, headers=hdr)

       # self.list_dict = xmltodict.parse(r.text)
        # data_dict = xmltodict.parse(r.text)
       # data_json = json.loads(json.dumps(data_dict))
        #print(data_json)

    @property
    def status_dict(self):
        r = self.request_status()
        return xmltodict.parse(r.text)

    @property
    def listeners_ip(self):
        """List of IPs of connected listeners"""
        source_dict = self.status_dict.get('icestats', {}).get('source', {})
        n_list = int(source_dict.get("Listeners"))
        if n_list != 0:
            listeners = source_dict.get('listener', {})
            if n_list == 1:
                return [listeners["IP"]]
            else:
                return [l["IP"] for l in listeners]
        else:
            return []

    @property
    def listeners_total(self):
        """Number of connected listeners"""
        return int(self.status_dict['icestats']['source']['Listeners'])

    @staticmethod
    def request_location(ip):
        """Request location of listener from IP"""

        # Using greegeoip.app API
        url = f"https://freegeoip.app/json/{ip}"

        hdr = {
            'accept': "application/json",
            'content-type': "application/json"
        }

        request = requests.request("GET", url, headers=hdr)

        return request.json()

    @property
    def listeners_locations(self):
        listeners_loc_json = [self.request_location(ip) for ip in self.listeners_ip]
        countries = [l['country_name'] for l in listeners_loc_json]
        return dict(Counter(countries))

if __name__ == '__main__':
    url = "stream.ruc.pt"
    mount = "/high"

    stream = Stream(url, mount)
    print(stream.status_dict)
    print(stream.listeners_ip)


    # lip = [stream.request_location(ip) for ip in stream.listeners_ip]
    # print(lip)
