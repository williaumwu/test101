**Description**

  - This will copy an ami from one region to another region.  It is also commonly used to create an encrypted ami if encrypted is set to True.

**Required**

| *argument*           | *description*                            | *var type* |  *default*      |
| ------------- | -------------------------------------- | -------- | ------------ |
| name         | the unique name for the new ami image                 | string   | None         |
| label         | label for the ami image - not unique                 | string   | None         |
| src_name         | source name of the ami image - should be unique                 | string   | None         |
| config_env      | the environmental where the source ami information can be found     | choices: public,private   | private    |

**Optional**

| *argument*           | *description*                            | *var type* |  *default*      |
| ------------- | -------------------------------------- | -------- | ------------ |
| shelloutconfig      | shelloutconfig for creating ami      | string   | elasticdev:::aws::ec2_ami         |
| insert_env_vars      | environmental variables for user to include      | list   | ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]     |
| src_region      | source aws region for the source ami image      | string   | us-east-1         |
| dst_region      | destination aws region for the new ami image      | string   | us-east-1         |
| verify      | wait to verify the new image has completed successfully    | boolean  | null    |
| encrypted      | option to create encrypted amis    | boolean  | null    |


**Sample entry (as substack):**

```
default_values = {"src_name":"app-01-east"}
default_values["name"] = "app-01-encrypted'
default_values["label"] = 'app-01'
default_values["encrypted"] = True
default_values["src_region"] = "us-east-1'
default_values["dst_region"] = "us-east-1'
default_values["config_env"] = 'public'
default_values["verify"] = True

human_description = 'Encrypting the ami image'
inputargs = {"default_values":default_values}
inputargs["automation_phase"] = "infrastructure"
inputargs["human_description"] = human_description
stack.copy_ami.insert(display=True,**inputargs)
```
