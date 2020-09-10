def run(stackargs):

    import json

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="name")
    stack.parse.add_required(key="aws_default_region",default="us-east-1")
    stack.parse.add_required(key="insert_env_vars",default='["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]')
    stack.parse.add_required(key="shelloutconfig",default='elasticdev:::aws::apigateway')
    stack.parse.add_required(key="cert_group",default="null")
    stack.parse.add_required(key="cert_name",default="null")

    stack.parse.add_optional(key="add_env_vars",default="null")
    stack.parse.add_optional(key="cert_file",default="certs/certificate")
    stack.parse.add_optional(key="cert_chain",default="certs/certificate_chain")
    stack.parse.add_optional(key="prv_key",default="certs/private_key")

    # Initialize Variables in stack
    stack.init_variables()

    cmd = "resource add"
    order_type = "upload_cert::api"
    role = "cloud/ec2"
    human_description = "upload SSL cert {} to AWS".format(stack.cert_name)

    env_vars = {"AWS_DEFAULT_REGION":stack.aws_default_region,
                "METHOD":"create",
                "CERT_FILE":stack.cert_file,
                "PRV_KEY":stack.prv_key,
                "CERT_CHAIN":stack.cert_chain,
                "NAME":stack.cert_name}

    default_values = {"insert_env_vars":stack.insert_env_vars}
    default_values["execgroup"] = stack.cert_group
    default_values["env_vars"] = env_vars
    if stack.add_env_vars: default_values["json_args"] = json.dumps(stack.add_env_vars)

    stack.insert_builtin_cmd(cmd,
                             order_type=order_type,
                             role=role,
                             human_description=human_description,
                             display=True,
                             default_values=default_values)

    return stack.get_results()
