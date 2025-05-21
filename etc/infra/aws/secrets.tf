resource "aws_secretsmanager_secret" "lambda_secret" {
  name = local.secret_name
}

resource "aws_secretsmanager_secret_version" "lambda_secret_version" {
  secret_id     = aws_secretsmanager_secret.lambda_secret.id
  secret_string = "{}"
  lifecycle {
    ignore_changes = [
      secret_string,
    ]
  }
}
