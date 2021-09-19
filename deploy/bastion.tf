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

# Create a new IAM role
resource "aws_iam_role" "bastion" {
  name               = "${local.prefix}-bastion"
  assume_role_policy = file("./templates/bastion/instance-profile-policy.json")
  tags               = local.common_tags
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "bastion_attach_policy" {
  role       = aws_iam_role.bastion.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_instance_profile" "bastion" {
  name = "${local.prefix}-bastion-instance-profile"
  role = aws_iam_role.bastion.name
}

resource "aws_instance" "bastion" {
  # match data field above
  # resource in terraform, 'data' is for retrieving information from AWS
  # create aws instance in our aws account
  ami                  = data.aws_ami.amazon_linux.id
  user_data            = file("./templates/bastion/user-data.sh")
  iam_instance_profile = aws_iam_instance_profile.bastion.name

  # Subnet for AWS instance to launch
  subnet_id = aws_subnet.public_a.id
  key_name  = var.bastion_key_name

  vpc_security_group_ids = [
    aws_security_group.bastion.id
  ]

  # Type -> how much resources will be assigned to that machine
  instance_type = "t2.micro"
  # include base tag and the custom name tag of our resource
  tags = merge(
    local.common_tags,
    tomap({
      "Name" = "${local.prefix}-bastion"
    })
  )
}

# In Terraform documentation, 'Data Source' is only for getting information
# 'Resource' is for creating resources

resource "aws_security_group" "bastion" {
  description = "Control inbound and outbound access of bastion"
  name        = "${local.prefix}-bastion"
  vpc_id      = aws_vpc.main.id


  # Only allows inbound access on port 22
  ingress {
    protocol  = "tcp"
    from_port = 22
    to_port   = 22
    # Allow access from any IP address, could set to static IP access for other situdation
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 5432
    to_port   = 5432
    protocol  = "tcp"
    cidr_blocks = [
      aws_subnet.private_a.cidr_block,
      aws_subnet.private_b.cidr_block,
    ]
  }

  tags = local.common_tags
}
