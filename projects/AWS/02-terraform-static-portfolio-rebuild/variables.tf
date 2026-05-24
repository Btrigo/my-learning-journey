# Input variables for the static portfolio structure

variable "aws_region" {
    description = "AWS region to deploy resources into"
    type = string
    default = "us-east-1"
}

variable "bucket_name" {
    description = "online-portfolio-terraform"
    type = string
    default = "brandon-portfolio-site-02-tf"
}