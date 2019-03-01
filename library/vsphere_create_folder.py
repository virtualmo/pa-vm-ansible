#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
author: "Shashank Awasthi"
module: vsphere_create_folder
short_description: Create a folder on VCenter if it does not exist
description:
  - This module requires login to VCenter Server
  - This module requires pysphere python module installed
  - This module creates a folder on mentioned VCenter Server
  - This module does not create any folder if the folder with the same name is already existing on the VCenter Server
  - This module supports nesting upto only 2 levels
version_added: "1.2"
options:
  host:
    description:
      - The vsphere Server on which the folder is to be created
    required: true
  login:
    description:
      - The login name to authenticate on VSphere
    required: true
  password:
    description:
      - The password to authenticate VSphere
    required: true
  folder_name:
    description:
      - The folder name which is to be created
    required: true
  parent_folder_name:
    description:
      The name of parent folder under which the folder_name is residing.
    required: true
  datacenter_name:
    description:
      - The name of the datacenter where the folder is to be created
    required: true
examples:
  - description: create the folder with name NewDeployments
    code:
       - local_action: vsphere_create_folder host=$eszserver login=$esxlogin password=$esxpassword folder_name=$folder_name
parent_folder_name=$parent_folder_name  datacenter_name=$dc_name
notes:
  - This module ought ot be run from a system which can access vsphere directly
'''

import sys

try:
        import pysphere
        from pysphere import *
        from pysphere.resources import VimService_services as VI
except ImportError:
        print "failed=true, msg=Pysphere Python module not available"
        sys.exit(1)

def main():
        module = AnsibleModule(
                argument_spec = dict(
                        host =  dict(requred = True),
                        login = dict(required = True),
                        password = dict(required = True),
                        folder_name = dict(required = True),
                        parent_folder_name =  dict(required = True),
                        datacenter_name = dict(required = True)
                )
        )

        host = module.params.get('host')
        login = module.params.get('login')
        password = module.params.get('password')
        folder_name = module.params.get('folder_name')
        parent_folder_name = module.params.get('parent_folder_name')
        datacenter_name = module.params.get('datacenter_name')

        server = pysphere.VIServer()
        try:
                server.connect(host,login,password)
        except Exception, e:
                module.fail_json(msg = 'Failed to connect to %s: %s' % (host, e))


        def createFolder(vm_folder,folder_name):
                try:
                        request = VI.CreateFolderRequestMsg()
                        _this = request.new__this(vm_folder)
                        _this.set_attribute_type(vm_folder.get_attribute_type())
                        request.set_element__this(_this)
                        request.set_element_name(folder_name)
                        server._proxy.CreateFolder(request)
                except pysphere.ZSI.FaultException, e:
                        pass

        try:
                datacenters = server._get_datacenters()
                dc = datacenters[datacenter_name]

                dc_props = VIProperty(server,dc)
                vm_folder = dc_props.vmFolder._obj

                createFolder(vm_folder,parent_folder_name)

                folders =  server._retrieve_properties_traversal(property_names=['name'], from_node =  dc, obj_type = 'Folder')

                for f in folders:
                        if f.PropSet[0].Val == parent_folder_name:
                                vm_folder = f.Obj
                                break
                createFolder(vm_folder,folder_name)
        except Exception, e:
                module.fail_json(msg = "failed to create folder: %s" % e)




        module.exit_json(changed = True, folder = folder_name, parent_folder = parent_folder_name)

#<<INCLUDE_ANSIBLE_MODULE_COMMON>>
main()
