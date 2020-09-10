def run(stackargs):

    import json
    
    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="name")
    stack.parse.add_required(key="aws_default_region",default="us-east-1")
    stack.parse.add_required(key="insert_env_vars",default='["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]')

    # Add shelloutconfig dependencies
    stack.add_shelloutconfig('elasticdev:::aws::apigateway',"apigateway_script")

    # Initialize Variables in stack
    stack.init_variables()
    stack.init_substacks()
    stack.init_shelloutconfigs()

    stack.env_vars = {"INSERT_IF_EXISTS":True}
    stack.env_vars["NAME"] = stack.name
    stack.env_vars["AWS_DEFAULT_REGION"] = stack.aws_default_region
    stack.env_vars["METHOD"] = "create"

    inputargs = {"display":True}
    inputargs["human_description"] = "Creates an AWS api gateway"
    inputargs["insert_env_vars"] = stack.insert_env_vars
    inputargs["env_vars"] = json.dumps(stack.env_vars)
    inputargs["automation_phase"] = "infrastructure"
    inputargs["retries"] = 2
    inputargs["timeout"] = 60
    inputargs["wait_last_run"] = 2
    stack.apigateway_script.resource_exec(**inputargs)

    return stack.get_results()
