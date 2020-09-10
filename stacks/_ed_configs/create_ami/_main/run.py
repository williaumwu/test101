def run(stackargs):

    #from time import sleep
    import json

    # instantiate stack
    stack = newStack(stackargs)

    # add variables
    stack.parse.add_required(key="hostname",default='null')
    stack.parse.add_required(key="instance_id",default='null')
    stack.parse.add_required(key="label")
    stack.parse.add_required(key="config_env",choices=["private", "public"],default="private")

    stack.parse.add_optional(key="aws_default_region",default="us-east-1")
    stack.parse.add_optional(key="shelloutconfig",default="elasticdev:::aws::ec2_ami")
    stack.parse.add_optional(key="insert_env_vars",default='["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]')
    stack.parse.add_optional(key="copy_regions",default="null")
    stack.parse.add_optional(key="verify",default="null")
    stack.parse.add_optional(key="encrypted",default="null")

    # revisit 3402870234
    # syntax to get working
    #stack.parse.add_optional(key="verify",choices=[ None, "True"],default="null")
    #stack.parse.add_optional(key="encrypted",choices=[ None, "True"],default="null")

    # add substacks
    stack.add_substack('elasticdev:::aws::verify_ami')
    stack.add_substack('elasticdev:::aws::make_public_ami')
    stack.add_substack('elasticdev:::aws::destroy_ami')
    stack.add_substack('elasticdev:::aws::copy_ami')

    # init the stack namespace
    stack.init_variables()
    stack.init_substacks()

    # You need to verify before you make it public or make an encrypted version
    if stack.config_env == "public" or stack.copy_regions or stack.encrypted or stack.verify:
        verify = True
    else:
        verify = None

    # create new name for the amis to referenced
    src_name = stack.get_random_string(size=12)

    # You need to determine the name of the image
    if stack.encrypted: 
        name = stack.get_random_string(size=12)
    else:
        name = src_name

    # Get server instance_id to image
    if not stack.instance_id:
        resource_info = stack.get_resource(name=stack.hostname,
                                           resource_type="server",
                                           must_exists=True)[0]

        stack.set_variable("instance_id",resource_info["instance_id"])

    # Creates and registers AMI from instance_id
    env_vars = {"INSTANCE_ID":stack.instance_id}
    env_vars["AWS_DEFAULT_REGION"] = stack.aws_default_region
    env_vars["LABEL"] = stack.label
    env_vars["METHOD"] = "create"
    env_vars["NAME"] = src_name
    if stack.config_env == "public": env_vars["PUBLIC"] = True

    ikwargs = {"insert_env_vars":stack.insert_env_vars}
    ikwargs["env_vars"] = json.dumps(env_vars)
    ikwargs["shelloutconfig"] = stack.shelloutconfig
    ikwargs["itype"] = "ami"
    ikwargs["name"] = src_name
    ikwargs["config_env"] = stack.config_env

    stack.register_image(order_type="register-ami::api",
                         human_description='Creates and records AMI',
                         display=None,
                         **ikwargs)

    # If you need an encrypted image, you need to verify the unencrypted image
    # before continuing.
    if verify:

        overide_values = {"name":src_name}
        overide_values["config_env"] = stack.config_env
        overide_values["aws_default_region"] = stack.aws_default_region

        inputargs = {"overide_values":overide_values}

        human_description = 'Verifying the ami image {}'.format(src_name)
        inputargs["automation_phase"] = "infrastructure"
        inputargs["human_description"] = human_description
        stack.verify_ami.insert(display=True,**inputargs)

    stack.set_parallel()

    # Creates encrypted image if needed
    if stack.encrypted:

        # make a copy with encrypted volume   
        default_values = {"src_name":src_name}
        default_values["name"] = name
        default_values["label"] = stack.label
        default_values["encrypted"] = True
        default_values["src_region"] = stack.aws_default_region
        default_values["dst_region"] = stack.aws_default_region
        default_values["config_env"] = stack.config_env
        if stack.verify: default_values["verify"] = True

        human_description = 'Encrypting the ami image {} to {}'.format(src_name,name)
        inputargs = {"default_values":default_values}
        inputargs["automation_phase"] = "infrastructure"
        inputargs["human_description"] = human_description
        stack.copy_ami.insert(display=True,**inputargs)

    # Makes the image public if needed
    if stack.config_env == "public":

        if stack.encrypted: 
            _name = name
        else:
            _name = src_name

        default_values = {"name":_name}
        default_values["aws_default_region"] = stack.aws_default_region
        default_values["config_env"] = stack.config_env

        human_description = 'Making the ami image {} public'.format(src_name)
        inputargs = {"default_values":default_values}
        inputargs["automation_phase"] = "infrastructure"
        inputargs["human_description"] = human_description
        stack.make_public_ami.insert(display=True,**inputargs)

    summary = {}
    summary[stack.aws_default_region] = name

    # Copy to other regions if required
    if stack.copy_regions:

        for copy_region in stack.copy_regions:
            copy_name = stack.get_random_string(size=12)
            summary[copy_region] = copy_name
            default_values = {"src_name":src_name}
            default_values["name"] = copy_name
            default_values["label"] = stack.label
            default_values["encrypted"] = stack.encrypted
            default_values["src_region"] = stack.aws_default_region
            default_values["dst_region"] = copy_region
            if stack.verify: default_values["verify"] = True

            human_description = 'Encrypting the ami image {} to {}'.format(src_name,copy_name)
            inputargs = {"default_values":default_values}
            inputargs["automation_phase"] = "infrastructure"
            inputargs["human_description"] = human_description
            stack.copy_ami.insert(display=True,**inputargs)

    stack.unset_parallel

    # Publish the summary
    stack.publish(summary)

    # wait for queue orders below to complete
    stack.wait_all()

    if stack.encrypted: 
        # destroy src unencrypted ami to protect
        # it from ever being distributed
        default_values = {"name":src_name}
        default_values["label"] = stack.label
        default_values["aws_default_region"] = stack.aws_default_region
        default_values["destroy"] = True
        stack.destroy_ami.insert(display=True,**inputargs)

    return stack.get_results()
