def run(stackargs):

    import json

    # instantiate stack
    stack = newStack(stackargs)

    stack.parse.add_required(key="name")
    stack.parse.add_required(key="config_env",choices=["private", "public"],default="private")
    stack.parse.add_optional(key="aws_default_region",default="us-east-1")
    stack.parse.add_optional(key="insert_env_vars",default='["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]')

    # Add shelloutconfigs
    stack.add_shelloutconfig('elasticdev:::aws::ec2_ami')

    # Initialize
    stack.init_variables()
    stack.init_shelloutconfigs()

    # get image info
    image = stack.get_image(name=stack.name,
                            itype="ami",
                            region=stack.aws_default_region,
                            config_env=stack.config_env)

    env_vars = {"AWS_DEFAULT_REGION":stack.aws_default_region}
    env_vars["METHOD"] = "make_public"
    env_vars["IMAGE_ID"] = image

    inputargs = {"display":True}
    inputargs["human_description"] = 'Making image_id {} public with shelloutconfig "{}"'.format(image,stack.shelloutconfig)
    inputargs["insert_env_vars"] = stack.insert_env_vars
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["retries"] = stack.retries
    inputargs["timeout"] = stack.timeout
    inputargs["wait_last_run"] = stack.wait_last_run
    stack.ec2_ami.run(**inputargs)

    return stack.get_results()
