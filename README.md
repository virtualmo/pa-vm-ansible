# Example Ansible playbooks to automate the deployment and scaling up/down of Palo Alto Networks VM-Series

## Usecases
The following use cases can be accomplished via this ansible playbooks.
1. Deploy Standalone PA-VM
Using **deploy.yml** playbooks, you can deploy standalone PA-VM.
![Standalone](https://raw.githubusercontent.com/mohanadelamin/pa-vm-ansible/master/others/Deploy.png)

**deploy.yml** playbook does the following tasks:
	1. Prepare the bootstrapping iso file required to bootstrap PAN-OS and Upload the image to the datastore. More information about bootstrapping can found at PAN-OS [Admin Guide](https://docs.paloaltonetworks.com/vm-series/8-1/vm-series-deployment/bootstrap-the-vm-series-firewall.html#).
	
	2. Prepare the environment at the vSphere by creating Folder, Resource Pool, and port groups.
	
	3. Deploy the PA-VM from datastore template. And attach the bootstrapping ISO.
	
	4. The PA-VM will automatically start the bootstrapping process and retrieve the licenses from Palo Alto Networks License Server.
	
	5. After retrieving the license, the PA-VM will contact Panorama for the configuration (i.e., Network and security policies).

2- Scale UP or Scale Down the PA-VM
Using **scaleUp.yml** and **scaleUp.yml** you can scale up or scale down the PA-VM model. For example, you can scale up from VM-50 to VM-100 or from VM-100 to VM-50
![Scaling](https://raw.githubusercontent.com/mohanadelamin/pa-vm-ansible/master/others/ScaleUP_DOWN.png)

**scaleUp.yml** and **scaleUp.yml** playbooks do the following tasks:

	1. Deactivate the old model license.
	
	2. Shutdown the PA-VM and modify the HW resources to match the new VM model. Check Palo Alto Networks Guide for the HW requirement per model [Admin Guide](https://docs.paloaltonetworks.com/vm-series/8-1/vm-series-deployment/about-the-vm-series-firewall/vm-series-models/vm-series-system-requirements.html#)
	
	3. Power on the PA-VM and retrieve the new license.
	
	4. Finally, update panorama with the new Serial Number.

*This use case can be done differently. For example, you can overprovision the PA-VM HW resources and then use [Upgrade the VM-Series Model process](https://docs.paloaltonetworks.com/vm-series/8-1/vm-series-deployment/about-the-vm-series-firewall/upgrade-the-vm-series-firewall/upgrade-the-vm-series-model.html#)*

3- Remove the deployment.
Using **remove.yml** you can remove the deployment. The playbooks will do the following tasks:

	1. Deactivate the PA-VM licenses.
	
	2. Remove the resources from vCenter (VM, Resource pool, Folder, bootstrapping ISO and Portgroups).

4- Deploy and remove PA-VM Active/Passive HA Cluster.
Using **deployHA.yml** and **removeHA.yml** you can deploy active/passive HA cluster. The playbook will also make sure every PA-VM run in separate host by applying VM/Host affinity rule.

![HA](https://raw.githubusercontent.com/mohanadelamin/pa-vm-ansible/master/others/DeployHA.png)

**deployHA.yml** does the following tasks:

	1. Prepare the bootstrapping iso file required to bootstrap PAN-OS and Upload the image to the datastore. More information about bootstrapping can found at PAN-OS [Admin Guide](https://docs.paloaltonetworks.com/vm-series/8-1/vm-series-deployment/bootstrap-the-vm-series-firewall.html#).
	
	2. Prepare the environment at the vSphere by creating Folder, Resource Pool, and port groups.
	
	3. Deploy the Active and Passive PA-VM from datastore template. And attach the bootstrapping ISO. Also, VM/Host affinity rule in order make sure every VM on the cluster is deployed on a separate ESXi Host.
	
	4. The PA-VM will automatically start the bootstrapping process and retrieve the licenses from Palo Alto Networks License Server.
	
	5. After retrieving the license, the PA-VM will contact Panorama for the configuration (i.e., HA configuration, Network, and security policies).

Using **removeHA.yml** does the following tasks:

	1. Deactivate the PA-VM licenses.
	
	2. Remove the resources from vCenter (VMs, Resource pool, Folder, bootstrapping ISOs and Portgroups).

## Usage
1. Prerequisites. To use this playbook you will need the following packages installed on the Ansible Control Machine (Tested on Ansible 2.7 for MacOS and Ubuntu):

	1. Python 2.7
	
	2. pan-python
	```bash
	pip install pan-python
	```

	3. pyvmomi
	```bash
	pip install pyvmomi
	```

	4. For Linux you will need mkisofs
	```bash
	apt-get install mkisofs
	```

2. Create PA-VM Base image template on vCenter.

	1. Download PAN-OS Base image OVA for ESXi from Palo Alto Networks [Support Portal](http://support.paloaltonetworks.com/)
	
	2. Import the OVA to you vCenter Cluster. (Do not power on the VM)
	
	3. Right-click the VM and select **Template** > **Convert to Template**

3. Download the files:
	```bash
	git clone https://github.com/mohanadelamin/pa-vm-ansible.git
	```

4. Change the variable file **variables.yml** to meet your requirements.
	```bash
	cd pa-vm-ansible/
	vim variables.yml
	```

5. Run the playbook. (For example)
	```bash
	ansible-playbook deploy.yml
	```

## Disclaimer

These playbooks is supplied "AS IS" without any warranties and support.