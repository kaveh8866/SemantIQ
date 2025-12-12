variable "cache_identifier" {
  type        = string
  default     = "semantiq-cache"
}

variable "cache_node_type" {
  type        = string
  default     = "cache.t3.micro"
}

variable "cache_engine_version" {
  type        = string
  default     = "7.0"
}

resource "aws_elasticache_subnet_group" "primary" {
  name       = "semantiq-cache-subnets"
  subnet_ids = var.subnet_ids
}

resource "aws_elasticache_replication_group" "redis" {
  replication_group_id          = var.cache_identifier
  description                   = "SemantIQ Redis"
  engine                        = "redis"
  engine_version                = var.cache_engine_version
  node_type                     = var.cache_node_type
  automatic_failover_enabled    = false
  num_cache_clusters            = 1
  subnet_group_name             = aws_elasticache_subnet_group.primary.name
}

output "redis_endpoint" {
  value = aws_elasticache_replication_group.redis.primary_endpoint_address
}

