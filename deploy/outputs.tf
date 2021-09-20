output "db_host" {
  value = aws_db_instance.main.address
}

output "bastion_host" {
  value = aws_instance.bastion.public_dns
}

# Create a new output value for load balancer dns name once it's been created by Terraform
output "api_endpoint" {
  value = aws_lb.api.dns_name
}