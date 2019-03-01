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
module: panos_lic
short_description: deactive VM capacity license either directly from the device or via the license api.
description:
    - Deactive VM capacity license
    - For auto deactivation the device should have Internet access.
    - For manual deactivation the ansible controller should have Internet access.
author: "Mohanad Elamin (@mohanadelamin)"
requirements:
    - pan-python
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device
        required: true
    password:
        description:
            - password for authentication
        required: true
    username:
        description:
            - username for authentication
        required: false
        default: "admin"
    api_key:
        description:
            - api_key to be applied for auto deactivation
        required: true
    auto:
        description:
            - whether to deactivate directly from the FW or from localy via the Licensing API
        required: false
        default: "false"
'''

EXAMPLES = '''
    - hosts: localhost
      connection: local
      tasks:
        - name: Deactivate License
          panos_de_lic:
            ip_address: "192.168.1.1"
            username: "admin"
            password: "paloalto"
            auto: True
            api_key: "XXXXXXXXXXXXXXXXXX"
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

def apply_api_key(xapi, module, api_key):
    try:
        xapi.op(cmd='<request><license><api-key><set><key>%s</key></set></api-key></license></request>' % api_key)
    except pan.xapi.PanXapiError as msg:
        if hasattr(xapi, 'xml_document'):
            if "API key is same as old" in xapi.xml_document:
                return True
        raise

    return True

def deactivate_license(xapi, module):
    try:
        xapi.op(cmd='<request><license><deactivate><VM-Capacity><mode>auto</mode></VM-Capacity></deactivate></license></request>')
    except pan.xapi.PanXapiError as msg:
        if hasattr(xapi, 'xml_document'):
            if 'Successfully' in xapi.xml_document:
                return
        else:
            module.fail_json(msg="Unknown error!")

        raise

    return

def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(required=True, no_log=True),
        username=dict(default='admin'),
        api_key=dict(required=False, no_log=True),
        auto=dict(type='bool', default=True)
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg='pan-python is required for this module')

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    auto = module.params['auto']
    username = module.params['username']
    api_key = module.params['api_key']

    xapi = pan.xapi.PanXapi(
        hostname=ip_address,
        api_username=username,
        api_password=password
    )

    if auto and not api_key:
        module.fail_json(msg='For Auto deactivation API-KEY is required.')
    elif auto:
        if (apply_api_key(xapi,module,api_key)):
            deactivate_license(xapi,module)
            module.exit_json(changed=True, msg="VM License deactivated.")
        else:
            module.fail_json(msg='License Deactivation Failed!')
    else:
        pass


if __name__ == '__main__':
    main()
