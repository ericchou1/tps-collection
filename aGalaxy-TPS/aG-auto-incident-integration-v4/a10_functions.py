#!/usr/bin/env python
from netaddr import IPNetwork
import random
import time
import os
import string


def get_ongoing_incidents_for_prefix(prefix, incident_dict):
    """
    Returns a list of ongoing incidents related with given prefix
    """
    prefix = IPNetwork(prefix)
    list1 = []
    for i in incident_dict["incident_list"]:
        ip_addr = IPNetwork(i["dst_entry"]["ip_addr"])
        if i["status"] == "Ongoing" and (prefix in ip_addr or ip_addr in prefix):
            list1.append(i)
    return list1


def old_get_dst_entries_for_prefix(prefix, dst_entry_dict):
    """
    Returns a list of destination entries related with the given prefix
    (This is the older version of the function)
    """
    prefix = IPNetwork(prefix)
    list1 = []
    for i in dst_entry_dict["dst_entry_list"]:
        ip_addr = IPNetwork(i["ip_addr"])
        if prefix in ip_addr or ip_addr in prefix:
            list1.append(i)
    return list1


def old_get_dst_entry_list_without_ongoing_incidents(dst_entry_list, incident_list):
    """
    Returns a list of destination entry objects without any ongoing incidents
    Input variables are lists generated via other functions
    (This is the older version of the function)
    """
    i = 0
    while (i < len(incident_list)):
        k = 0
        while (k < len(dst_entry_list)):
            if incident_list[i]["dst_entry"]["name"] == dst_entry_list[k]["name"]:
                del dst_entry_list[k]
            k += 1
        i += 1
    return dst_entry_list


def get_dst_entry_list_without_ongoing_incidents(dst_entry_table, incident_list):
    """
    Deletes all destination entries that have an ongoing incident
    Returns the final list
    """
    i = 0
    while (i < len(incident_list["incident_list"])):
        k = 0
        while (k < len(dst_entry_table)):
            if incident_list["incident_list"][i]["dst_entry"]["name"] == dst_entry_table[k]["name"] and incident_list["incident_list"][i]["status"] == "Ongoing":
                del dst_entry_table[k]
            k += 1
        i += 1
    return dst_entry_table


def get_dst_entry_list_with_ongoing_auto_incidents(dst_entry_table, incident_list):
    """
    Deletes all destination entries that do not have an ongoing incident
    Returns the final list
    """
    list_1 = []
    i = 0
    while (i < len(incident_list["incident_list"])):
        k = 0
        while (k < len(dst_entry_table)):
            if incident_list["incident_list"][i]["dst_entry"]["name"] == dst_entry_table[k]["name"] and incident_list["incident_list"][i]["status"] == "Ongoing" and "auto-inc-" in incident_list["incident_list"][i]["name"]:
                dst_entry_table[k]["incident-id"] = incident_list["incident_list"][i]["id"]
                list_1.append(dst_entry_table[k])
            k += 1
        i += 1
    return list_1


def get_mitigation_temp_uuid(mit_temp_list, mit_temp_name):
    """
    Returns the UUID of the mitigation template based on name
    """
    for i in mit_temp_list["mitigation_template_list"]:
        if i["name"] == mit_temp_name:
            return i["id"]


def get_destination_entry_uuid(dst_entry_list, dst_entry_name):
    """
    Returns the UUID of the destination entry based on name
    """
    for i in dst_entry_list["dst_entry_list"]:
        if i["name"] == dst_entry_name:
            return i["id"]


def update_dst_entry_table(dst_entries_1, dst_entry_table_1):
    """
    Updates the destination entry table with most recent destination entry list
    If the list is empty (first time run) constructs the list
    """
    for each in dst_entries_1["dst_entry_list"]:
        v_sub = {"ip_addr": each["ip_addr"], "name": each["name"], "id": each["id"], "related_prefixes": [], "incident-id": ""}
        does_exist = False
        if not dst_entry_table_1 == []:
            for each in dst_entry_table_1:
                if each["name"] == v_sub["name"]:
                    does_exist = True
        if does_exist is False:
            dst_entry_table_1.append(v_sub)
    return dst_entry_table_1


def get_bgp_updates(route_dict1, peer_router):
    """
    Get updates from stdin as a JSON line like route_dict1 = json.loads(line)
    """
    new_prefixes = []
    withdrawn_prefixes = []
    try:
        for each_new_prefix in route_dict1["neighbor"]["message"]["update"]["announce"]["ipv4 unicast"][peer_router]:
            new_prefixes.append(each_new_prefix)
    except KeyError:
        pass
    try:
        for each_withdrawn_prefix in route_dict1["neighbor"]["message"]["update"]["withdraw"]["ipv4 unicast"]:
            withdrawn_prefixes.append(each_withdrawn_prefix)
    except KeyError:
        pass
    return new_prefixes, withdrawn_prefixes


def update_active_routing_table(new_prefixes, withdrawn_prefixes, active_routing_table):
    """
    Updates the routing table with most recent prefix changes
    Then, this routing table is used to associate prefixes with destination entries
    """
    for each_new_prefix in new_prefixes:
        if not each_new_prefix in active_routing_table:
            active_routing_table.append(each_new_prefix)
    for each_withdrawn_prefix in withdrawn_prefixes:
        if each_withdrawn_prefix in active_routing_table:
            active_routing_table.remove(each_withdrawn_prefix)
    return active_routing_table


