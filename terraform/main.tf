module "cdn" {
  source = "./modules/cdn"

  env             = var.env
  frontend_domain = var.frontend_domain
  hosted_zone_id  = local.hosted_zone_id

  providers = {
    aws           = aws
    aws.us_east_1 = aws.us_east_1
  }
}

module "api" {
  source = "./modules/api"

  env             = var.env
  aws_region      = var.aws_region
  frontend_domain = var.frontend_domain
  api_domain      = var.api_domain
  hosted_zone_id  = local.hosted_zone_id
}
