DICT_CREDENTIALS_TYPE = dict(
	cloud = ['amazon_ec2', 'azure_rm'],
	)




DICT_CREDENTIALS = dict(
	generic = [{
		"name": "inventory",
		"label": "Hostname or IP",
		"type": "text",
		"required": 1,
		"help_text": "Enter remote IP or Hostname"
	},
	{
		"name": "username",
		"label": "Username",
		"type": "text",
		"required": 1,
		"help_text": "Enter your Username"
	},

	{
		"name": "password",
		"label": "Password",
		"type": "password",
		"required": 1,
		"help_text": "Enter your SSH Password"
	},

	],

	kvm = [{
		"name": "inventory",
		"label": "Hostname or IP",
		"type": "text",
		"required": 1,
		"help_text": "Enter remote IP or Hostname"
	},
	{
		"name": "username",
		"label": "Username",
		"type": "text",
		"required": 1,
		"help_text": "Enter your Username"
	},
	{
		"name": "password",
		"label": "Password",
		"type": "password",
		"required": 1,
		"help_text": "Enter your SSH Password"
	},


	],

	appliance = [{
		"name": "inventory",
		"label": "Hostname or IP",
		"type": "text",
		"required": 1,
		"help_text": "Enter remote IP or Hostname"
	},
	{
		"name": "username",
		"label": "Appliance Username",
		"type": "text",
		"max_length": 25,
		"required": 1,
		"help_text": "Enter appliance Username"
	},
	{
		"name": "password",
		"label": "Appliance Password",
		"type": "password",
		"max_length": 25,
		"required": 1,
		"help_text": "Enter Appliance Password"
	},

	],

	amazon_ec2 = [{
		"name": "AWS_ACCESS_KEY_ID",
		"label": "AWS ACCESS KEY ID",
		"type": "text",
		"required": 1,
		"help_text": "AWS Access Key ID"
	},
	{
		"name": "AWS_SECRET_ACCESS_KEY",
		"label": "AWS SECRET ACCESS KEY",
		"type": "password",
		"required": 1,
		"help_text": "AWS Access Key"
	},
	{
		"name": "AWS_SECURITY_TOKEN",
		"label": "AWS SECURITY TOKEN",
		"type": "text",
		"help_text": "AWS Security Token"
	},

	{
		"name": "AWS_REGION",
		"label": "AWS REGION",
		"type": "select",
		"help_text": "AWS Region",
		"choices": [
		# https://docs.aws.amazon.com/general/latest/gr/rande.html
					{
						"name": "EU (Frankfurt)",
						"value": "eu-central-1",
					 },
					{
						"name": "EU (Ireland)",
						"value": "eu-west-1",
					 },

					{
						"name": "EU (London)",
						"value": "eu-west-2",
					 },

					{
						"name": "EU (Paris)",
						"value": "eu-west-3",
					 },


					]
	},



	],

	ms_azure = [{
		"name": "AZURE_SUBSCRIPTION_ID",
		"label": "AZURE SUBSCRIPTION ID",
		"type": "text",
		"required": 1,
		"help_text": "AZURE SUBSCRIPTION ID"
	},
	{
		"name": "AZURE_CLIENT_ID",
		"label": "AZURE CLIENT ID",
		"type": "text",
		"required": 1,
		"help_text": "AZURE CLIENT ID"
	},
	{
		"name": "AZURE_TENANT",
		"label": "AZURE TENANT",
		"type": "text",
		"required": 1,
		"help_text": "AZURE TENANT"
	},

	{
		"name": "AZURE_SECRET",
		"label": "AZURE SECRET",
		"type": "password",
		"required": 1,
		"help_text": "AZURE SECRET"
	},

	{
		"name": "AZURE_AD_USER",
		"label": "AZURE AD USER",
		"type": "text",
		"required": 0,
		"help_text": "AZURE TENANT"
	},

	{
		"name": "AZURE_PASSWORD",
		"label": "AZURE PASSWORD",
		"type": "password",
		"required": 0,
		"help_text": "AZURE PASSWORD"
	},

	{
		"name": "AZURE_CLOUD_ENVIRONMENT",
		"label": "AZURE CLOUD ENVIRONMENT",
		"type": "password",
		"required": 0,
		"help_text": "AZURE CLOUD ENVIRONMENT"
	},


	],

	vmware = [{
		"name": "VMWARE_HOST",
		"label": "VMWARE HOST",
		"type": "text",
		"required": 1,
		"help_text": "VMWARE HOST"
	},
	{
		"name": "VMWARE_USER",
		"label": "VMWARE USER",
		"type": "text",
		"required": 1,
		"help_text": "VMWARE USER"
	},
	{
		"name": "VMWARE_PASSWORD",
		"label": "VMWARE PASSWORD",
		"type": "password",
		"required": 1,
		"help_text": "VMWARE PASSWORD"
	},
	{
		"name": "VMWARE_VALIDATE_CERTS",
		"label": "VMWARE VALIDATE CERTS",
		"type": "checkbox",
		"required": 1,
		"help_text": "VMWARE VALIDATE CERTS"
	},

	],


)



# # Basic provisioning example
# - ec2:
#     key_name: mykey
#     instance_type: t2.micro
#     image: ami-123456
#     wait: yes
#     group: webserver
#     count: 3
#     vpc_subnet_id: subnet-29e63245
#     assign_public_ip: yes




