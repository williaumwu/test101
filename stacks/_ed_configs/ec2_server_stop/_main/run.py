def run(stackargs):

    stack = newStack(stackargs)

    stack.parse.add_required(key="hostname")

    # init the stack namespace
    stack.init_variables()

    # Check resource
    stack.get_resource(name=stack.hostname,
                       resource_type="server",
                       provider="ec2",
                       must_exists=True)

    # Stop the server when done to save money
    stack.modify_resource(resource_type="server",
                          human_description='Stopping resource server hostname "{}"'.format(stack.hostname),
                          provider="ec2",
                          name=stack.hostname,
                          method="stop")
    
    return stack.get_results(zero_orders=True)
