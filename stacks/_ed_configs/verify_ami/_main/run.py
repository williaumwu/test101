def run(stackargs):

    import json

    # instantiate stack
    stack = newStack(stackargs)

    stack.parse.add_required(key="name")
    stack.parse.add_required(key="config_env",choices=["private", "public"],default="private")

    stack.parse.add_optional(key="aws_default_region",default="us-east-1")
    stack.parse.add_optional(key="insert_env_vars",default='["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]')
    stack.parse.add_optional(key="wait_last_run",default=60)
    stack.parse.add_optional(key="retries",default=20)
    stack.parse.add_optional(key="timeout",default=1800)

    # Add shelloutconfigs
    stack.add_shelloutconfig('elasticdev:::aws::ec2_ami')

    # init the stack namespace
    stack.init_variables()

    # get image info
    image = stack.get_image(name=stack.name,
                            itype="ami",
                            region=stack.aws_default_region,
                            config_env=stack.config_env)

    env_vars = {"AWS_DEFAULT_REGION":stack.aws_default_region}
    env_vars["METHOD"] = "confirm"
    env_vars["IMAGE_ID"] = image

    inputargs = {"human_description":'Verifying image_id {} with shelloutconfig "{}"'.format(image,stack.shelloutconfig)}
    inputargs["insert_env_vars"] = stack.insert_env_vars
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["retries"] = stack.retries
    inputargs["timeout"] = stack.timeout
    inputargs["wait_last_run"] = stack.wait_last_run
    inputargs["display"] = True
    stack.ec2_ami.run(**inputargs)

    return stack.get_results()
