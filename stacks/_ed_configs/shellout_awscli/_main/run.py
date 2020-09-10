def run(stackargs):

    import json

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="name")
    stack.parse.add_required(key="aws_default_region",default="us-east-1")
    stack.parse.add_required(key="insert_env_vars",default='["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]')
    stack.parse.add_required(key="shelloutconfig")
    stack.parse.add_required(key="method",default="create")
    stack.parse.add_optional(key="add_env_vars",default="null")

    # Initialize Variables in stack
    stack.init_variables()

    # Add resource
    cmd = "resource add"
    order_type = "create-resource::api"
    role = "cloud/ec2"
    human_description = "creating resource via shelloutconfig {}".format(stack.shelloutconfig)
    env_vars = {"NAME":stack.name,"METHOD":stack.method,"AWS_DEFAULT_REGION":stack.aws_default_region}

    if stack.add_env_vars: 
        add_env_vars = stack.convert_str2json(stack.add_env_vars)
        env_vars = dict(env_vars,**add_env_vars)

    default_values = {"insert_env_vars":stack.insert_env_vars}
    default_values["env_vars"] = json.dumps(env_vars)
    default_values["shelloutconfig"] = stack.shelloutconfig

    stack.insert_builtin_cmd(cmd,
                             order_type=order_type,
                             role=role,
                             human_description=human_description,
                             display=True,
                             default_values=default_values)

    return stack.get_results()
