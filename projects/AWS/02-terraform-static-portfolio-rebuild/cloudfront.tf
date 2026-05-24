# origin access control - grant cloudfront permission to access the private s3 bucket 
resource "aws_cloudfront_origin_access_control" "portfolio" {
name = "portfolio-oac"
description = "OAC for static website portfolio"
origin_access_control_origin_type = "s3" 
signing_behavior = "always"
signing_protocol = "sigv4"
}

# cloudfront function - rewrites directory-style URIs to index.html 
