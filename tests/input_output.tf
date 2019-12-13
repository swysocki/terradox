# minimal variable
# if no type is declared, any type will be accepted
variable "minimal_var" {}

# minimal with description
variable "minimal_var_descr" {
  description = "This is a minimal var with a description"
}

# variable with type specified
variable "typed_var" {
  type = string
}

# variable with type and description
variable "type_descrip_var" {
  type        = number
  description = "Variable with type declared and description"
}

# variable with type and default value
variable "type_default_var" {
  type    = string
  default = "Default string value"
}

output "my_simple_output" {
    value = aws_instance.server.private_ip
}

output "a_bit_more_complex" {
  value = aws_instance.server.public_ip
  description = "My server's IP address"
}