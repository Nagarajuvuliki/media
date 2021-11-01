import requests
from django.http import HttpResponse
import json

import requests

url = "https://live-server-2553.wati.io/api/v1/getContacts"

headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0MzE5NjQxMC1iNDA2LTQ0ZDktOWFiYy1lZTE5ZmZiZWMzNWEiLCJ1bmlxdWVfbmFtZSI6IlNvbmFtQGtzbGVnYWwuY28uaW4iLCJuYW1laWQiOiJTb25hbUBrc2xlZ2FsLmNvLmluIiwiZW1haWwiOiJTb25hbUBrc2xlZ2FsLmNvLmluIiwiYXV0aF90aW1lIjoiMDgvMDMvMjAyMSAwNToyOToxNCIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFETUlOSVNUUkFUT1IiLCJleHAiOjI1MzQwMjMwMDgwMCwiaXNzIjoiQ2xhcmVfQUkiLCJhdWQiOiJDbGFyZV9BSSJ9.d8Z083VdTnmkv4k86NTY6oU6PhRhEi_ldUc-7cHN9Sg"}

response = requests.request("GET", url, headers=headers)

if response.status_code == 200:
    # print(response.json())

    r = json.loads(response.content.decode('utf-8'))

    contact_numbers = response.json()

    def get_c_no():
        c_nos = []
        for i in contact_numbers["contact_list"]:
            c_nos.append(i["wAid"])
        # print(c_nos)
        # print(len(c_nos))
        return c_nos

    get_c_no()

  
