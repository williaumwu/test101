**Description**
  - The stack that creates a VPC on AWS for 2 tier web application with some "dev" ports open.

**Notable**
  -  Ports open to public include: 

```
"web" security group
  http: 80
  https: 443
  ssh: 22
  alternative http: 8090-9010 
  alternative ssh: 22000-22500

"database" security group
  web security group
  bastion security group

"bastion" security group
  http: 80
  https: 443
  ssh: 22

vpc_name: <project_name>-vpc
```
