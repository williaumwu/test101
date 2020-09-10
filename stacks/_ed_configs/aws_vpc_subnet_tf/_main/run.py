def run(stackargs):

    import json

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="vpc_name")
    stack.parse.add_optional(key="insert_env_vars",default='["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]')
    
    # clobber templated file if already exists
    stack.parse.add_optional(key="clobber",default=True)
    stack.parse.add_required(key="subnet_base")
    stack.parse.add_optional(key="aws_default_region",default="us-east-1")
    stack.parse.add_required(key="availability_zones")
    stack.parse.add_required(key="subnet_labels")

    # Add execgroup
    stack.add_execgroup("elasticdev:::aws::subnet_tf")

    # Initialize 
    stack.init_variables()
    stack.init_execgroups()

    vpc_lookup = {"must_exists":True}
    vpc_lookup["resource_type"] = "vpc"
    vpc_lookup["provider"] = "aws"
    vpc_lookup["vpc"] = stack.vpc_name
    vpc_info = list(stack.get_resource(**vpc_lookup))[0]

    stack.set_parallel()

    # env_var base for subnet creation
    env_vars = {"NAME":stack.vpc_name}
    env_vars["VPC_NAME"] = stack.vpc_name
    env_vars["VPC_ID"] = vpc_info["vpc_id"]
    env_vars["CLOBBER"] = True
    env_vars["METHOD"] = "create"
    env_vars["AWS_DEFAULT_REGION"] = stack.aws_default_region
    env_vars["RESOURCE_TYPE"] = "subnet"
    env_vars["TERRAFORM_TEMPLATE_FILES"] = "subnet"
    os_template_vars = [ "AWS_DEFAULT_REGION", "TERRAFORM_TEMPLATE_FILES", "SUBNET_LABEL", "SUBNET_NAME", "VPC_NAME", "VPC_ID", "CIDR_SUBNET", "AVAILABILITY_ZONE" ]
    env_vars["OS_TEMPLATE_VARS"] = ",".join(os_template_vars)

    _subnet_digit = 11

    for _subnet_label in stack.subnet_labels:

        _subnet_label_digit = 0

        for availiability_zone in stack.availability_zones:
            
            _subnet_digit += 1
            _subnet_label_digit += 1

            subnet_name = "{}-{}-{}".format(stack.vpc_name,_subnet_label,_subnet_label_digit)
            stateful_id = stack.random_id()

            env_vars["SUBNET_NAME"] = subnet_name
            env_vars["SUBNET_LABEL"] = _subnet_label
            env_vars["CIDR_SUBNET"] = "{}.{}.0/24".format(stack.subnet_base,str(_subnet_digit))
            env_vars["STATEFUL_ID"] = stateful_id
            env_vars["AVAILABILITY_ZONE"] = availiability_zone
            env_vars["RESOURCE_TAGS"] = [ "subnet", _subnet_label, subnet_name, availiability_zone, stack.vpc_name, stack.aws_default_region ]

            inputargs = {"insert_env_vars":stack.insert_env_vars}
            inputargs["env_vars"] = json.dumps(env_vars)
            inputargs["name"] = subnet_name
            inputargs["stateful_id"] = stateful_id
            stack.subnet_tf.insert(**inputargs)

    return stack.get_results()
