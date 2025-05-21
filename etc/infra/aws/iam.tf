resource "aws_iam_role" "iam_role_lambda" {
  name               = local.resource_name
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_policy" "lambda_cloudwatch" {
  name   = local.resource_name
  policy = data.aws_iam_policy_document.cloud_watch_role.json
}

resource "aws_iam_role_policy_attachment" "lambda_cloudwatch" {
  role       = aws_iam_role.iam_role_lambda.name
  policy_arn = aws_iam_policy.lambda_cloudwatch.arn
}

resource "aws_iam_policy" "lambda_secrets" {
  name   = "${var.environment}-${var.app_name}-lambda-additional"
  policy = data.aws_iam_policy_document.lambda_secrets.json
}

resource "aws_iam_role_policy_attachment" "lambda_secrets" {
  role       = aws_iam_role.iam_role_lambda.name
  policy_arn = aws_iam_policy.lambda_secrets.arn
}
