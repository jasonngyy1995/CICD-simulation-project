data "aws_ami" "amazon_linux" {
  most_recent = true
  filter {
    name = "name"
    # * -> retrieve the latest version
    # most_recent = true
    values = ["amzn2-ami-hvm-2.0.*-x86_64-gp2"]
  }
  owners = ["amazon"]
}

resource "aws_instance" "bastion" {
  # match data field above
  # resource in terraform, 'data' is for retrieving information from AWS
  # create aws instance in our aws account
  ami = data.aws_ami.amazon_linux.id
  # Type -> how much resources will be assigned to that machine
  instance_type = "t2.micro"

  tags = {
    Name = "${local.prefix}-bastion"
  }
}

# In Terraform documentation, 'Data Source' is only for getting information
# 'Resource' is for creating resources