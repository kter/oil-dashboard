data "aws_route53_zone" "main" {
  name         = var.hosted_zone_name
  private_zone = false
}

locals {
  hosted_zone_id = data.aws_route53_zone.main.zone_id
}
