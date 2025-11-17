output "vpc_id" {
  value = module.network.vpc_id
}

output "public_subnet_ids" {
  value = module.network.public_subnet_ids
}

output "private_subnet_ids" {
  value = module.network.private_subnet_ids
}

output "alb_security_group_id" {
  value = module.security.alb_sg_id
}

output "app_security_group_id" {
  value = module.security.app_sg_id
}

output "db_security_group_id" {
  value = module.security.db_sg_id
}

output "bastion_public_ip" {
  value = module.bastion.public_ip
}

output "bastion_instance_id" {
  value = module.bastion.instance_id
}

output "nat_gateway_id" {
  value = module.network.nat_gateway_id
}
