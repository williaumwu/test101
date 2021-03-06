**Description**

  - This will make an ami publically available.

**Required**

| *argument*           | *description*                            | *var type* |  *default*      |
| ------------- | -------------------------------------- | -------- | ------------ |
| name         | name of the ami image - should be unique                 | string   | None         |
| config_env      | the environmental where the ami information can be found     | choices: public,private   | private    |

**Optional**

| *argument*           | *description*                            | *var type* |  *default*      |
| ------------- | -------------------------------------- | -------- | ------------ |
| aws_default_region      | aws region - must be the same as where the hostname resides      | string   | us-east-1         |
| shelloutconfig      | shelloutconfig for creating ami      | string   | elasticdev:::aws::ec2_ami         |
| insert_env_vars      | environmental variables for user to include      | list   | ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]     |

**Sample entry (as substack):**

```
overide_values = {"name":"app-snapshot-1"}
overide_values["config_env"] = "public"
default_values = {"region":"us-east-1"

inputargs = {"default_values":default_values,
             "overide_values":overide_values}

human_description = 'Making the ami image'
inputargs["automation_phase"] = "infrastructure"
inputargs["human_description"] = human_description
stack.make_public_ami.insert(display=True,**inputargs)
```
