resource "aws_s3_bucket" "raw_images" {
  bucket = "${var.project_name}-raw-images"

  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.raw_images.id

  versioning_configuration {
    status = "Enabled"
  }
}
