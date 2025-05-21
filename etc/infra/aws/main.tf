resource "aws_lambda_function" "aws_lambda" {
  function_name    = local.resource_name
  role             = aws_iam_role.iam_role_lambda.arn
  filename         = local.lambda_zip_file
  source_code_hash = filebase64sha256(local.lambda_zip_file)
  runtime          = var.runtime
  handler          = var.handler
  memory_size      = var.memory_size
  timeout          = var.timeout
  architectures    = [var.arch]
  layers           = [aws_lambda_layer_version.lambda_layer_version.arn]

  environment {
    variables = local.env_vars
  }

  depends_on = [
    aws_iam_role.iam_role_lambda,
    aws_cloudwatch_log_group.lambda_cloud_watch_group,
  ]
}

resource "aws_cloudwatch_log_group" "lambda_cloud_watch_group" {
  name              = "/aws/lambda/${local.resource_name}"
  retention_in_days = var.log_retention
}

resource "aws_lambda_function_url" "lambda_function_url" {
  function_name      = aws_lambda_function.aws_lambda.function_name
  authorization_type = "NONE"
}

resource "aws_lambda_permission" "lambda_url_permission" {
  statement_id           = "AllowPublicInvokeURL"
  action                 = "lambda:InvokeFunctionUrl"
  function_name          = aws_lambda_function.aws_lambda.function_name
  principal              = "*"
  function_url_auth_type = "NONE"
}

output "lambda_function_url" {
  value = aws_lambda_function_url.lambda_function_url.function_url
}
