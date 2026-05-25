# Output values printed after terraform apply

output "cloudfront_domain_name" {
  description = "The CloudFront distribution domain name — use this URL to access the site"
  value       = aws_cloudfront_distribution.portfolio.domain_name
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket"
  value       = aws_s3_bucket.portfolio.bucket
}