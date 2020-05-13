   42  ansible zeus.afahounko.com -m virt -a "name=alpha command=status"
   43  ansible all -i zeus.afahounko.com, -m virt -a "name=alpha command=status"
   44  ansible all -i zeus.afahounko.com, -m virt -a "name=community.obacy.africa command=status"
   45  ansible all -i zeus.afahounko.com, -m virt -a "command=list_vms"
   46  ansible all -i zeus.afahounko.com, -m virt -a "command=list_vms state=running"
   47  ansible all -i zeus.afahounko.com, -m virt -a "name=community.obacy.africa command=get_xml"


ansible-runner --role discover.libvirt --hosts zeus.afahounko.com --roles-path /ahome_devel/playbooks/roles run /tmp/runner


ansible-runner -m setup --hosts zeus.afahounko.com  run /tmp/runner



ansible-playbook playbooks/local.yml -i zeus.afahounko.com,

ansible all -m ping -i /opt/tmp/ahome_4a644d63-3def-4ca7-ad01-ed6d15e9a5ee_h3tbru5i/inventory/hosts

ansible-playbook local.yml -i /opt/tmp/ahome_8c08d13e-cc32-4da2-9547-2d5de5f0ffca_dh3k33w3/inventory/hosts


