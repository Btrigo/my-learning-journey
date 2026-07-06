variable "aws_region" {
  description = "AWS region where resources are deployed"
  type        = string
  default     = "us-east-1"
}

variable "github_org" {
  description = "GitHub organization or username that owns the repository"
  type        = string
}

variable "github_repo" {
  description = "Name of the GitHub repository allowed to assume the deploy role"
  type        = string
}

variable "github_branch" {
  description = "Branch permitted to assume the deploy role via OIDC"
  type        = string
  default     = "main"
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket the deploy role is permitted to sync to"
  type        = string
}

variable "iam_role_name" {
  description = "Name of the IAM role assumed by GitHub Actions via OIDC"
  type        = string
  default     = "github-actions-portfolio-deploy"
}

variable "iam_policy_name" {
  description = "Name of the inline IAM policy granting S3 deploy permissions"
  type        = string
  default     = "github-actions-portfolio-s3-deploy"
}