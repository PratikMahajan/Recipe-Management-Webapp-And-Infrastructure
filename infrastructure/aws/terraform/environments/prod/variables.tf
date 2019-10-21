# Configuration for VPC
variable "aws_region" {}
variable "subnet1_az" {}
variable "subnet1_name" {}
variable "subnet1_cidr" {}
variable "subnet2_az" {}
variable "subnet2_cidr" {}
variable "subnet2_name" {}
variable "subnet3_cidr" {}
variable "subnet3_az" {}
variable "subnet3_name" {}
variable "vpc_cidr" {}
variable "vpc_name" {}


# Configuration for s3 bucket creation
variable "s3_bucket_name" {}

# Configuring database
variable "database_engine_version" {}
variable "db_identifier" {}
variable "allocated_storage" {}
variable "storage_type" {}
variable "database_engine" {}
variable "instance_class" {}
variable "db_name" {}
variable "db_username" {}
variable "db_password" {}
variable "publicly_accessible" {}