DICT_WIZARDBOXFORMS = dict(

	default = [
	{
		"name": "default_instance_name",
		"label": "instance name",
		"type": "text",
		"required": 1,
		"help_text": "instance name"
	},

	],


	ec2 = [
	{
		"name": "ec2_instance_name",
		"label": "instance name",
		"type": "text",
		"required": 1,
		"help_text": "instance name"
	},
	{
		"name": "ec2_instance_type",
		"label": "instance type",
		"type": "text",
		"required": 1,
		"help_text": "t2.micro"
	},

	{
		"name": "ec2_image",
		"label": "image",
		"type": "text",
		"required": 1,
		"help_text": "ami-123456"
	},

	],

	kvm = [{
		"name": "inventory",
		"label": "Hostname or IP",
		"type": "text",
		"required": 1,
		"help_text": "Enter remote IP or Hostname"
	},
	{
		"name": "username",
		"label": "Username",
		"type": "text",
		"required": 1,
		"help_text": "Enter your Username"
	},
	{
		"name": "password",
		"label": "Password",
		"type": "password",
		"required": 1,
		"help_text": "Enter your SSH Password"
	},


	],

	appliance = [{
		"name": "inventory",
		"label": "Hostname or IP",
		"type": "text",
		"required": 1,
		"help_text": "Enter remote IP or Hostname"
	},
	{
		"name": "username",
		"label": "Appliance Username",
		"type": "text",
		"max_length": 25,
		"required": 1,
		"help_text": "Enter appliance Username"
	},
	{
		"name": "password",
		"label": "Appliance Password",
		"type": "password",
		"max_length": 25,
		"required": 1,
		"help_text": "Enter Appliance Password"
	},

	],

	amazon_ec2 = [{
		"name": "AWS_ACCESS_KEY_ID",
		"label": "AWS ACCESS KEY ID",
		"type": "text",
		"required": 1,
		"help_text": "AWS Access Key ID"
	},
	{
		"name": "AWS_SECRET_ACCESS_KEY",
		"label": "AWS SECRET ACCESS KEY",
		"type": "password",
		"required": 1,
		"help_text": "AWS Access Key"
	},
	{
		"name": "AWS_SECURITY_TOKEN",
		"label": "AWS SECURITY TOKEN",
		"type": "text",
		"help_text": "AWS Security Token"
	},

	{
		"name": "AWS_REGION",
		"label": "AWS REGION",
		"type": "select",
		"help_text": "AWS Region",
		"choices": [
		# https://docs.aws.amazon.com/general/latest/gr/rande.html
					{
						"name": "EU (Frankfurt)",
						"value": "eu-central-1",
					 },
					{
						"name": "EU (Ireland)",
						"value": "eu-west-1",
					 },

					{
						"name": "EU (London)",
						"value": "eu-west-2",
					 },

					{
						"name": "EU (Paris)",
						"value": "eu-west-3",
					 },


					]
	},



	],

	ms_azure = [{
		"name": "AZURE_SUBSCRIPTION_ID",
		"label": "AZURE SUBSCRIPTION ID",
		"type": "text",
		"required": 1,
		"help_text": "AZURE SUBSCRIPTION ID"
	},
	{
		"name": "AZURE_CLIENT_ID",
		"label": "AZURE CLIENT ID",
		"type": "text",
		"required": 1,
		"help_text": "AZURE CLIENT ID"
	},
	{
		"name": "AZURE_TENANT",
		"label": "AZURE TENANT",
		"type": "text",
		"required": 1,
		"help_text": "AZURE TENANT"
	},

	{
		"name": "AZURE_SECRET",
		"label": "AZURE SECRET",
		"type": "password",
		"required": 1,
		"help_text": "AZURE SECRET"
	},

	{
		"name": "AZURE_AD_USER",
		"label": "AZURE AD USER",
		"type": "text",
		"required": 0,
		"help_text": "AZURE TENANT"
	},

	{
		"name": "AZURE_PASSWORD",
		"label": "AZURE PASSWORD",
		"type": "password",
		"required": 0,
		"help_text": "AZURE PASSWORD"
	},

	{
		"name": "AZURE_CLOUD_ENVIRONMENT",
		"label": "AZURE CLOUD ENVIRONMENT",
		"type": "password",
		"required": 0,
		"help_text": "AZURE CLOUD ENVIRONMENT"
	},


	],

	vmware = [{
		"name": "VMWARE_HOST",
		"label": "VMWARE HOST",
		"type": "text",
		"required": 1,
		"help_text": "VMWARE HOST"
	},
	{
		"name": "VMWARE_USER",
		"label": "VMWARE USER",
		"type": "text",
		"required": 1,
		"help_text": "VMWARE USER"
	},
	{
		"name": "VMWARE_PASSWORD",
		"label": "VMWARE PASSWORD",
		"type": "password",
		"required": 1,
		"help_text": "VMWARE PASSWORD"
	},
	{
		"name": "VMWARE_VALIDATE_CERTS",
		"label": "VMWARE VALIDATE CERTS",
		"type": "checkbox",
		"required": 1,
		"help_text": "VMWARE VALIDATE CERTS"
	},

	],


)
