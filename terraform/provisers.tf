terraform {
    required_version = "~> 1.6.3"
    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = ">= 5.23.1"
        }
    }
}

provider "aws" {
    region = "us-east-1"
    # profile = "default"
    profile = "localstack"
}