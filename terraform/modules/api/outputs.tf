output "ecr_repository_url" {
  value = aws_ecr_repository.api.repository_url
}

output "lambda_function_name" {
  value = aws_lambda_function.api.function_name
}

output "api_gateway_url" {
  value = "https://${var.api_domain}"
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.reserves.name
}
