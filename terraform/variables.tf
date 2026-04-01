variable "env" {
  type        = string
  description = "Environment name (dev or prd)"
}

variable "aws_profile" {
  type        = string
  description = "AWS CLI profile name"
}

variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "ap-northeast-1"
}

variable "frontend_domain" {
  type        = string
  description = "Frontend CloudFront domain"
}

variable "api_domain" {
  type        = string
  description = "API Gateway custom domain"
}

variable "hosted_zone_name" {
  type        = string
  description = "Route53 hosted zone name"
}
