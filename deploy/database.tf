# Allow adding multiple subnets to database
resource "aws_db_subnet_group" "main" {
  name = "${local.prefix}-main"
  subnet_ids = [
    aws_subnet.private_a.id,
    aws_subnet.private_b.id
  ]
  tags = merge(
    local.common_tags,
    map("Name", "${local.prefix}-main")
  )
}

# Control rules for inbound access
resource "aws_security_group" "rds" {
  description = "Allow access to the RDS database instance."
  name        = "${local.prefix}-rds-inbound-access"
  vpc_id      = aws_vpc.main.id

  ingress {
    protocol = "tcp"
    # Default port for Postgres
    from_port = 5432
    to_port   = 5432
  }

  tags = local.common_tags
}

resource "aws_db_instance" "main" {
  # Database identifier used to access the database
  identifier = "${local.prefix}-db"

  # Define the name of database that is created with instance
  name              = "recipe"
  allocated_storage = 20

  # Entry level storage type in AWS
  storage_type   = "gp2"
  engine         = "postgres"
  engine_version = "11.4"

  # Type of database server
  instance_class       = "db.t2.micro"
  db_subnet_group_name = aws_db_subnet_group.main.name
  username             = var.db_username
  password             = var.db_password

  # Numbers of days for maintaining backup, set to 0 because the app is for course use only
  backup_retention_period = 0
  multi_az                = false
  skip_final_snapshot     = true
  vpc_security_group_ids  = [aws_security_group.rds.id]

  tags = merge(
    local.common_tags,
    map("Name", "${local.prefix}-main")
  )
}
