def run(stackargs):

    import json

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="vpc_name")
    stack.parse.add_required(key="stateful_id",default="_random")
    stack.parse.add_optional(key="insert_env_vars",default='["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]')
    
    # clobber templated file if already exists
    stack.parse.add_optional(key="use_docker",default=True)

    # docker image to execute terraform with
    stack.parse.add_optional(key="docker_exec_env",default="elasticdev/terraform-run-env")

    stack.parse.add_optional(key="clobber",default=True)
    stack.parse.add_optional(key="cidr",default="10.10.0.0/16")
    stack.parse.add_optional(key="subnet_base",default="10.10")
    stack.parse.add_optional(key="aws_default_region",default="us-east-1")
    stack.parse.add_optional(key="availability_zones",default=["us-east-1b", "us-east-1a", "us-east-1c"])

    # Add execgroup
    stack.add_execgroup("elasticdev:::aws::simple_vpc")

    # Initialize 
    stack.init_variables()
    stack.init_execgroups()

    stack.set_variable("resource_type","vpc")

    # Execute execgroup
    env_vars = {"NAME":stack.vpc_name}
    env_vars["CLOBBER"] = True
    env_vars["VPC_NAME"] = stack.vpc_name
    env_vars["CIDR"] = stack.cidr
    env_vars["STATEFUL_ID"] = stack.stateful_id
    env_vars["METHOD"] = "create"
    env_vars["AWS_DEFAULT_REGION"] = stack.aws_default_region
    env_vars["AVAILABILITY_ZONES"] = stack.availability_zones
    env_vars["RESOURCE_TYPE"] = stack.resource_type
    env_vars["RESOURCE_TAGS"] = [ stack.resource_type, stack.vpc_name, stack.aws_default_region]

    if stack.use_docker:
        env_vars["USE_DOCKER"] = True
        env_vars["DOCKER_EXEC_ENV"] = stack.docker_exec_env
        docker_env_fields_keys = env_vars.keys()
        docker_env_fields_keys.append("AWS_ACCESS_KEY_ID")
        docker_env_fields_keys.append("AWS_SECRET_ACCESS_KEY")
        # we do not include method in the .env file for docker builds
        docker_env_fields_keys.remove("METHOD")

        env_vars["DOCKER_ENV_FIELDS"] = ",".join(docker_env_fields_keys)

    os_template_vars = [ "AWS_DEFAULT_REGION", "AVAILABILITY_ZONES", "VPC_NAME", "CIDR" ]

    for _digit in range(1,21):
        _key = "CIDR_SUBNET{}".format(_digit)
        env_vars[_key] = "{}.{}.0/24".format(stack.subnet_base,str(_digit))
        os_template_vars.append(_key)

    env_vars["OS_TEMPLATE_VARS"] = ",".join(os_template_vars)

    inputargs = {"insert_env_vars":stack.insert_env_vars}
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["name"] = stack.vpc_name
    inputargs["stateful_id"] = stack.stateful_id
    stack.simple_vpc.insert(**inputargs)

    return stack.get_results()
