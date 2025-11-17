output "instance_id" {
  value = aws_instance.bastion.id
}

output "public_ip" {
  value = aws_eip.bastion.public_ip
}

output "subnet_id" {
  value = var.subnet_id
}
