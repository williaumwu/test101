**Description**

  - This will deregister an ami and optionally destroys the snapshot

**Required**

| *argument*           | *description*                            | *var type* |  *default*      |
| ------------- | -------------------------------------- | -------- | ------------ |
| name         | the name for the ami image                 | string   | None         |
| config_env      | the environmental where the ami information can be found     | choices: public,private   | private    |
| region      | aws region for the source ami image      | string   | us-east-1         |

**Optional**

| *argument*           | *description*                            | *var type* |  *default*      |
| ------------- | -------------------------------------- | -------- | ------------ |
| destroy      | to optionally destroy the snapshot volume on aws      | boolean   | True         |
| label      | the main label for the ami image - not unique      | string   | null        |

**Sample entry (as substack):**

```
default_values = {"name":"main-app-01}
default_values["label"] = "main-app"
default_values["region"] = "us-east-1"
default_values["destroy"] = True
stack.destroy_ami.insert(display=True,**inputargs)
```
