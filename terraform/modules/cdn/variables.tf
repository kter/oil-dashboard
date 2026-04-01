variable "env" {
  type = string
}

variable "frontend_domain" {
  type = string
}

variable "hosted_zone_id" {
  type = string
}

terraform {
  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = "~> 5.0"
      configuration_aliases = [aws.us_east_1]
    }
  }
}
