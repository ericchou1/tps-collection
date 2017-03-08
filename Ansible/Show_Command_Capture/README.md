# TPS Show Command

1. Execute CLI show command
2. Captured output in /tmp/a10_output.txt
3. Execute Python parser command and delete /tmp/a10_output.txt after
4. Display parsed stdnout output 

```
$ ansible-playbook show_command.yml
 [WARNING]: provided hosts list is empty, only localhost is available


PLAY [Playbook for Show Command] ***********************************************

TASK [show command] ************************************************************
ok: [localhost]

TASK [copy output out to /tmp/a10_output.txt] **********************************
changed: [localhost]

TASK [run another script to parse out serial number] ***************************
changed: [localhost]

TASK [show serial number] ******************************************************
ok: [localhost] => {
    "msg": "TH441130......"
}

PLAY RECAP *********************************************************************
localhost                  : ok=4    changed=2    unreachable=0    failed=0
```
