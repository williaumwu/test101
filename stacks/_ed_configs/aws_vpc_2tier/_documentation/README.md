**Description**
  - The stack that creates a secure VPC on AWS for 2 tier web application.

**Notable**
  -  Ports open to public include: 

```
"web" security group
  http: 80
  https: 443
  ssh: 22

"database" security group
  web security group
  bastion security group

"bastion" security group
  http: 80
  https: 443
  ssh: 22

vpc_name: <project_name>-vpc
```
