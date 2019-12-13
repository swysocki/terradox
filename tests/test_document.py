import io
from terradox import document

complex_var = """variable "type_default_var" {
  type    = string
  default = "Default string value"
}"""

complex_output = """output "a_bit_more_complex" {
  value = aws_instance.server.public_ip
  description = "My server's IP address"
}"""

complex_var_table = """# Variables
| Name | Description | Type | Default
|---|---|---|---
|type_default_var||string|Default string value"""

complex_output_table = """# Output
|Name|Value|Description
|---|---|---
|a_bit_more_complex|aws_instance.server.public_ip|My server's IP address|Any"""


def test_xstr():
    assert document.xstr(None) == ""
    assert document.xstr("Mystring") == "Mystring"


def test_type_str():
    assert document.type_str(None) == "Any"
    assert document.type_str("Mystring") == "Mystring"


def test_remove_special_chars():
    assert document.remove_special_chars("${Mystring}") == "Mystring"
    assert (
        document.remove_special_chars("${my_resource.resource.foo-bar}")
        == "my_resource.resource.foo-bar"
    )


def test_pop_list():
    assert document.pop_list(None) is None
    assert document.pop_list(["Mylist"]) == "Mylist"


def test_variable_document():
    v = document.Document(io.StringIO(complex_var))
    v.read()
    assert len(v._variables) > 0
    assert v.vars_table == complex_var_table


def test_output_document():
    o = document.Document(io.StringIO(complex_output))
    o.read()
    assert len(o._output) > 0
    assert o.output_table == complex_output_table
