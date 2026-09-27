# Remote state with DynamoDB locking.
# Commented out because the S3 bucket and DynamoDB table must exist
# before `terraform init` can use them — a bootstrap ordering problem.
# See bootstrap/ for the one-time setup that creates them.
#
# terraform {
#   backend "s3" {
#     bucket         = "meditrack-tfstate-shreyash"
#     key            = "eks/terraform.tfstate"
#     region         = "ap-south-1"
#     dynamodb_table = "meditrack-tfstate-lock"
#     encrypt        = true
#   }
# }
