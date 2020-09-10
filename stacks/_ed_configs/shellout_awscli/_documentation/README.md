# The stack is a wrapper to used by other AWS cli related stacks

e.g. Call to create the api gateway

default_values = {"name":stack.name}
default_values["region"] = stack.region
default_values["method"] = "create"
default_values["insert_env_vars"] = stack.insert_env_vars
default_values["shelloutconfig"] = stack.shelloutconfig
if stack.add_env_vars: default_values["add_env_vars"] = stack.add_env_vars

inputargs = {"default_values":default_values}
inputargs["automation_phase"] = "infrastructure"
inputargs["human_description"] = "Creates an AWS api gateway"
stack.shellout_awscli.insert(display=None,**inputargs)

