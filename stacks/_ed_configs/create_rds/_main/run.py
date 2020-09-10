def run(stackargs):

    # instantiate stack
    stack = newStack(stackargs)

    # add variables
    stack.parse.add_required(key="db_root_user",default="null")
    stack.parse.add_required(key="db_root_password",default="null")
    stack.parse.add_required(key="engine",default="MySQL")
    stack.parse.add_required(key="az",default="null")
    stack.parse.add_required(key="size",default=5)
    stack.parse.add_required(key="flavor",default="db.t2.micro")
    stack.parse.add_required(key="name",default="null")
    stack.parse.add_required(key="vpc_name",default="null")

    stack.parse.add_optional(key="vpc_label",default="vpc")
    stack.parse.add_optional(key="aws_default_region",default="us-east-1")

    stack.add_substack('elasticdev:::aws::publish_rds_info')

    # init the stack namespace
    stack.init_variables()
    stack.init_substacks()

    stack.set_variable("region",stack.aws_default_region)

    if not stack.db_root_user: 
        stack.set_variable("db_root_user",stack.get_random_string())

    if not stack.db_root_password: 
        stack.set_variable("db_root_password",stack.get_random_string())

    if not stack.name: 
        _suffix = stack.get_hash_string("{}".format(stack.cluster))[0:5]
        name = "{}-{}".format(stack.engine,_suffix).lower()
        stack.set_variable("name",name)

    if stack.vpc_name:
        stack.set_variable("vpc",stack.vpc_name)
    else:
        stack.set_variable("vpc","{}-{}".format(stack.cluster,stack.vpc_label))

    # sleep 1 to set parallel
    cmd = "sleep {0}".format(1)
    stack.add_external_cmd(cmd=cmd,
                           order_type="sleep::shellout",
                           human_description="sleep 1 second",
                           display=True,
                           role="external/cli/execute")

    # Create database with built-in
    pargs = "ec2 rds create"
    order_type = "create-rds::api"
    role = "cloud/database"
    human_description = "Creates RDS {}".format(stack.name)

    default_values = {"name":stack.name}
    default_values["size"] = stack.size
    default_values["flavor"] = stack.flavor
    default_values["engine"] = stack.engine
    default_values["region"] = stack.region
    default_values["user"] = stack.db_root_user
    default_values["password"] = stack.db_root_password
    default_values["vpc"] = stack.vpc
    if stack.az: default_values["az"] = stack.az

    stack.insert_builtin_cmd(pargs,
                             order_type=order_type,
                             default_values=default_values,
                             human_description=human_description,
                             display=True,
                             role=role)

    ## Insert variables into pipeline run
    #data = {"db_instance_name":stack.name}
    #data["db_root_user"] = stack.db_root_user
    #data["db_root_password"] = stack.db_root_password
    #data["engine"] = stack.engine

    #stack.add_stack_env_vars_to_run(data,**stackargs)
    #stack.publish(data,**stackargs)

    overide_values = {"db_instance_name":stack.name}
    overide_values["db_root_user"] = stack.db_root_user
    overide_values["db_root_password"] = stack.db_root_password
    overide_values["engine"] = stack.engine

    inputargs = {"overide_values":overide_values}
    inputargs["automation_phase"] = "infrastructure"
    inputargs["human_description"] = 'Publish info for RDS"{}"'.format(stack.name)
    stack.publish_rds_info.insert(display=True,**inputargs)

    return stack.get_results()

## Move over to shellouts below
#{
#    "az": null, 
#    "caller": "cli", 
#    "cluster": "zozo", 
#    "engine": "MySQL", 
#    "flavor": "db.t2.micro", 
#    "instance": "rds_mysql", 
#    "job_id": null, 
#    "job_instance_id": null, 
#    "name": "yo3", 
#    "password": "POJJBFTTBNDGCIBA", 
#    "region": "us-west-2", 
#    "ronly": false, 
#    "run_id": null, 
#    "schedule_id": null, 
#    "security_group": null, 
#    "sg": "zozo-database", 
#    "sg_ids": [
#        "sg-072c1f426c99fa691"
#    ], 
#    "sg_label": "database", 
#    "size": "5", 
#    "subnet_group_name": "yo3", 
#    "subnet_ids": [
#        "subnet-0457c82e0150ec5ee", 
#        "subnet-050c4ecb3d4f9ab47", 
#        "subnet-0ae12b1934deee6fc", 
#        "subnet-0cdba22a4ca93188c"
#    ], 
#    "tags": null, 
#    "user": "BLJNLGUXPIZXRVLI", 
#    "vpc": "zozo-vpc", 
#    "vpc_label": "vpc", 
#    "zone": null
#}
#
## Get vpc
#kwargs,vpc_exists = self.resource_info.get_name("vpc","vpc_label",
#                                                 input_args=kwargs,
#                                                 resource_type="vpc")
#
## Get security_groups
## Get sg_ids
#kwargs,sg_exists = self.resource_info.get_name("sg","sg_label",
#                                               input_args=kwargs,
#                                               resource_type="security_group")
#
#sg_ids = self.resource_info.get_sg_ids(kwargs,label=kwargs["sg_label"])
#if sg_ids: kwargs["sg_ids"] = sg_ids
#
#if not kwargs.get("sg_ids") and not kwargs.get("security_group"):
#    kwargs["security_groups"] = "default"
#
#def get_sg_ids(self,input_args,label=None):
#
#    sg_ids = None
#    match = {}
#    match["vpc"] = input_args["vpc"]
#    match["resource_type"] = "security_group"
#    if label: match["label"] = label
#
#    sgs = list(self.db.search(self.collection,match))
#    self.logger.debug("sgs: \n\n%s\n" % sgs)
#    if sgs: sg_ids = [ sg["id"] for sg in sgs ]
#
#    return sg_ids
#
## Get subnets
#subnet_ids = self.resource_info.get_subnets_ids(kwargs,label=kwargs["sg_label"])
#if subnet_ids: kwargs["subnet_ids"] = subnet_ids
#
## Create subnet for db
#def create_subnet(self,**kwargs):
#
#    '''
#    create db subnet which is needed for amazon
#    '''
#
#    query = None
#
#    db_subnet_args = {}
#    db_subnet_args["name"] = kwargs["name"]
#    db_subnet_args["subnet_ids"] = kwargs["subnet_ids"]
#
#    region = kwargs.get("region")
#    if not region: region = self.provider_instance.default_region
#    db_subnet_args["region"] = region
#
#    sstatus = self.provider_instance.add_subnet(**db_subnet_args)
#
#    if sstatus:
#        #Enter into DB
#        svalues = self._subnet_hash(db_subnet_args)
#        query = self.resource_info.append_resource_add(svalues,kwargs)
#
#    return query
#
#subnet_group_name = self.get_resource_subnet_name(**kwargs)
#
##If db_subnet not found, we create one
#if not subnet_group_name: subnet_group_name = self.get_subnet(**kwargs)[0]["name"]
#
#if not subnet_group_name:
#msg = "Cannot create/retrieve subnet for cloud database"
#self.ehandle.CloudNoSubnet(message=msg)
#
#kwargs["subnet_group_name"] = subnet_group_name
#
