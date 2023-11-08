output "vpc_cidr" {
  value = aws_vpc.default.cidr_block
}

output "subnet_vpc" {
  value = {
    public_cidr_block =  { for i, v in aws_subnet.public_subnets : format("public_ip%d", i + 1) => v.cidr_block }
    private_cidr_block =  { for i, v in aws_subnet.private_subnets : format("private_ip%d", i + 1) => v.cidr_block }
  }
}

output "s3" {
  value = {
    s3_trungtpp = aws_s3_bucket.example.bucket
  }
}