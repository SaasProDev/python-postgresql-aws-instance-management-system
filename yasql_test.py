import yaql
import yaml
import json

#data_source = yaml.load(open('/tmp/file.json', 'r'), Loader=yaml.safe_load)

data_source = json.loads('{"customers_city": [{"city": "New York", "customer_id": 1}, {"city": "Saint Louis", "customer_id": 2}, {"city": "Mountain View", "customer_id": 3}], "customers": [{"customer_id": 1, "name": "John", "orders": [{"order_id": 1, "item": "Guitar", "quantity": 1}]}, {"customer_id": 2, "name": "Paul", "orders": [{"order_id": 2, "item": "Banjo", "quantity": 2}, {"order_id": 3, "item": "Piano", "quantity": 1}]}, {"customer_id": 3, "name": "Diana", "orders": [{"order_id": 4, "item": "Drums", "quantity": 1}]}]}')

engine = yaql.factory.YaqlFactory().create()

query = '$.customers.orders.selectMany($.where($.order_id = 4)).where($.item = Drums).select($.item)'

expression = engine( query )
order = expression.evaluate(data=data_source)
print (order)


query = '$.customers.orders.selectMany($.where($.order_id = 4)).where($.item = Drums)'

expression = engine( query )
order = expression.evaluate(data=data_source)
print (order)


query = '$.customers.orders.selectMany($.where($.order_id = 4)).len()'

expression = engine( query )
order = expression.evaluate(data=data_source)
print (order)


query = '$.customers.orders.selectMany($.where($.order_id = 4)).where($.item = Drums).select({ "name" => $.item + "_demo" })'

expression = engine( query )
order = expression.evaluate(data=data_source)
print (order)


# query = '$.customers.orders.selectMany($.where($.order_id = 4)).where($.item = Drums).select({ "name" => $.item1 + "_demo" })'

# try:
# 	# print(f'{person} is {ages[person]} years old.')
# 	expression = engine( query )
# 	order = expression.evaluate(data=data_source)
# 	print (order)
# except KeyError as e:
# 	print (f"{e} is unknown.")



