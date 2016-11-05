# This example utilize the A10 Thunder aXAPIv3 with Ansible URI module
# to quickly perform show and config commands. 

The playbook contains the following: 

- Authorization and Token
- Registers variable for later use
- GET example for 'show version'
- POST example to change device hostname
- Writes configuration change to non-volatile memory
- Gracefully logoff

Playbook Output: 

```
ansible-playbook -i host_a10 A10_Test_uri.yml

PLAY [A10 aXAPIv3 Demonstration Playbook] **************************************

TASK [authenticate] ************************************************************
ok: [192.168.199.152.xip.io]

TASK [show output] *************************************************************
ok: [192.168.199.152.xip.io] => {
    "output": {
        "changed": false,
        "connection": "close",
        "content_length": "176",
        "content_type": "application/json",
        "date": "Sat, 05 Nov 2016 02:38:46 GMT",
        "json": {
            "authresponse": {
                "description": "the signature should be set in Authorization header for following request.",
                "signature": "c7c7a0e418affdad15dccea8faef5c"
            }
        },
        "redirected": false,
        "server": "Apache",
        "status": 200
    }
}

TASK [show version] ************************************************************
ok: [192.168.199.152.xip.io]

TASK [show version output] *****************************************************
ok: [192.168.199.152.xip.io] => {
    "version": {
        "changed": false,
        "connection": "close",
        "content_length": "682",
        "content_location": "https://192.168.199.152/axapi/v3/version/oper",
        "content_type": "application/json",
        "date": "Sat, 05 Nov 2016 02:38:46 GMT",
        "json": {
            "version": {
                "a10-url": "/axapi/v3/version/oper",
                "oper": {
                    "boot-from": "HD_SECONDARY",
                    "cf-pri": "3.0.0.419",
                    "cf-sec": "",
                    "copyright": "Copyright 2007-2014 by A10 Networks, Inc.",
                    "current-time": "Nov-4-2016, 19:38",
                    "firmware-version": "5.6",
                    "hd-pri": "3.2.1.175",
                    "hd-sec": "3.2.1-P1.42",
                    "hw-code": "140611",
                    "hw-platform": "TH4435 TPS",
                    "last-config-saved-time": "Nov-4-2016, 19:34",
                    "plat-features": "",
                    "serial-number": "TH44113014060008",
                    "sw-version": "3.2.1-P1 build 42 (Aug-19-2016,06:53)",
                    "up-time": "74 days, 14 hours, 39 minutes",
                    "virtualization-type": "NA"
                }
            }
        },
        "redirected": false,
        "server": "Apache",
        "status": 200
    }
}

TASK [change hostname] *********************************************************
ok: [192.168.199.152.xip.io]

TASK [write memory] ************************************************************
ok: [192.168.199.152.xip.io]

TASK [logoff] ******************************************************************
ok: [192.168.199.152.xip.io]

PLAY RECAP *********************************************************************
192.168.199.152.xip.io     : ok=7    changed=0    unreachable=0    failed=0
```

