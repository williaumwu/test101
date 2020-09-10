def run(stackargs):

    # initializes stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="vpc_name",default="null")
    stack.parse.add_required(key="vpc_label",default="vpc")
    stack.parse.add_required(key="vpc_peer",default="jiffy",null_allowed=True)
    stack.parse.add_required(key="sg_web_label",default="web")
    stack.parse.add_required(key="sg_bastion_label",default="bastion")
    stack.parse.add_required(key="sg_db_label",default="database")
    stack.parse.add_required(key="aws_default_region",default="us-east-1")
    stack.parse.add_required(key="region",default="null")

    # Initialize Variables in stack
    stack.init_variables()
  
    stack.set_variable("vpc","{}-{}".format(stack.cluster,stack.vpc_label))
    stack.set_variable("sg_web","{}-{}".format(stack.cluster,stack.sg_web_label))
    stack.set_variable("sg_bastion","{}-{}".format(stack.cluster,stack.sg_bastion_label))
    stack.set_variable("sg_db","{}-{}".format(stack.cluster,stack.sg_db_label))

    if stack.vpc_name:
        stack.set_variable("vpc",stack.vpc_name)
    else:
        stack.set_variable("vpc","{}-{}".format(stack.cluster,stack.vpc_label))

    if not stack.region: 
        stack.set_variable("region",stack.aws_default_region)

    #####################################
    stack.unset_parallel()
    #####################################

    # Creates VPC
    default_values = {}
    default_values["region"] = stack.region
    default_values["name"] = stack.vpc

    cmd = "ec2 vpc create"
    order_type = "create-cloudvpc::api"
    role = "cloud/ec2"
    human_description = "Creates VPC {}".format(stack.vpc)

    stack.insert_builtin_cmd(cmd,
                             order_type=order_type,
                             default_values=default_values,
                             human_description=human_description,
                             display=True,
                             role=role)

    # Creates Subnets
    labels = {}
    labels[stack.sg_db_label] = {"subnet_type":"public"}
    labels["bastion"] = {"subnet_type":"public"}
    labels["web"] = {"subnet_type":"public"}

    snets = []

    for lkey,lvalue in labels.iteritems():
        snets.append("%s:%s" % (lkey,lvalue["subnet_type"]))

    subnets = " ".join(snets)

    inputargs = { "subnets":subnets,
                  "add_cluster_name":True,
                  "add_instance_name":True }

    cli = stack.new_builtin_cmd("ec2 subnet batchadd")
    cli.order_type = "create-cloudsubnet::api"
    cli.role = "cloud/ec2"
    cli.required_keys = [ "subnets" ]
    cli.human_description = "Creates subnets for vpc"
    cli.long_description = "Creates subnets in batches on ec2 for vpc"
    cli.display = True
    cli.overide_kwargs = inputargs
    stack.add_builtin_cmd()

    #####################################
    stack.set_parallel()
    #####################################

    # Creates VPC Peer if necessary
    if stack.vpc_peer:
        cmd = "ec2 vpc peering"
        order_type = "peer-cloudvpc::api"
        role = "cloud/ec2"

        default_values = {"bidirectional":True}
        default_values["src_vpc"] = stack.vpc_peer
        if stack.vpc_label: default_values["dst_label"] = stack.vpc_label
        human_description = "Creates VPC peering"

        cli = stack.new_builtin_cmd(cmd)
        cli.order_type = order_type
        cli.role = role
        cli.default_values = default_values
        cli.human_description = human_description 
        cli.display = True
        stack.add_builtin_cmd()

    # Creates the security groups
    required_keys=[ "sg_label", "rules" ]

    base_args = { "add_cluster_name":True,
                  "add_instance_name":True }

    cmd = "ec2 security group create"
    order_type = "create-cloudsg::api"
    role = "cloud/ec2"

    # db security group
    inputargs = base_args.copy()
    inputargs["sg_label"] = stack.sg_db_label
    inputargs["rules"] = "elasticdev:::dev_repo::firewall/web \
                          elasticdev:::dev_repo::firewall/ssh_sgs \
                          elasticdev:::dev_repo::firewall/%s" % "database_2tier"

    human_description = "Creates security group = {}".format(stack.sg_db_label)
    long_description = "Creates security group with label={}".format(stack.sg_db_label)

    cli = stack.new_builtin_cmd(cmd)
    cli.order_type = order_type
    cli.role = role
    cli.human_description = human_description 
    cli.long_description = long_description 
    cli.display = True
    cli.required_keys = required_keys
    cli.overide_kwargs = inputargs
    stack.add_builtin_cmd()

    # bastion security group
    inputargs = base_args.copy()
    inputargs["sg_label"] = "bastion"
    inputargs["rules"] = "elasticdev:::dev_repo::firewall/web \
                          elasticdev:::dev_repo::firewall/bastion" 

    human_description = "Creates security group = {}".format("bastion")
    long_description = "Creates security group with label={}".format("bastion")

    cli = stack.new_builtin_cmd(cmd)
    cli.order_type = order_type
    cli.role = role
    cli.required_keys = required_keys
    cli.human_description = human_description 
    cli.long_description = long_description 
    cli.display = True
    cli.overide_kwargs = inputargs
    stack.add_builtin_cmd()

    # web security group
    inputargs = base_args.copy()
    inputargs["sg_label"] = "web"
    inputargs["rules"] = "elasticdev:::dev_repo::firewall/web_public \
                          elasticdev:::dev_repo::firewall/web_secure_public \
                          elasticdev:::dev_repo::firewall/ssh_sgs \
                          elasticdev:::dev_repo::firewall/ssh_local_10 \
                          elasticdev:::dev_repo::firewall/ssh_local_172 \
                          elasticdev:::dev_repo::firewall/ssh/public/default \
                          elasticdev:::dev_repo::firewall/ssh/public/dockerguest \
                          elasticdev:::dev_repo::firewall/http/public/dockerguest" 

    human_description = "Creates security group = {}".format("web")
    long_description = "Creates security group with label={}".format("web")

    cli = stack.new_builtin_cmd(cmd)
    cli.order_type = order_type
    cli.role = role
    cli.required_keys = required_keys
    cli.human_description = human_description 
    cli.long_description = long_description 
    cli.display = True
    cli.overide_kwargs = inputargs
    stack.add_builtin_cmd()

    #####################################
    stack.unset_parallel()
    #####################################

    # wait for queue orders below to complete
    stack.wait_all()

    # activate security group
    cmd = "ec2 security group activate"
    order_type = "activate-cloudsg::api"
    role = "cloud/ec2"
    human_description = "Activates the security groups"

    stack.insert_builtin_cmd(cmd,
                             order_type=order_type,
                             human_description=human_description,
                             display=True,
                             role=role)

    stack.set_parallel()

    # Publish the variables
    values = {}
    values["vpc"] = stack.vpc
    values["vpc_peer"] = stack.vpc_peer
    values["sg_web"] = stack.sg_web
    values["sg_bastion"] = stack.sg_bastion
    values["sg_db"] = stack.sg_db
    stack.publish(values)

    # Pass on additional variables as part of the 
    # infrastructure base
    values["sg_web"] = stack.sg_web
    values["sg_bastion"] = stack.sg_bastion
    values["sg_db"] = stack.sg_db
    values["sg_db_label"] = stack.sg_db_label
    values["sg_web_label"] = stack.sg_web_label
    values["sg_bastion_label"] = stack.sg_bastion_label
    values["vpc_name"] = stack.vpc
    values["vpc"] = stack.vpc
    stack.add_stack_args_to_run(values,mkey="infrastructure")

    # Return results
    return stack.get_results()
