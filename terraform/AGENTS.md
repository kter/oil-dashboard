# Terraform - Agent Instructions

## Commands

All Terraform workflows via root Makefile:

```bash
make tf-init ENV=dev    # Init with backend config
make tf-plan ENV=dev    # Plan changes
make tf-apply ENV=dev   # Apply changes
make tf-fmt             # Format HCL files
make tf-validate        # Validate configuration
```

## Conventions

- Use Terraform workspaces for environment separation (dev, prd)
- Backend configs in `terraform/backends/{env}.s3.tfbackend`
- Environment-specific vars in `terraform/envs/{env}.tfvars`
- AWS profiles match environment names: `dev`, `prd`
- Modules: `state/` (TF backend), `cdn/` (CloudFront+S3), `api/` (Lambda+APIGW+DynamoDB), `dns/` (Route53)
- Existing hosted zones: `dev.devtools.site` (dev account), `devtools.site` (prd account)
