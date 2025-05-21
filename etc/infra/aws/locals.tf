locals {
  resource_name = "${var.app_name}-${var.environment}"
  secret_name   = "${var.environment}-${var.app_name}-secret"
  env_vars = {
    ENVIRONMENT            = var.environment,
    DEBUG                  = "False",
    SECRET_APP_CONFIG_PATH = local.secret_name
    ALLOWED_DOMAIN_PATTERN = var.allowed_domain_patterns
  }
  lambda_dist_path = "${path.module}/../../../dist/lambda"
  lambda_zip_file  = "${local.lambda_dist_path}/${var.app_name}-${var.lambda_tag}.zip"
  layer_zip_file   = "${local.lambda_dist_path}/${var.app_name}-requirements-layer-${var.lambda_tag}.zip"
}
