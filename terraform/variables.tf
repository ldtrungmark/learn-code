variable "vpc_cidr" {
  type    = string
  default = "172.31.0.0/16"
}

variable "public_subnet_cidrs" {
  type    = list(string)
  default = ["172.31.0.0/24", "172.31.1.0/24", "172.31.2.0/24"]
}

variable "private_subnet_cidrs" {
  type    = list(string)
  default = ["172.31.3.0/24", "172.31.4.0/24", "172.31.5.0/24"]
}

variable "azs" {
  type        = list(string)
  description = "Availability Zones"

  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "instance_type" {
  type = string
  description = "Instance type of the EC2"

  validation {
    condition = contains(["t2.micro", "t3.small"], var.instance_type)
    error_message = "Value not allow."
  }
}

variable "public_key" {
  type = string
  description = "SSH Key from local"
}