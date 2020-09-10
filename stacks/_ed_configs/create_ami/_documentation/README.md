**Description**

  - This will create an ami on aws provided the hostname of the machine

**Infrastructure**

  - expects a hostname to be to create the ami from

**Required**

| *argument*           | *description*                            | *var type* |  *default*      |
| ------------- | -------------------------------------- | -------- | ------------ |
| hostname         | hostname to create the ami from                 | string   | None         |
| label         | label for the ami image - not unique                 | string   | None         |
| aws_default_region      | aws region - must be the same as where the hostname resides      | string   | us-east-1         |

**Optional**

| *argument*           | *description*                            | *var type* |  *default*      |
| ------------- | -------------------------------------- | -------- | ------------ |
| shelloutconfig      | shelloutconfig for creating ami      | string   | elasticdev:::aws::ec2_ami         |
| insert_env_vars      | environmental variables for user to include      | list   | ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]     |
| copy_regions      | after creating the ami, the regions to make copy of the ami      | list   | null    |
| config_env      | the environmental to share or not share the ami image information     | choices: public,private   | private    |
| verify      | wait to verify the image has completed successfully    | boolean  | null    |
| encrypted      | option to create encrypted amis    | boolean  | null    |

**Sample entry (as substack):**

```
# create ami for docker run
default_values = {"hostname":"app-01"}
default_values["label"] = "main_app"
default_values["copy_regions"] = ["us-west-1","ap-southeast-1"]
default_values["encrypted"] = True

inputargs = {"default_values":default_values}
inputargs["automation_phase"] = "build_ami"
inputargs["human_description"] ="Creating ami for docker build workers"
inputargs["display"] = True
inputargs["display_hash"] = stack.get_hash_object(inputargs)
stack.create_ami.insert(display=True,**inputargs)

```

**Sample entry (in elasticdev.yml):**

```
infrastructure:
   ami:
       stack_name: elasticdev:::create_ami
       arguments:
          aws_default_region: us-west-2
          instance_id: i-08a07cf9a972748c4
          label: php-app
          encrypted: True
          copy_regions:
              - us-east-1
```
