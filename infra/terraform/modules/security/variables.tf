variable "project_name" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "allowed_ssh_cidrs" {
  type = list(string)
}

variable "tags" {
  type = map(string)
  default = {}
}
