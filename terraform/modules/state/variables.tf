variable "env" {
  type        = string
  description = "Environment name (dev or prd)"
}

variable "aws_profile" {
  type        = string
  description = "AWS CLI profile name"
  default     = "dev"
}
