output "frontend_url" {
  value = "https://${var.frontend_domain}"
}

output "api_url" {
  value = module.api.api_gateway_url
}

output "s3_bucket_name" {
  value = module.cdn.s3_bucket_name
}

output "cloudfront_distribution_id" {
  value = module.cdn.cloudfront_distribution_id
}

output "ecr_repository_url" {
  value = module.api.ecr_repository_url
}

output "lambda_function_name" {
  value = module.api.lambda_function_name
}

output "dynamodb_table_name" {
  value = module.api.dynamodb_table_name
}
