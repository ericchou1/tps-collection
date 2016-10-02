#!/usr/bin/env python
import requests
import json
from netaddr import IPNetwork

"""
aGServer class hadles all aGalaxy related API calls
It is used to create an aGalaxy class object so that all API calls can easily be made
"""
class aGserver:
    def __init__(self, aG_server, aG_server_port, aG_username=None, aG_password=None):
        """
        Initialize aGalaxy connection and get cookie via POST method
        """

        self.aG_server = aG_server
        self.aG_server_port = aG_server_port
        self.server_token = ""

        if aG_username != None and aG_password != None:
            self.getcookie(aG_username, aG_password)


    def getcookie(self, aG_username, aG_password):
        """
        Get authentication cookie
        """

        self.aG_username = aG_username
        self.aG_password = aG_password

        headers = {
            "content-type": "application/json",
            "accept": "application/json",
        }

        payload = {"credentials":
            {
                "username": aG_username,
                "password": aG_password
            }
        }

        target_url = "https://" + self.aG_server + ":" + str(self.aG_server_port) + "/agapi/auth/login/"

        session1 = requests.Session()
        session1.headers.update(headers)
        post1 = session1.post(target_url, verify=False, data=json.dumps(payload))

        session1.headers["X-CSRFToken"] = session1.cookies.get("csrftoken")
        self.session = session1


    def get_devices(self):
        """
        Gets the list of TPS devices defined in aGalaxy
        """

        target_url = "https://" + self.aG_server + ":" + str(self.aG_server_port) + "/agapi/v1/device/"
        response1 = self.session.get(target_url, verify=False)

        # device_list = pf(response1.json())

        return response1


    def get_incident_list(self):
        """
        Gets the list of incidents in aGalaxy
        Current aGAPI retuns the full list of incidents
        """

        target_total_url = "https://" + self.aG_server + ":" + str(
            self.aG_server_port) + "/agapi/v1/ddos/incident/?total=true"
        response1 = self.session.get(target_total_url, verify=False).json()
        total1 = response1["total"]

        target_url = "https://" + self.aG_server + ":" + str(
            self.aG_server_port) + "/agapi/v1/ddos/incident/" + "?count=" + str(total1)
        response1 = self.session.get(target_url, verify=False)

        return response1


    def get_dstentry_list(self):
        """
        Gets the list of destination entry objects
        """

        target_total_url = "https://" + self.aG_server + ":" + str(
            self.aG_server_port) + "/agapi/v1/ddos/dst/?total=true"
        response1 = self.session.get(target_total_url, verify=False).json()
        total1 = response1["total"]

        target_url = "https://" + self.aG_server + ":" + str(
            self.aG_server_port) + "/agapi/v1/ddos/dst/" + "?count=" + str(total1)
        response1 = self.session.get(target_url, verify=False)

        return response1


    def get_mitigation_template_list(self):
        """
        Gets the list of mitigation templates
        """

        target_total_url = "https://" + self.aG_server + ":" + str(
            self.aG_server_port) + "/agapi/v1/ddos/template/mitigation/?total=true"
        response1 = self.session.get(target_total_url, verify=False).json()
        total1 = response1["total"]

        target_url = "https://" + self.aG_server + ":" + str(
            self.aG_server_port) + "/agapi/v1/ddos/template/mitigation/" + "?count=" + str(total1)
        response1 = self.session.get(target_url, verify=False)

        return response1


    def create_incident_for_destination_entry(self,dst_entry_uuid,mit_temp_uuid,incident_name,
                                              incident_note,start_mitigation=True):
        """
        Creates an incident for a single destination entry
        """
        target_url = "https://" + self.aG_server + ":" + str(
            self.aG_server_port) + "/agapi/v1/ddos/incident/"


        payload = {"incident":
                       {
                            "name": incident_name,
                            "note": incident_note,
                            "type": "Unknown",
                            "mitigation_template": mit_temp_uuid,
                            "start_mitigation": True,
                            "dst_entry":
                                {
                                    "id": dst_entry_uuid,
                                },
                            "use_scheduler": False
                       }
        }


        response1 = self.session.post(target_url, verify=False, data=json.dumps(payload))

        return response1


    def stop_incident_via_incident_uuid(self,incident_uuid):
        """
        Stops an incident for a given incident UUID
        """
        target_url = "https://" + self.aG_server + ":" + str(
            self.aG_server_port) + "/agapi/v1/ddos/incident/" + str(incident_uuid) + "/stop/"

        response1 = self.session.post(target_url, verify=False)

        return response1


