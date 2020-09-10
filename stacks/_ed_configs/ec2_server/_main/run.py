def _determine_region(stack,stackargs):

    stack.region = stack.aws_default_region
    stackargs["region"] = stack.aws_default_region

def _determine_image(stack,stackargs):

    if stack.image: return

    # Determine the image
    if stack.image_ref or stack.image_name:
        stack.image = stack.get_image(image_ref=stack.image_ref,
                                      name=stack.image_name,
                                      itype="ami",
                                      ignore=True,
                                      region=stack.region)

        if not stack.image:
            msg = "Cannot determine the image_id/ami for ec2 server creation"
            stack.ehandle.NeedRtInput(message=msg)

        stackargs["image"] = stack.image

def _determine_vpc_sg(stack,stackargs):

    # Determine vpc and security by assuming it is automatically
    # a combination of cluster and label

    if not stack.vpc and stack.vpc_label: 
        stack.vpc = "{}_{}".format(stack.cluster,stack.vpc_label)
        stackargs["vpc"] = stack.vpc

    if not stack.security_group and stack.security_group_label: 
        stack.security_group = "{}_{}".format(stack.cluster,stack.security_group_label)
        stackargs["security_group"] = stack.security_group

def _determine_subnet_id(stack,stackargs):

    import random

    if not stack.subnet_id: return

    # We need a vpc reference to get the subnet_id
    if not stack.vpc_id and not stack.vpc_label: return

    # Get the subnets if vpc_id or vpc is determined
    resource_lookup = {"must_exists":None}
    resource_lookup["resource_type"] = "subnet"
    resource_lookup["provider"] = "ec2"

    if stack.vpc_id:
        resource_lookup["vpc_id"] = stack.vpc_id
    else:
        resource_lookup["vpc"] = stack.vpc

    _resources = list(stack.get_resource(**resource_lookup))
    if not _resources: return 

    stack.subnet_id = random.randrange(len([ resource["id"] for resource in _resources ])) - 1
    stackargs["subnet_id"] = stack.subnet_id

def _determine_sg_id(stack,stackargs):

    if stack.security_group_id: return

    # Need both subnet_id and sg label to get the sg_id
    if not stack.subnet_id: return
    if not stack.security_group_label: return
    if not stack.security_group: return

    resource_lookup = {"must_exists":True}
    resource_lookup["resource_type"] = "security_group"
    resource_lookup["provider"] = "ec2"
    resource_lookup["name"] = stack.security_group

    # If subnet is found, there must be a vpc_id or vpc
    if stack.vpc_id:
        resource_lookup["vpc_id"] = stack.vpc_id
    else:
        resource_lookup["vpc"] = stack.vpc

    stack.security_group_id = stack.get_resource(**resource_lookup)[0]["id"]
    stackargs["security_group_id"] = stack.security_group_id

def run(stackargs):

    import json

    stackargs["add_cluster"] = False
    stackargs["add_instance"] = False

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="hostname")
    stack.parse.add_required(key="key")
    stack.parse.add_required(key="aws_default_region",default="us-east-1")
    stack.parse.add_required(key="image_ref",default="elasticdev:::public::ubuntu.16.04-chef_solo")
    stack.parse.add_required(key="insert_env_vars",default='["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]')

    # revisit 987302943adfffysdfsdfj
    # need to add user data script from s3 or something location or http location.
    #stack.parse.add_required(key="user_data_script",default="/opt/jiffy/Bootstraps/cloudinit/ubuntu.yaml")
    #stack.parse.add_optional(key="user_data_script",default="null")
    stack.parse.add_optional(key="image",default="null")
    stack.parse.add_optional(key="image_name",default="null")
    stack.parse.add_optional(key="tags",default="null")
    stack.parse.add_optional(key="size",default="t2.micro")
    stack.parse.add_optional(key="disksize",default=40)

    # For determining vpc and subnet
    stack.parse.add_optional(key="vpc_label",default="null")
    stack.parse.add_optional(key="vpc_id",default="null")
    stack.parse.add_optional(key="vpc",default="null")

    stack.parse.add_optional(key="subnet_id",default="null")

    # For determining security group
    stack.parse.add_optional(key="security_group_label",default="null")
    stack.parse.add_optional(key="security_group_id",default="null")
    stack.parse.add_optional(key="security_group",default="default")

    # Add shelloutconfig dependencies
    stack.add_shelloutconfig('elasticdev:::aws::ec2_server',"ec2_server")

    # Initialize Variables in stack
    stack.init_variables()
    stack.init_substacks()
    stack.init_shelloutconfigs()
   
    # Determine the region
    _determine_region(stack,stackargs)

    # Determine the image
    _determine_image(stack,stackargs)

    # Determine vpc/security_group 
    _determine_vpc_sg(stack,stackargs)

    # Determine subnet
    _determine_subnet_id(stack,stackargs)

    # Determine security_group
    _determine_sg_id(stack,stackargs)

    # Call to create the server with shellout script
    stack.env_vars = {"INSERT_IF_EXISTS":True}
    stack.env_vars["AWS_DEFAULT_REGION"] = stack.aws_default_region
    stack.env_vars["HOSTNAME"] = stack.hostname
    stack.env_vars["NAME"] = stack.hostname
    stack.env_vars["METHOD"] = "create"
    stack.env_vars["KEY"] = stack.key
    stack.env_vars["INSTANCE_TYPE"] = stack.size
    stack.env_vars["DISKSIZE"] = stack.disksize
    stack.env_vars["AMI"] = stack.image

    if stack.subnet_id: stack.env_vars["SUBNET_ID"] = stack.subnet_id
    if stack.security_group_id: stack.env_vars["SECURITY_GROUPS_IDS"] = stack.security_group_id
    if stack.tags: stack.env_vars["TAGS"] = stack.tags

    if hasattr(stack, "job_instance_id") and stack.job_instance_id: stack.env_vars["JOB_INSTANCE_ID"] = stack.job_instance_id
    if hasattr(stack, "schedule_id") and stack.schedule_id: stack.env_vars["SCHEDULE_ID"] = stack.schedule_id

    inputargs = {"display":True}
    inputargs["human_description"] = 'API Call: Create a Server on Ec2 hostname "{}"'.format(stack.hostname)
    inputargs["insert_env_vars"] = stack.insert_env_vars
    inputargs["env_vars"] = json.dumps(stack.env_vars)
    inputargs["automation_phase"] = "infrastructure"
    inputargs["retries"] = 2
    inputargs["timeout"] = 60
    inputargs["wait_last_run"] = 2
    stack.ec2_server.resource_exec(**inputargs)

    return stack.get_results()
