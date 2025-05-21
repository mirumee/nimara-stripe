resource "aws_lambda_layer_version" "lambda_layer_version" {
  layer_name               = "${local.resource_name}-main"
  filename                 = local.layer_zip_file
  source_code_hash         = filebase64sha256(local.layer_zip_file)
  compatible_runtimes      = [var.runtime]
  compatible_architectures = [var.arch]
}
