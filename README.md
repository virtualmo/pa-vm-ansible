# Example Ansible playbooks to automate the deployment and scaling up/down of Palo Alto Networks VM-Series

## Usecases
The following use cases can be accomplished via this ansible playbooks.
1. Deploy Standalone PA-VM
Using **deploy.yml** playbooks, you can deploy standalone PA-VM.
![Standalone](https://raw.githubusercontent.com/mohanadelamin/pa-vm-ansible/master/others/Deploy.png)

**deploy.yml** playbook does the following tasks:
	i. Prepare the bootstrapping iso file required to bootstrap PAN-OS and Upload the image to the datastore. More information about bootstrapping can found at PAN-OS [Admin Guide](https://docs.paloaltonetworks.com/vm-series/8-1/vm-series-deployment/bootstrap-the-vm-series-firewall.html#).
	ii. Prepare the environment at the vSphere by creating Folder, Resource Pool, and port groups.
	iii. Deploy the PA-VM from datastore template. And attach the bootstrapping ISO.
	iv. The PA-VM will automatically start the bootstrapping process and retrieve the licenses from Palo Alto Networks License Server.
	v. After retrieving the license, the PA-VM will contact Panorama for the configuration (i.e., Network and security policies).

2- Scale UP or Scale Down the PA-VM
Using **scaleUp.yml** and **scaleUp.yml** you can scale up or scale down the PA-VM model. For example, you can scale up from VM-50 to VM-100 or from VM-100 to VM-50
![Scaling](https://raw.githubusercontent.com/mohanadelamin/pa-vm-ansible/master/others/ScaleUP_DOWN.png)

**scaleUp.yml** and **scaleUp.yml** playbooks do the following tasks:
	i. Deactivate the old model license.
	ii. Shutdown the PA-VM and modify the HW resources to match the new VM model. Check Palo Alto Networks Guide for the HW requirement per model [Admin Guide](https://docs.paloaltonetworks.com/vm-series/8-1/vm-series-deployment/about-the-vm-series-firewall/vm-series-models/vm-series-system-requirements.html#)
	iii. Power on the PA-VM and retrieve the new license.
	iv. Finally, update panorama with the new Serial Number.

*This use case can be done differently. For example, you can overprovision the PA-VM HW resources and then use [Upgrade the VM-Series Model process](https://docs.paloaltonetworks.com/vm-series/8-1/vm-series-deployment/about-the-vm-series-firewall/upgrade-the-vm-series-firewall/upgrade-the-vm-series-model.html#)*

3- Remove the deployment.
Using **remove.yml** you can remove the deployment. The playbooks will do the following tasks:
	i. Deactivate the PA-VM licenses.
	ii. Remove the resources from vCenter (VM, Resource pool, Folder, bootstrapping ISO and Portgroups).

4- Deploy and remove PA-VM Active/Passive HA Cluster.
Using **deployHA.yml** and **removeHA.yml** you can deploy active/passive HA cluster. The playbook will also make sure every PA-VM run in separate host by applying VM/Host affinity rule.

![HA](https://raw.githubusercontent.com/mohanadelamin/pa-vm-ansible/master/others/DeployHA.png)

**deployHA.yml** does the following tasks:
	i. Prepare the bootstrapping iso file required to bootstrap PAN-OS and Upload the image to the datastore. More information about bootstrapping can found at PAN-OS [Admin Guide](https://docs.paloaltonetworks.com/vm-series/8-1/vm-series-deployment/bootstrap-the-vm-series-firewall.html#).
	ii. Prepare the environment at the vSphere by creating Folder, Resource Pool, and port groups.
	iii. Deploy the Active and Passive PA-VM from datastore template. And attach the bootstrapping ISO. Also, VM/Host affinity rule in order make sure every VM on the cluster is deployed on a separate ESXi Host.
	iv. The PA-VM will automatically start the bootstrapping process and retrieve the licenses from Palo Alto Networks License Server.
	v. After retrieving the license, the PA-VM will contact Panorama for the configuration (i.e., HA configuration, Network, and security policies).

Using **removeHA.yml** does the following tasks:
	i. Deactivate the PA-VM licenses.
	ii Remove the resources from vCenter (VMs, Resource pool, Folder, bootstrapping ISOs and Portgroups).

## Usage
1. Prerequisites. To use this playbook you will need the following packages installed on the Ansible Control Machine (Tested on Ansible 2.7 for MacOS and Ubuntu):
	i. Python 2.7
	ii. pan-python
	```bash
	pip install pan-python
	```

	iii. pyvmomi
	```bash
	pip install pyvmomi
	```

	iv. For Linux you will need mkisofs
	```bash
	apt-get install mkisofs
	```

2. Create PA-VM Base image template on vCenter.
	i. Download PAN-OS Base image OVA for ESXi from Palo Alto Networks [Support Portal](http://support.paloaltonetworks.com/)
	ii. Import the OVA to you vCenter Cluster. (Do not power on the VM)
	iii. Right-click the VM and select **Template** > **Convert to Template**

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