data="""
{
  "apiVersion": "v1",
  "kind": "amazon_ec2",
  "labels": {
    "amazon_ec2": "cloud provider"
  },
  "metadata": {
    "name": "aws-provider",
    "annotations": {
      "title": "Provisioning Amazon Web Services",
      "description": "Amazon Web service EC2\n",
      "iconClass": "icon-amazon-aws",
      "tags": "aws,cloud,provider"
    },
    "cloud": true
  },
  "ansibleObjects": [
    {
      "apiVersion": "v1",
      "kind": "ModelInjector",
      "metadata": {
        "name": "instance",
        "model": "core.iaas",
        "debug": "r__debug"
      },
      "spec": {
        "uniqueKeys": [
          {
            "name": "instance_id",
            "value": "xxxxx.",
            "modelRef": "instance_id",
            "yaqlRef": "$.consumers....."
          }
        ],
        "modelFields": [
          {
            "name": "image",
            "modelRef": "image",
            "valueRef": "ec2_instance_image"
          },
          {
            "name": "name",
            "valueRef": "ec2_instance_name"
          },
          {
            "name": "type",
            "valueRef": "ec2_instance_type"
          },
          {
            "name": "count",
            "valueRef": "ec2_instance_count"
          },
          {
            "name": "name",
            "modelRef": "inputs",
            "valueRef": "ec2_instance_name"
          },
          {
            "name": "count",
            "modelRef": "inputs",
            "valueRef": "ec2_instance_count"
          }
        ]
      }
    },
    {
      "apiVersion": "v1",
      "kind": "ModelInjector",
      "metadata": {
        "name": "instance",
        "model": "core.iaas",
        "debug": "r__debug1"
      },
      "spec": {
        "uniqueKeys": [
          {
            "name": "instance_id",
            "value": "xxxxx.",
            "modelRef": "instance_id",
            "yaqlRef": "$.consumers....."
          }
        ],
        "modelFields": [
          {
            "name": "image",
            "modelRef": "image",
            "valueRef": "ec2_instance_image"
          },
          {
            "name": "name",
            "valueRef": "ec2_instance_name"
          },
          {
            "name": "type",
            "valueRef": "ec2_instance_type"
          },
          {
            "name": "count",
            "valueRef": "ec2_instance_count"
          },
          {
            "name": "name",
            "modelRef": "inputs",
            "valueRef": "ec2_instance_name"
          },
          {
            "name": "count",
            "modelRef": "inputs",
            "valueRef": "ec2_instance_count"
          }
        ],
        "vars": [
          "registered_var1",
          "r__debug"
        ]
      }
    }
  ],
  "parameters": [
    {
      "description": "Password used for Redis authentication",
      "from": "[A-Z0-9]{8}",
      "generate": "expression",
      "name": "REDIS_PASSWORD"
    }
  ],
  "fields": [
    {
      "name": "ec2_instance_name",
      "label": "instance name",
      "help_text": "ex. instance1",
      "required": true
    },
    {
      "name": "ec2_instance_type",
      "label": "instance type",
      "help_text": "ex. t2.micro",
      "initial": "t2.micro",
      "type": "select",
      "choices": [
        {
          "name": "1vCPU 0.5GiB RAM $0.0058/hr",
          "value": "t2.nano"
        },
        {
          "name": "1vCPU 1GiB RAM $0.0116/hr",
          "value": "t2.micro"
        },
        {
          "name": "1vCPU 1GiB RAM $0.023/hr",
          "value": "t2.small"
        },
        {
          "name": "2vCPUs 4GiB RAM $0.0464/hr",
          "value": "t2.medium"
        },
        {
          "name": "2vCPUs 8GiB RAM $0.0928/hr",
          "value": "t2.large"
        },
        {
          "name": "4vCPUs 16GiB RAM $0.1856/hr",
          "value": "t2.xlarge"
        },
        {
          "name": "8vCPUs 32GiB RAM $0.3712/hr",
          "value": "t2.2xlarge"
        }
      ]
    },
    {
      "name": "ec2_instance_image",
      "label": "image",
      "help_text": "ex. ami-123456",
      "initial": "309956199498;RHEL-8.0.*",
      "type": "select",
      "choices": [
        {
          "name": "RHEL 6 x64",
          "value": "309956199498;RHEL-6*"
        },
        {
          "name": "RHEL 7 x64",
          "value": "309956199498;RHEL-7*"
        },
        {
          "name": "RHEL 8 x64",
          "value": "309956199498;RHEL-8.0.*"
        }
      ]
    },
    {
      "name": "ec2_wait",
      "type": "checkbox",
      "advanced": true
    },
    {
      "name": "ec2_group",
      "help_text": "ex. webserver",
      "advanced": true
    },
    {
      "name": "ec2_assign_public_ip",
      "label": "assign public ip",
      "help_text": "public ip",
      "type": "checkbox",
      "advanced": true
    },
    {
      "name": "ec2_instance_count",
      "label": "count",
      "type": "integer",
      "min_value": 1,
      "max_value": 10,
      "initial": 1,
      "advanced": false
    }
  ],
  "credentials": [
    {
      "name": "ec2_username",
      "label": "username"
    },
    {
      "name": "ec2_password",
      "type": "password",
      "label": "Password"
    },
    {
      "name": "ec2_key_name",
      "advanced": true
    },
    {
      "name": "ec2_ssh_pubkey",
      "label": "ssh public key",
      "advanced": true,
      "type": "textarea"
    }
  ]
}
"""
data_source = json.loads(data)



engine = yaql.factory.YaqlFactory().create()

query = '$.ansibleObjects.metadata.selectMany($.where($.debug = "r__debug1"))'

expression = engine( query )
order = expression.evaluate(data=data_source)
print (order)

# try:
# 	pass
# except Exception as e:
# 	raise e