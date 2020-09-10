def run(stackargs):

    stackargs["add_cluster"] = False
    stackargs["add_instance"] = False

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="hostname")
    stack.parse.add_required(key="key")
    stack.parse.add_required(key="aws_default_region",default="us-east-1")
    stack.parse.add_required(key="region",default="null")
    stack.parse.add_required(key="image_ref",default="elasticdev:::public::ubuntu.16.04-chef_solo")

    # revisit 987302943adfffysdfsdfj
    # need to add user data script from s3 or something location or http location.
    #stack.parse.add_required(key="user_data_script",default="/opt/jiffy/Bootstraps/cloudinit/ubuntu.yaml")

    stack.parse.add_optional(key="user_data_script",default="null")
    stack.parse.add_optional(key="image",default="null")
    stack.parse.add_optional(key="image_name",default="null")
    stack.parse.add_optional(key="sg_label",default="null")
    stack.parse.add_optional(key="sg",default="null")
    stack.parse.add_optional(key="placement",default="null")
    stack.parse.add_optional(key="vpc",default="null")
    stack.parse.add_optional(key="tags",default="null")
    stack.parse.add_optional(key="comment",default="null")

    stack.parse.add_optional(key="size",default="t2.micro")
    stack.parse.add_optional(key="disksize",default=40)
    stack.parse.add_optional(key="timeout",default=600)
    stack.parse.add_optional(key="security_group",default="default")
    stack.parse.add_optional(key="vpc_label",default="vpc")

    # Initialize Variables in stack
    stack.init_variables()

    # Create Server
    cmd = "ec2 server create"
    order_type = "create-cloudserver::api"
    role = "cloud/ec2"

    default_values = {}
    default_values["hostname"] = stack.hostname

    if not stack.region: 
        stack.region = stack.aws_default_region
        stackargs["region"] = stack.aws_default_region

    default_values["region"] = stack.region
    default_values["key"] = stack.key

    default_values["size"] = stack.size
    default_values["disksize"] = stack.disksize
    default_values["timeout"] = stack.timeout
    default_values["security_group"] = stack.security_group
    default_values["vpc_label"] = stack.vpc_label

    # These are the None default
    default_values["tags"] = stack.tags
    default_values["comment"] = stack.comment
    default_values["placement"] = stack.placement
    default_values["vpc"] = stack.vpc
    default_values["sg_label"] = stack.sg_label
    default_values["sg"] = stack.sg
    default_values["image"] = stack.image
    default_values["user_data_script"] = stack.user_data_script

    long_description = "Makes the API call to create a Server on Ec2"
    human_description = "API Call: Create a Server on Ec2"

    input_args = stackargs.copy()

    #if image_ref, it will overide the image parameter above
    if stack.image_ref or stack.image_name and not stack.image:
        input_args["image"] = stack.get_image(image_ref=stack.image_ref,
                                              name=stack.image_name,
                                              itype="ami",
                                              ignore=True,
                                              region=stack.region)

        if not input_args.get("image"):
            msg = "Cannot determine the image_id/ami for ec2 server creation"
            stack.ehandle.NeedRtInput(message=msg)

    stack.insert_builtin_cmd(cmd,
                             order_type=order_type,
                             role=role,
                             human_description=human_description,
                             long_description=long_description,
                             display=True,
                             default_values=default_values,
                             jkwargs=input_args)

    return stack.get_results()
