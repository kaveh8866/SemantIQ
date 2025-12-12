variable "db_identifier" {
  type        = string
  default     = "semantiq-db"
}

variable "db_username" {
  type        = string
}

variable "db_password" {
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  type        = string
  default     = "db.t3.micro"
}

resource "aws_db_subnet_group" "primary" {
  name       = "semantiq-db-subnets"
  subnet_ids = var.subnet_ids
}

variable "subnet_ids" {
  type = list(string)
}

resource "aws_db_instance" "postgres" {
  identifier             = var.db_identifier
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "15"
  instance_class         = var.db_instance_class
  username               = var.db_username
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.primary.name
  skip_final_snapshot    = true
  publicly_accessible    = false
}

output "db_endpoint" {
  value = aws_db_instance.postgres.address
}

output "db_url" {
  value = "postgresql://${var.db_username}:${var.db_password}@${aws_db_instance.postgres.address}:5432/postgres"
  sensitive = true
}