def get_dst_entries_for_prefix(prefix, dst_entry_dict):
    """
    Returns a list of destination entries related with the given prefix
    """
    prefix = IPNetwork(prefix)
    list1 = [{u'ipv6_addr': None, u'ip_addr': u'0.0.0.0/0', u'name': u'no-name',
              u'device_list': [u'227005a9-bdb5-4b57-a25d-94886922fcf5'],
              u'url': u'https://1.3.6.1/agapi/v1/ddos/dst/bd2d3cdf-ec71-4166-b848-f361ea1b0d05/',
              u'device_group_id': None, u'id': u'ad2d3cdf-ec71-4166-b848-f361ea1b0d05'}]
    for i in dst_entry_dict["dst_entry_list"]:
        ip_addr = IPNetwork(i["ip_addr"])
        ip_addr2 = IPNetwork(list1[0]["ip_addr"])
        if prefix in ip_addr and ip_addr in ip_addr2:
            list1[0] = i
    # If there is no match for the given prefix, we should change to 0.0.0.0/32 in the default list entry
    # Otherwise below function will match all of the destination entries
    if list1[0]["ip_addr"] == "0.0.0.0/0":
        list1[0]["ip_addr"] = "0.0.0.0/32"
    for i in dst_entry_dict["dst_entry_list"]:
        ip_addr_i = IPNetwork(i["ip_addr"])
        ip_addr2 = IPNetwork(list1[0]["ip_addr"])
        if (not ip_addr_i == ip_addr2) and (ip_addr_i in ip_addr2) and (ip_addr_i in prefix):
            list1.append(i)
    if list1[0]["name"] == "no-name":
        list1 = []
    return list1


def set_related_prefixes_for_dst_entry_table(routing_table, dst_entry_table):
    """
    Updates destination entry table based on given routing table.
    """

    # Clear all the entries inside the "related prefixes" lists
    for each_dst_entry in dst_entry_table:
        dst_entry_table[dst_entry_table.index(each_dst_entry)]["related_prefixes"] = []

    # Process all prefixes that is or inside the most specific destination entry network
    for each_prefix in routing_table:
        temp_dst_entry_list_1 = [{'related_prefixes': [], 'ip_addr': u'0.0.0.0/0', 'name': u'no-name'}]
        for each_dst_entry in dst_entry_table:
            if IPNetwork(each_prefix) in IPNetwork(each_dst_entry["ip_addr"]) and IPNetwork(each_dst_entry["ip_addr"]) in IPNetwork(temp_dst_entry_list_1[0]["ip_addr"]):
                temp_dst_entry_list_1[0] = each_dst_entry

        for each_dst_entry in dst_entry_table:
            if temp_dst_entry_list_1[0]["name"] == each_dst_entry["name"]:
                entry_index = dst_entry_table.index(each_dst_entry)
                dst_entry_table[entry_index]["related_prefixes"].append(each_prefix)

    # Process all prefixes that covers (but not the same as) the destination entry network
    for each_prefix in routing_table:
        exact_match = False
        for each_dst_entry in dst_entry_table:
            if IPNetwork(each_dst_entry["ip_addr"]) == IPNetwork(each_prefix):
                exact_match = True
                temp_dst_entry_list_1[0] = each_dst_entry

        if exact_match == True:
            for each_dst_entry in dst_entry_table:
                if IPNetwork(each_dst_entry["ip_addr"]) in IPNetwork(each_prefix) and IPNetwork(each_dst_entry["ip_addr"]) in IPNetwork(temp_dst_entry_list_1[0]["ip_addr"]):
                    # Same exact prefix can be inserted into "related prefixes" list, but that's not an operational problem
                    entry_index = dst_entry_table.index(each_dst_entry)

                    if not each_prefix in dst_entry_table[entry_index]["related_prefixes"]:
                        dst_entry_table[entry_index]["related_prefixes"].append(each_prefix)

    return dst_entry_table


def find_dst_entries_with_active_prefixes(dst_entry_table):
    """
    Deletes all destination entries that have zero "related prefixes" list.
    Returns the short list.
    """
    short_list = []
    for each_dst_entry in dst_entry_table:
        if not each_dst_entry["related_prefixes"] == []:
            short_list.append(each_dst_entry)

    return short_list


def find_dst_entries_with_no_active_prefixes(dst_entry_table):
    """
    Deletes all destination entries that have a non-zero "related prefixes" list.
    Returns the short list.
    """
    short_list = []
    for each_dst_entry in dst_entry_table:
        if each_dst_entry["related_prefixes"] == []:
            short_list.append(each_dst_entry)

    return short_list


def find_mitigation_temp_id_for_dest_entry(dst_entry_name, default_mitigation_template_name, mitigation_template_list):
    """
    Returns the id of the mitigation template based on destination entry name.
    Returns customer default mitigation template if no match is found.
    Mitigation templates are linked to destination entries based on naming conventions.
    """
    mitigation_template_id = ""
    default_mitigation_template_id = ""

    for each_mit_temp in mitigation_template_list["mitigation_template_list"]:
        if each_mit_temp["name"] == "mit-temp-" + str(dst_entry_name):
            mitigation_template_id = each_mit_temp["id"]

        if each_mit_temp["name"] == str(default_mitigation_template_name):
            default_mitigation_template_id = each_mit_temp["id"]

    if mitigation_template_id == "":
        return default_mitigation_template_id
    else:
        return mitigation_template_id


def randomid(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))


def prefixed(level, message):
    now = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())
    return "%s %-8s %-6d %s" % (now, level, os.getpid(), message)

