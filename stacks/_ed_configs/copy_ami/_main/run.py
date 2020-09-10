def run(stackargs):

    import json

    # instantiate stack
    stack = newStack(stackargs)

    stack.parse.add_required(key="src_name")
    stack.parse.add_required(key="name")
    stack.parse.add_required(key="label")
    stack.parse.add_required(key="config_env",choices=["private","public"],default="private")

    stack.parse.add_optional(key="aws_default_region",default="us-east-1")
    stack.parse.add_optional(key="src_region",default="us-east-1")
    stack.parse.add_optional(key="dst_region",default="us-east-1")
    stack.parse.add_optional(key="encrypted",default=True)
    stack.parse.add_optional(key="verify",default='null')

    stack.parse.add_optional(key="shelloutconfig",default="elasticdev:::aws::ec2_ami")
    stack.parse.add_optional(key="insert_env_vars",default='["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]')

    # add substacks
    stack.add_substack('elasticdev:::aws::verify_ami')

    # init the stack namespace
    stack.init_variables()
    stack.init_substacks()

    # get image info
    image = stack.get_image(name=stack.src_name,
                            itype="ami",
                            region=stack.src_region,
                            config_env=stack.config_env)

    # copy image
    env_vars = {"AWS_DEFAULT_REGION":stack.aws_default_region}
    env_vars["METHOD"] = "copy"
    env_vars["NAME"] = stack.name
    env_vars["LABEL"] = stack.label
    env_vars["SRC_IMAGE_ID"] = image
    env_vars["SRC_REGION"] = stack.src_region
    env_vars["DST_REGION"] = stack.dst_region
    if stack.encrypted: env_vars["ENCRYPTED"] = True
    if stack.config_env == "public": env_vars["PUBLIC"] = True

    human_description='Copying image_id {} to name "{}"'.format(image,stack.name)

    ikwargs = {"insert_env_vars":stack.insert_env_vars}
    ikwargs["env_vars"] = json.dumps(env_vars)
    ikwargs["shelloutconfig"] = stack.shelloutconfig
    ikwargs["itype"] = "ami"
    ikwargs["config_env"] = stack.config_env

    stack.register_image(order_type="register-ami::api",
                         human_description='Creates and records AMI',
                         display=None,
                         **ikwargs)

    if stack.verify:
        overide_values = {"name":stack.name}
        overide_values["config_env"] = stack.config_env
        default_values = {"region":stack.dst_region}

        inputargs = {"default_values":default_values,
                     "overide_values":overide_values}

        human_description = 'Verifying the ami image {}'.format(stack.name)
        inputargs["automation_phase"] = "infrastructure"
        inputargs["human_description"] = human_description
        stack.verify_ami.insert(display=True,**inputargs)

    return stack.get_results()
