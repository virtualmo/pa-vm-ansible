#!/usr/bin/env python

#  Copyright 2016 Palo Alto Networks, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: panos_get_sn
short_description: get device SN
description:
    - get device SN
author: "Mohanad Elamin (@mohanadelamin)"
requirements:
    - pan-python
options:
    fw_ip_address:
        description:
            - IP address (or hostname) of PAN-OS device
        required: true    
    fw_password:
        description:
            - password for authentication
        required: true
    fw_username:
        description:
            - username for authentication
        required: false
        default: "admin"
'''

EXAMPLES = '''
    - hosts: localhost
      connection: local
      tasks:
        - name: Deactivate License
          panos_de_lic:
            panorama_ip_address: "192.168.1.1"
            panorama_username: "admin"
            panorama_password: "paloalto"
            fw_ip_address: "192.168.1.2"
            fw_username: "admin"
            fw_password: "paloalto"
          register: result
    - name: Display serialnumber (if already registered)
      debug:
        var: "{{result.serialnumber}}"
'''

RETURN = '''
serialnumber:
    description: serialnumber of the device in case that it has been already registered
    returned: success
    type: string
    sample: 007200004214
'''

from ansible.module_utils.basic import AnsibleModule

try:
    import pan.xapi
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

def get_serial(xapi, module):
    xapi.op(cmd="show system info", cmd_xml=True)
    r = xapi.element_root
    serial = r.find('.//serial')
    if serial is None:
        module.fail_json(msg="No <serial> tag in show system info")

    serial = serial.text

    return serial


def main():
    argument_spec = dict(
        fw_ip_address=dict(required=True),
        fw_password=dict(required=True, no_log=True),
        fw_username=dict(default='admin')
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg='pan-python is required for this module')

    fw_ip_address = module.params["fw_ip_address"]
    fw_password = module.params["fw_password"]
    fw_username = module.params['fw_username']

    xapi_fw = pan.xapi.PanXapi(
        hostname=fw_ip_address,
        api_username=fw_username,
        api_password=fw_password
    )
    
    serialnumber = get_serial(xapi_fw, module)
    if serialnumber != 'unknown':
            return module.exit_json(changed=False, serialnumber=serialnumber)

if __name__ == '__main__':
    main()
