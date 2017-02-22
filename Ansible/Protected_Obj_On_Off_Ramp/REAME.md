# Thunder TPS Ansible Playbook for On / Off Ramp Protected Objects

## Beta
## Overview

  1. A10 Thunder TPS provides two ways to dynamically on / off ramp protected objects:
    a. 'bgp advertised' command under 'ddos dst zone' with 'ddos advertised' route-map. 
    b. direct bgp netblock advertisement under 'router bgp'.
  2. Use the cli.deploy custom module under library/ folder to insert command accordingly. 

## Sample Usage

```
(protected_object.yml)
---
- name: Playbook for On / Off Ramp Thunder TPS Protected Objects
  hosts: localhost
  user: echou
  connection: local
  gather_facts: false

  tasks:
      - name: BGP On / Off Ramp for Protected Object
        action: cli_deploy_example host="192.168.199.152" username="admin" password="a10" commands="router bgp 64513, network 1.1.1.1/32, wr mem"
        register: output

      - debug: msg="{{ output.msg }}"

(output)
PLAY [Playbook for On / Off Ramp Thunder TPS Protected Objects] ****************

TASK [BGP On / Off Ramp for Protected Object] **********************************
ok: [localhost]

TASK [debug] *******************************************************************
ok: [localhost] => {
    "msg": {
        "Result": "{\n  \"response\": {\n    \"status\": \"OK\"\n  }\n}"
    }
}

PLAY RECAP *********************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0
```
