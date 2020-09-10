def run(stackargs):

    import json


    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="vpc_name")
    stack.parse.add_optional(key="insert_env_vars",default='["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]')
    
    # clobber templated file if already exists
    stack.parse.add_optional(key="clobber",default=True)
    stack.parse.add_optional(key="main_cidr",default="10.10.0.0/16")
    stack.parse.add_optional(key="subnet_base",default="10.10")
    stack.parse.add_optional(key="aws_default_region",default="us-east-1")
    stack.parse.add_optional(key="availability_zones",default=["us-east-1b", "us-east-1a", "us-east-1c"])
    stack.parse.add_optional(key="security_groups",default="null")

    # Add substacks
    stack.add_substack('elasticdev:::aws_vpc_subnet_tf')

    # Add execgroup
    stack.add_execgroup("elasticdev:::aws::vpc_tf")

    # Initialize 
    stack.init_variables()
    stack.init_substacks()

    # Initialize execgroups
    stack.init_execgroups()

    if not stack.security_groups: 
        security_groups = {}
        security_groups["bastion"] = {}
        security_groups["bastion"]["public"] = []
        security_groups["bastion"]["public"].append({"22":["0.0.0.0/0"],"ports":"tcp"})
        security_groups["app"] = {}
        security_groups["app"]["public"] = []
        security_groups["app"]["public"].append({"22":["0.0.0.0/0"],"ports":"tcp"})
        security_groups["app"]["public"].append({"80":["0.0.0.0/0"]})
        security_groups["app"]["public"].append({"443":["0.0.0.0/0"]})
        security_groups["app"]["sg_labels"] = []
        security_groups["app"]["sg_labels"].append({"bastion":["0.0.0.0/0"]})
        security_groups["api"] = {}
        security_groups["api"]["public"] = []
        security_groups["api"]["public"].append({"22":["0.0.0.0/0"],"ports":"tcp"})
        security_groups["api"]["sg_labels"] = []
        security_groups["api"]["sg_labels"].append({"bastion":["0.0.0.0/0"]})
        security_groups["api"]["sg_labels"].append({"app":["0.0.0.0/0"]})
        security_groups["db"] = {}
        security_groups["db"]["sg_labels"] = []
        security_groups["db"]["sg_labels"].append({"bastion":["0.0.0.0/0"]})
        security_groups["db"]["sg_labels"].append({"api":["0.0.0.0/0"]})
        stack.set_variable("security_groups",security_groups)

    # Execute execgroup for creating vpc
    stateful_id = stack.random_id()

    env_vars = {"NAME":stack.vpc_name}
    env_vars["CLOBBER"] = True
    env_vars["VPC_NAME"] = stack.vpc_name
    env_vars["MAIN_CIDR"] = stack.main_cidr
    env_vars["STATEFUL_ID"] = stateful_id
    env_vars["METHOD"] = "create"
    env_vars["AWS_DEFAULT_REGION"] = stack.aws_default_region
    env_vars["RESOURCE_TYPE"] = "vpc"
    env_vars["RESOURCE_TAGS"] = [ "vpc", stack.vpc_name, stack.aws_default_region]

    os_template_vars = [ "AWS_DEFAULT_REGION","VPC_NAME", "MAIN_CIDR" ]
    env_vars["OS_TEMPLATE_VARS"] = ",".join(os_template_vars)

    inputargs = {"insert_env_vars":stack.insert_env_vars}
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["name"] = stack.vpc_name
    inputargs["stateful_id"] = stateful_id
    stack.vpc_tf.insert(**inputargs)

    stack.set_parallel()

    # Execute subnet creation
    # Add separable subnet for nat
    subnet_labels = security_groups.keys()
    subnet_labels.append("nat")
    stack.set_variable("subnet_labels",subnet_labels)

    default_values = {"vpc_name":stack.vpc_name}
    default_values["vpc"] = stack.vpc_name
    default_values["aws_default_region"] = stack.aws_default_region
    default_values["subnet_base"] = stack.subnet_base
    default_values["availability_zones"] = stack.availability_zones
    default_values["subnet_labels"] = stack.subnet_labels

    inputargs = {"default_values":default_values}
    inputargs["automation_phase"] = "infrastructure"
    inputargs["human_description"] = "Creates subnets for vpc_name {}".format(stack.vpc_name)
    stack.aws_vpc_subnet_tf.insert(display=True,**inputargs)

    return stack.get_results()
