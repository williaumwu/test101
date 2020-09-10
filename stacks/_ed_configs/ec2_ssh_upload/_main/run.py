def run(stackargs):

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="name")
    stack.parse.add_required(key="region",default="null")

    # Initialize Variables in stack
    stack.init_variables()

    # Create key
    cmd = "ssh_key create"
    order_type = "create-ssh_key::api"
    role = "cloud/ec2"

    default_values = {"name":stack.name}
    human_description = "Generate new ssh_key {} if it does not exists".format(stack.name)

    stack.insert_builtin_cmd(cmd,
                             order_type=order_type,
                             role=role,
                             human_description=human_description,
                             display=True,
                             default_values=default_values)

    # Delete key just in case it already exists
    cmd = "ec2 ssh_key delete"
    order_type = "delete-ssh_key::api"
    role = "cloud/ec2"

    default_values = {"name":stack.name}
    default_values["region"] = stack.region
    default_values["without_resource_table"] = True
    human_description = "Delete ssh_key {} to ec2 at {} forcibly".format(stack.name,stack.region)

    stack.insert_builtin_cmd(cmd,
                             order_type=order_type,
                             role=role,
                             human_description=human_description,
                             display=True,
                             default_values=default_values)

    # Clean up key deletion
    cmd = "ec2 ssh_key delete"
    order_type = "delete-ssh_key::api"
    role = "cloud/ec2"

    default_values = {"name":stack.name}
    default_values["region"] = stack.region
    human_description = "Cleanup deletion of ssh_key {} to ec2 at {}".format(stack.name,stack.region)

    stack.insert_builtin_cmd(cmd,
                             order_type=order_type,
                             role=role,
                             human_description=human_description,
                             display=True,
                             default_values=default_values)

    # Upload key
    cmd = "ec2 ssh_key upload"
    order_type = "upload-ssh_key::api"
    role = "cloud/ec2"

    default_values = {"name":stack.name}
    default_values["region"] = stack.region
    human_description = "Upload ssh_key {} to ec2 at {}".format(stack.name,stack.region)

    stack.insert_builtin_cmd(cmd,
                             order_type=order_type,
                             role=role,
                             human_description=human_description,
                             display=True,
                             default_values=default_values)

    return stack.get_results()
