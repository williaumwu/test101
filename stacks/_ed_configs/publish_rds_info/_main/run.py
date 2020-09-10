def run(stackargs):

    # instantiate stack
    stack = newStack(stackargs)

    # add variables
    stack.parse.add_required(key="db_instance_name")
    stack.parse.add_required(key="db_root_user",default="null")
    stack.parse.add_required(key="db_root_password",default="null")
    stack.parse.add_required(key="engine",default="MySQL")

    stack.parse.add_optional(key="db_name",default="null")
    stack.parse.add_optional(key="db_user",default="null")
    stack.parse.add_optional(key="db_password",default="null")

    # init the stack namespace
    stack.init_variables()

    database_info = stack.get_resource(name=stack.db_instance_name,
                                       resource_type="database",
                                       must_exists=True)[0]

    keys2pass = ['zone','vpc']
    pipeline_env_var = stack.add_dict2dict(keys2pass,{},database_info,addNone=None)

    db_endpoint = database_info["endpoint"]["Address"]
    db_port = database_info["endpoint"]["Port"]

    if stack.engine:
        pipeline_env_var["{}_INSTANCE_NAME".format(stack.engine.upper())] = stack.db_instance_name
        pipeline_env_var["{}_ROOT_USER".format(stack.engine.upper())] = stack.db_root_user
        pipeline_env_var["{}_ROOT_PASSWORD".format(stack.engine.upper())] = stack.db_root_password
        pipeline_env_var["{}_ENDPOINT".format(stack.engine.upper())] = db_endpoint
        pipeline_env_var["{}_HOST".format(stack.engine.upper())] = db_endpoint
        pipeline_env_var["{}_PORT".format(stack.engine.upper())] = db_port

        if stack.db_name: pipeline_env_var["{}_DB_NAME".format(stack.engine.upper())] = stack.db_name
        if stack.db_user: pipeline_env_var["{}_DB_USER".format(stack.engine.upper())] = stack.db_user
        if stack.db_password: pipeline_env_var["{}_DB_PASSWORD".format(stack.engine.upper())] = stack.db_password
    else:
        pipeline_env_var["DB_INSTANCE_NAME"] = stack.db_instance_name
        pipeline_env_var["DB_ROOT_USER"] = stack.db_root_user
        pipeline_env_var["DB_ROOT_PASSWORD"] = stack.db_root_password
        pipeline_env_var["DB_ENDPOINT"] = db_endpoint
        pipeline_env_var["DB_HOST"] = db_endpoint
        pipeline_env_var["DB_PORT"] = db_port
        if stack.db_name: pipeline_env_var["DB_NAME"] = stack.db_name
        if stack.db_user: pipeline_env_var["DB_USER"] = stack.db_user
        if stack.db_password: pipeline_env_var["DB_PASSWORD"] = stack.db_password

    stack.add_host_env_vars_to_run(pipeline_env_var)
    stack.publish(pipeline_env_var,**stackargs)

    return stack.get_results()
