variable "vpc_name" {
    description = "vpc_name for the VPC"
    default = "sample_vpc_name"
}

variable "aws_region" {
    description = "EC2 Region for the VPC"
    default = "us-east-1"
}

variable "main_vpc_cidr" {
    description = "CIDR of the VPC"
    default = "10.0.0.0/16"
}
