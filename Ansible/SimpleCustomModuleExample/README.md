## Example of a Custom Module that can be run locally

### Requirements 

1. Python version 2.7.x. This code was tested with Python 2.7.6, but will likely work with most Python 2.4 and greater. 
  a. If you want to learn more about Ansible Python 3 support, https://docs.ansible.com/ansible/developing_modules_python3.html.
  b. This code is run on the Ansbile control machine (that makes outbound call to manage other devices), therefore Windows machine is not supported at this time. This is an Ansible limitation, http://docs.ansible.com/ansible/intro_installation.html#control-machine-requirements. 
2. You have Ansible version 2.x or greater installed on the host machine. If not, please use PIP, i.e. sudo pip install ansible, instead of host package management system such as apt or yum. The host apt or yum packages are likely outdated in the 1.x versions. 
3. Python Requests (http://docs.python-requests.org/en/master/) package installed. Please 'sudo pip install requests' if it is not on the local machine. This dependency is not needed to be specified in group_vars since the connection is local. 
4. AXAPIv3 (ACOS 3.x and above) on your A10 Thunder TPS device. 

### Notes

1. By default, the directory ./library alongside your top level Playbooks added as a search directory, more information here: http://docs.ansible.com/ansible/developing_modules.html. 
2. The Playbook is executed locally and make API calls outboud to the TPS device, localhost by default is presented so no host file is needed. However, you will get a warning during exection. 
3. While you can use any language, any API, it is recommended to levearage AnsibleModule API as indicated here http://docs.ansible.com/ansible/developing_modules.html#getting-your-module-into-ansible and is used in the module example.

### Steps

1. In the directory where you want to place your Playbook, create a directory called library and place the axapiExample.py file in the directory. 
2. Place the axapi_module.yml file in the top level directory. 
3. Run the Playbook. 

### Output 

```
echou@echou-u2:~/ansible$ tree .
.
├── axapi_module.yml
└── library
    └── axapiExample.py

1 directory, 2 files
echou@echou-u2:~/ansible$

echou@echou-u2:~/ansible$ ansible --version
ansible 2.1.2.0
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/usr/share/ansible']
echou@echou-u2:~/ansible$

echou@echou-u2:~/ansible$ ansible-playbook axapi_module.yml
 [WARNING]: provided hosts list is empty, only localhost is available


PLAY [localhost] ***************************************************************

TASK [setup] *******************************************************************
ok: [localhost]

TASK [Simple AXAPIv3 Module] ***************************************************
changed: [localhost]

TASK [debug] *******************************************************************
ok: [localhost] => {
    "msg": {
        "Device_Info": {
            "Hardware": "TH4435 TPS",
            "Software": "3.2.1-P1 build 42 (Aug-19-2016,06:53)"
        }
    }
}

PLAY RECAP *********************************************************************
localhost                  : ok=3    changed=1    unreachable=0    failed=0

echou@echou-u2:~/ansible$

```

Please submit any issues or feature requests in the Issues section of the repository. Thank you. 

