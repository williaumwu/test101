def run(stackargs):

    #from time import sleep
    import json

    # instantiate stack
    stack = newStack(stackargs)

    # add variables
    stack.parse.add_required(key="name")
    stack.parse.add_required(key="config_env",choices=["private", "public"],default="private")
    stack.parse.add_optional(key="region",default="us-east-1")
    stack.parse.add_optional(key="label",default="null")
    stack.parse.add_optional(key="destroy",default=True)

    # init the stack namespace
    stack.init_variables()

    ikwargs = {"name":stack.name}
    ikwargs["itype"] = "ami"
    ikwargs["config_env"] = stack.config_env
    ikwargs["region"] = stack.region
    if stack.label: ikwargs["label"] = stack.label

    stack.deregister_image(order_type="deregister-ami::api",
                           human_description='Deregisters the ami',
                           display=True,
                           **ikwargs)

    return stack.get_results()
