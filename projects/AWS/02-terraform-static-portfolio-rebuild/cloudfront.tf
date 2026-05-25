# origin access control - grant cloudfront permission to access the private s3 bucket 
resource "aws_cloudfront_origin_access_control" "portfolio" {
  name                              = "portfolio-oac"                    # you make this up. your label.
  description                       = "OAC for static website portfolio" # description obviously
  origin_access_control_origin_type = "s3"                               # connecting to s3
  signing_behavior                  = "always"                           # always sign requests with sigv4
  signing_protocol                  = "sigv4"                            # AWS signature version 4
}

# cloudfront function - rewrites directory-style URIs to index.html 
resource "aws_cloudfront_function" "rewrite_uri" {
  name    = "rewrite_uri"       # your own label
  runtime = "cloudfront-js-2.0" # cloudfront's javascript runtime 
  publish = true                # publish immediately on apply

  code = <<-EOT
    async function handler(event) {
      var request = event.request;
      var uri = request.uri;
      if (uri.endsWith('/')) {
        request.uri += 'index.html';
      } else if (!uri.includes('.')) {
        request.uri += '/index.html';
      }
      return request;
    }
  EOT
}

# cloudfront distribution 
resource "aws_cloudfront_distribution" "portfolio" {
  enabled             = true         # distribution is active 
  default_root_object = "index.html" # serves index.html when hitting the root URL

  # origin - points to cloudfront at the s3 bucket 
  origin {
    domain_name              = aws_s3_bucket.portfolio.bucket_regional_domain_name #s3 bucket endpoint
    origin_id                = "S3Origin"                                          # my label for this origin
    origin_access_control_id = aws_cloudfront_origin_access_control.portfolio.id   #attaches the OAC
  }

  # default cache behavior — how CloudFront handles requests
  default_cache_behavior {
    target_origin_id       = "S3Origin"          # must match origin_id above
    viewer_protocol_policy = "redirect-to-https" # force HTTPS

    allowed_methods = ["GET", "HEAD"] # only allow read requests
    cached_methods  = ["GET", "HEAD"] # cache these methods

    cache_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6" # AWS managed cache policy (CachingOptimized)

    # attach the CloudFront Function for URI rewriting
    function_association {
      event_type   = "viewer-request"                        # fires on every incoming request
      function_arn = aws_cloudfront_function.rewrite_uri.arn # references the function above
    }
  }

  # no geographic restrictions
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  # use default CloudFront certificate — no custom domain used for this project
  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = {
    Name        = "static-portfolio"
    Environment = "lab"
  }
}