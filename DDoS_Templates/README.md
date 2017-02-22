#A10 Thunder TPS Configuration Generator 

##Prerequisites: 

  1. The configuration generator requires Ansible (https://www.ansible.com/) and the template module (http://docs.ansible.com/ansible/template_module.html) 

##Overview:

  1. The Templates folder contains the tps_base_config_v1.j2 and tps_zone_config_v1.j2 template files in Jinja2 format. 
  2. The TPS_Base_Config_Creation.yml and TPS_Zone_Config_Creation.yml are Ansible plabooks to be run. You can see a sample of the fields that can be modified. 
  3. The Config folder will contain the configuration outputs. 

##Sample Usage:

```
echou@ubuntu:~/A10/DDoS_Templates$ cat TPS_Zone_Config_Creation.yml
---
- name: Create TPS Zone Config
  hosts: localhost
  vars:
    tps_zones: {
      "webserver": {
         "zone_name": "webserver",
         "zone_ip": "192.168.1.101",
         "bgp_advertise": True
      }
    }

  tasks:
    - name: Create TPS Zone Config
      template:
        src=./Templates/tps_zone_config_v1.j2
        dest=./Configs/{{ item.key }}_zone.txt
      with_dict: "{{ tps_zones }}"

echou@ubuntu:~/A10/DDoS_Templates$ ansible-playbook TPS_Zone_Config_Creation.yml
 [WARNING]: provided hosts list is empty, only localhost is available


PLAY [Create TPS Zone Config] **************************************************

TASK [setup] *******************************************************************
ok: [localhost]

TASK [Create TPS Zone Config] **************************************************
ok: [localhost] => (item={'key': u'webserver', 'value': {u'zone_name': u'webserver', u'bgp_advertise': True, u'zone_ip': u'192.168.1.101'}})

PLAY RECAP *********************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0

echou@ubuntu:~/A10/DDoS_Templates$ cat Configs/webserver_zone.txt
ddos dst zone webserver
  ip 192.168.1.101
  operational-mode monitor
    bgp advertised
    zone-template logging cef-logger
  log enable periodic
  ip-proto tcp
    drop-frag-pkt
  ip-proto udp
    drop-frag-pkt
<skip>
  port other tcp
    detection-enable
    deny
  port other udp
    detection-enable
    deny
```

## Beta: Config Push

You can use the beta configuration push Playbook and module as below: 

```
(TPS_Config_Push.yml)
---
- hosts: localhost
  user: echou
  connection: local

  tasks:
      - name: Thunder TPS configuration push using cli.deploy
        action: config_push host="192.168.199.152" username="admin" password="a10" config_file="./Configs/webserver_zone.txt"
        register: output

      - debug: msg="{{ output.msg }}"


(output)
PLAY ***************************************************************************

TASK [setup] *******************************************************************
ok: [localhost]

TASK [Thunder TPS configuration push using cli.deploy] *************************
ok: [localhost]

TASK [debug] *******************************************************************
ok: [localhost] => {
    "msg": {
        "Result": "{\n  \"response\": {\n    \"status\": \"OK\"\n  }\n}"
    }
}

PLAY RECAP *********************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0

```

