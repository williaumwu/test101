variable "vpc_name" {
    description = "vpc_name for the VPC"
    default = "sample_vpc_name"
}

variable "aws_region" {
    description = "EC2 Region for the VPC"
    default = "us-east-1"
}

variable "availability_zones" {
    description = "Avaialbility Zones"
    type = "list"
    default = [ "us-east-1a", "us-east-1b" ]
}

variable "main_vpc_cidr" {
    description = "CIDR of the VPC"
    default = "10.0.0.0/16"
}

variable "cidr_subnet1" {
    description = "cidr_subnet1"
    default = "10.0.1.0/24"
}

variable "cidr_subnet2" {
    description = "cidr_subnet2"
    default = "10.0.2.0/24"
}

variable "cidr_subnet3" {
    description = "cidr_subnet3"
    default = "10.0.3.0/24"
}

variable "cidr_subnet4" {
    description = "cidr_subnet4"
    default = "10.0.4.0/24"
}

variable "cidr_subnet5" {
    description = "cidr_subnet5"
    default = "10.0.5.0/24"
}

variable "cidr_subnet6" {
    description = "cidr_subnet6"
    default = "10.0.6.0/24"
}

variable "cidr_subnet7" {
    description = "cidr_subnet7"
    default = "10.0.7.0/24"
}

variable "cidr_subnet8" {
    description = "cidr_subnet8"
    default = "10.0.8.0/24"
}
