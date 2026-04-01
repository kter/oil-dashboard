variable "env" {
  type = string
}

variable "aws_region" {
  type    = string
  default = "ap-northeast-1"
}

variable "frontend_domain" {
  type = string
}

variable "api_domain" {
  type = string
}

variable "hosted_zone_id" {
  type = string
}
