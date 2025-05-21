## Deployment Steps for nimara-stripe from Local to AWS

### Requirements
* [AWS-VAULT](https://github.com/99designs/aws-vault)
* AWS Account

### Pre-conditions
1. Copy `terraform.tfvars.example` to `terraform.tfvars` and fill in the required variables. \
Most variables will be common, but \
`environment` should be added with caution to avoid overwriting existing environments and their `tfstate` files. \
`provider_bucket_name` is the name of the S3 bucket that will store shared `tfstate` files. (previously created manually)

```terraform
aws_region              = "eu-central-1"
environment             = "" # A unique name to avoid overwriting existing environments
lambda_tag              = "0.9.8" # Should match the version of the app
app_name                = "nimara-stripe"
runtime                 = "python3.12"
arch                    = "arm64"
handler                 = "nimara_stripe.app.http_handler"
provider_bucket_name    = "" # A shared bucket with tfstate files
timeout                 = 10
allowed_domain_patterns = "\\.saleor\\.cloud$"
```

For example:
```terraform
environment          = "my-username-local" # Needed to create tfstate file in the bucket
app_name             = "my-application-name"
provider_bucket_name = "my-shared-bucket"
```
This will create a `tfstate` file in the bucket `my-shared-bucket` with the name `my-username-local-my-application-name.tfstate`.

### Deployment Steps
1. Run `make all` to build the app artifacts (the Lambda package and layers).
2. Initialize the Terraform configuration:
   ```sh
   aws-vault exec <your-profile> -- make init
   ```
3. Preview the changes:
   ```sh
   aws-vault exec <your-profile> -- make plan
   ```
4. Apply the changes:
   ```sh
   aws-vault exec <your-profile> -- make apply
   ```
5. Destroy the resources:
   ```sh
   aws-vault exec <your-profile> -- make destroy
   ```

> **Note**: \
> You may use `aws-vault exec <your-profile> --no-session` to avoid session expiration and then run: \
> `make init` \
> `make plan` \
> `make apply` \
> `make destroy`

### Common Issues
1. Double-check that you build your app artifacts for the correct architecture (check `uv` Python version).
2. If you finished working with the app, run `make destroy` to clean up the resources.
