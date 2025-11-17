locals {
  base_tags = merge(
    {
      Project = var.project_name
    },
    var.tags
  )
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_instance" "bastion" {
  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [var.security_group_id]
  associate_public_ip_address = true
  key_name                    = var.key_name != "" ? var.key_name : null

  tags = merge(local.base_tags, { Name = "${var.project_name}-bastion" })
}

resource "aws_eip" "bastion" {
  domain   = "vpc"
  instance = aws_instance.bastion.id
  tags     = merge(local.base_tags, { Name = "${var.project_name}-bastion-eip" })
}
