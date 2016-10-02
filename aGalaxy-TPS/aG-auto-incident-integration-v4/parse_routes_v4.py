#!/usr/bin/env python
import sys
import syslog
from a10_api_calls import *
from a10_functions import *
from pprint import pformat as pf

# aGalaxy server details that will be used
aGalaxy_server = "1.3.6.2"
aGalaxy_port = "443"
aGalaxy_user = "admin"
aGalaxy_password = "a10"

# Name of the default mitigation template inside aGalaxy server that will be used if no matching template is found
# This template is used in case no templates matching to the specific object is found
default_mitigation_template = "default-mit-temp-1"

# Next hop address for BGP updates that ExaBGP receives
# Next hop address is seen inside the BGP update message
# Flow analysis tool (BGP neighbor) send the route update with this next hop address
bgp_next_hop = "2.1.3.3"

# Tables for housekeeping. These tables are used internally and key parts of the code
dst_entry_table_1 = []
art_1 = []

# The handle that will be seen in syslog messages
syslog.openlog("A10-Incident-Integration-v4-302")

# We will listen standard input where ExaBGP will send messages
while True:
    try:
        line = sys.stdin.readline().strip()
        if line == "":
            counter += 1
            if counter > 100:
                break
            continue
        counter = 0

        route_dict1 = json.loads(line)

        if "update" in str(route_dict1):

            # Create the class object instance and automatically login
            aG_srv_instance1 = aGserver(aGalaxy_server, aGalaxy_port, aGalaxy_user, aGalaxy_password)

            # Get all the relevant stuff
            dst_entries_1 = aG_srv_instance1.get_dstentry_list().json()
            incidents1 = aG_srv_instance1.get_incident_list().json()
            mit_temps1 = aG_srv_instance1.get_mitigation_template_list().json()
            dst_entry_table_1 = update_dst_entry_table(dst_entries_1, dst_entry_table_1)

            new_prefixes, withdrawn_prefixes = get_bgp_updates(route_dict1, bgp_next_hop)
            art_1 = update_active_routing_table(new_prefixes, withdrawn_prefixes, art_1)

            syslog.syslog("Actual routing table: " + str(art_1))

            dst_entry_table_1 = set_related_prefixes_for_dst_entry_table(art_1, dst_entry_table_1)

            short_list_dst_entry_table_1 = find_dst_entries_with_active_prefixes(dst_entry_table_1)
            final_list_dst_entry_table_1 = get_dst_entry_list_without_ongoing_incidents(short_list_dst_entry_table_1,
                                                                                        incidents1)

            if final_list_dst_entry_table_1 == []:
                syslog.syslog(
                    "No objects matched with the current routing table or the matched objects have an ongoing incident.")
            else:
                syslog.syslog("Matched destination entry objects: " + str(final_list_dst_entry_table_1))

                # Create and start necessary incidents
                for each_dst_entry in short_list_dst_entry_table_1:
                    incident_name_1 = "auto-inc-" + each_dst_entry["name"] + "-" + randomid(6)
                    incident_note_1 = "Auto created incident. Related prefix(es): " + str(
                        each_dst_entry["related_prefixes"])
                    mit_temp_id = find_mitigation_temp_id_for_dest_entry(each_dst_entry["name"],
                                                                         default_mitigation_template, mit_temps1)

                    result1 = aG_srv_instance1.create_incident_for_destination_entry(each_dst_entry["id"], mit_temp_id,
                                                                                     incident_name_1, incident_note_1)
                    syslog.syslog("Incident creation result: Object: " + each_dst_entry["name"] + ". Response: " + str(
                        result1.content))

            short_empty_prefix_dst_entry_table_1 = find_dst_entries_with_no_active_prefixes(dst_entry_table_1)
            final_empty_list_dst_entry_table_1 = get_dst_entry_list_with_ongoing_auto_incidents(
                short_empty_prefix_dst_entry_table_1, incidents1)

            if final_empty_list_dst_entry_table_1 == []:
                syslog.syslog("No objects matched for incident stopping.")
            else:
                syslog.syslog("Matched destination entry objects for incident stopping: " + str(
                    final_empty_list_dst_entry_table_1))

                # Stop already active incidents
                for each_dst_entry in final_empty_list_dst_entry_table_1:
                    incident_uuid_1 = each_dst_entry["incident-id"]

                    result1 = aG_srv_instance1.stop_incident_via_incident_uuid(incident_uuid_1)

                    syslog.syslog("Incident stop result: Incident ID:" + each_dst_entry[
                        "incident-id"] + ". Related destination entry object: " + each_dst_entry[
                                      "name"] + ". Response: " + str(result1.content))


        else:
            syslog.syslog("Not an update.")
            syslog.syslog(syslog.LOG_ALERT, prefixed('INFO', line))

    except KeyboardInterrupt:
        pass
    except IOError:
        # most likely a signal during readline
        pass


