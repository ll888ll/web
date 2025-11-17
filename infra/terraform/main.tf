module "network" {
  source          = "./modules/network"
  project_name    = var.project_name
  vpc_cidr        = var.vpc_cidr
  public_subnets  = var.public_subnets
  private_subnets = var.private_subnets
  tags            = var.tags
}

module "security" {
  source            = "./modules/security"
  project_name      = var.project_name
  vpc_id            = module.network.vpc_id
  allowed_ssh_cidrs = var.allowed_ssh_cidrs
  tags              = var.tags
}

module "bastion" {
  source            = "./modules/bastion"
  project_name      = var.project_name
  subnet_id         = module.network.public_subnet_ids[0]
  security_group_id = module.security.bastion_sg_id
  instance_type     = var.bastion_instance_type
  key_name          = var.bastion_key_pair
  tags              = var.tags
}
