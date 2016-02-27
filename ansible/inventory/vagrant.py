import json
import os


VM_IP = os.environ.get('VM_IP')
VM_SSH_KEY_PATH = os.environ.get('VM_SSH_KEY_PATH')

if not VM_IP or not VM_SSH_KEY_PATH:
    raise ValueError('Both VM_IP and VM_SSH_KEY_PATH environment '
                     'variables must be set')


inventory_data = {
  "_meta": {
    "hostvars": {
      "vm": {
         "ansible_ssh_user": "vagrant",
         "ansible_ssh_host": "{}".format(VM_IP),
         "ansible_ssh_private_key_file": "{}".format(VM_SSH_KEY_PATH),
      }
    }
  },
  "webservers": [
    "vm"
  ]
}


print(json.dumps(inventory_data, sort_keys=True, indent=2))

