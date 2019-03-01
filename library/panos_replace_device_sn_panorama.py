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
module: panos_replace_device_sn_panorama
short_description: Replace device SN in panorama.
description:
    - Replace device SN in panorama.
author: "Mohanad Elamin (@mohanadelamin)"
requirements:
    - pan-python
options:
    panorama_ip_address:
        description:
            - IP address (or hostname) of Panorama device
        required: true
    password:
        description:
            - password for authentication
        required: true
    username:
        description:
            - username for authentication
        required: true
    old_sn:
        description:
            - old device serial number
        required: true
    new_sn:
        description:
            - new device serial number
'''

EXAMPLES = '''
    - hosts: localhost
      connection: local
      tasks:
        - name: Deactivate License
          panos_de_lic:
            panorama_ip_address: "192.168.1.1"
            username: "admin"
            password: "paloalto"
            old_sn: "XXXXXXXXXXXXXXXXXX"
            new_sn: "yyyyyyyyyyyyyyyyyy"
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule

try:
    import pan.xapi
    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def replace_sn(xapi, module,old_sn,new_sn):
    try:
        xapi.op(cmd='<replace><device><old>%s</old><new>%s</new></device></replace>' % (old_sn, new_sn))
    except pan.xapi.PanXapiError as msg:
        if hasattr(xapi, 'xml_document'):
            if 'Successfully' in xapi.xml_document:
                return True
        else:
            module.fail_json(msg="Unknown error!")

        raise

    return True

def main():
    argument_spec = dict(
        panorama_ip_address=dict(required=True),
        password=dict(required=True, no_log=True),
        username=dict(default='admin'),
        old_sn=dict(required=True),
        new_sn=dict(required=True),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg='pan-python is required for this module')

    ip_address = module.params["panorama_ip_address"]
    password = module.params["password"]
    username = module.params['username']
    old_sn = module.params['old_sn']
    new_sn = module.params['new_sn']

    xapi = pan.xapi.PanXapi(
        hostname=ip_address,
        api_username=username,
        api_password=password
    )

    if(replace_sn(xapi,module,old_sn,new_sn)):
        module.exit_json(changed=True, msg="SN replaced from %s to %s" % (old_sn, new_sn))
    else:
        module.fail_json(msg='SN Change Failed!')

if __name__ == '__main__':
    main()
