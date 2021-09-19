#!/bin/bash

# Install and enable docker on system
sudo yum update -y
sudo amazon-linux-extras install -y docker
sudo systemctl enable docker.service
sudo systemctl start docker.service
# Add the EC2 user to the bastion group, the default username is ec2-user
sudo usermod -aG docker ec2-user