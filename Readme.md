> **_NOTE:_** this project was useful when `terraform-docs` didn't support Terraform version 0.12 syntax. I highly recommend https://github.com/terraform-docs/terraform-docs now.

# Terradox

Convert Terraform variables and outputs to Markdown tables

## Use

The `make_markdown.py` script is a wrapper around the Terradox module.  It accepts stdin and outputs the markdown as stdout.

### Example

`cat tests/input_output.tf | python3 make_markdown.py >> Readme.md`

the result is:

# Output
|Name|Value|Description
|---|---|---
|my_simple_output|aws_instance.server.private_ip||Any
|a_bit_more_complex|aws_instance.server.public_ip|My server's IP address|Any
# Variables
| Name | Description | Type | Default
|---|---|---|---
|minimal_var||Any|
|minimal_var_descr|This is a minimal var with a description|Any|
|typed_var||string|
|type_descrip_var|Variable with type declared and description|number|
|type_default_var||string|Default string value
