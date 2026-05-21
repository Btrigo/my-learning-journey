output "cloudfront_url" {
  description = "CloudFront distribution domain name"
  value       = "https://${aws_cloudfront_distribution.portfolio.domain_name}"
}

output "s3_bucket_name" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.portfolio.id
}