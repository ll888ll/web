variable "aws_region" {
  description = "AWS region where resources will be created."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Tag/name prefix for all resources."
  type        = string
  default     = "croody"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.50.0.0/16"
}

variable "public_subnets" {
  description = "List of public subnets (for ALB/NAT/Bastion)."
  type = list(object({
    cidr = string
    az   = string
  }))
  default = [
    { cidr = "10.50.10.0/24", az = "us-east-1a" },
    { cidr = "10.50.20.0/24", az = "us-east-1b" }
  ]
}

variable "private_subnets" {
  description = "List of private subnets (for app/db)."
  type = list(object({
    cidr = string
    az   = string
  }))
  default = [
    { cidr = "10.50.110.0/24", az = "us-east-1a" },
    { cidr = "10.50.210.0/24", az = "us-east-1b" }
  ]
}

variable "allowed_ssh_cidrs" {
  description = "CIDR ranges allowed to SSH to the bastion."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "bastion_instance_type" {
  description = "Instance type for the bastion host."
  type        = string
  default     = "t3.micro"
}

variable "bastion_key_pair" {
  description = "Existing EC2 key pair name for the bastion host."
  type        = string
  default     = ""
}

variable "tags" {
  description = "Extra tags applied to resources."
  type        = map(string)
  default     = {}
}
