from typing import Dict, List
import hcl2
import re


def xstr(s: str) -> str:
    """ Return empty string

    If the value is a None type, return an empty string

    """
    return "" if s is None else str(s)


def type_str(s: str) -> str:
    """ Returns proper type declarations

    Undeclared types will accept any type in HCL2.

    """
    return "Any" if s is None else str(s)


def remove_special_chars(s: str) -> str:
    """ Removes special chars from string

    python-hcl2 surrounds some values with ${} syntax.  This removes those characters

    """
    return re.sub("[\\$\\{\\}]+", "", s)


def pop_list(attr_list: List):
    """ Convert from list to single value

    python-hcl2 assummes attributes values are lists.
    - https://github.com/amplify-education/python-hcl2/blob/a4b29a76e34bbbd4bcac8d073f96392f451f79b3/hcl2/transformer.py#L120

    This is an edge case in TF, and will never happen in variables and outputs in TF

    Returns:
        single value from list
    """
    return attr_list if attr_list is None else attr_list.pop()


class Document:
    """ Creates a TerraDox instance

    Params:
        input_data: is a file-like object - this is normally from stdin or from reading a file

    """

    def __init__(self, input_data):
        self.data = input_data
        self._output = []
        self._variables = []
        self.vars_table = ""
        self.output_table = ""

    def read(self):
        parsed = hcl2.load(self.data)
        self._output = parsed.get("output")
        self._variables = parsed.get("variable")

        if self._variables:
            vars = Variables(self._variables)
            self.vars_table = vars.create_table()

        if self._output:
            outs = Outputs(self._output)
            self.output_table = outs.create_table()


class Variables:
    def __init__(self, var_list):
        self._variables_list = var_list
        self._header = (
            "# Variables\n| Name | Description | Type | Default\n|---|---|---|---"
        )
        self._body = ""

    def _convert_dict(self, vars_dict: Dict) -> str:
        """ Convert variable to row

        Converts a single HCL2 variable dictionary to a markdown table row.
        The function is specific to TF Variables.  The F-string will not format other
        types of HCL2 dictionaries properly

        Returns:
            string of Markdown with variable data
        """
        for var_name, var_attr in vars_dict.items():
            return (
                f"|{var_name}"
                f"|{xstr(pop_list(var_attr.get('description')))}"
                f"|{remove_special_chars(type_str(pop_list(var_attr.get('type'))))}"
                f"|{xstr(pop_list(var_attr.get('default')))}"
            )

    def create_table(self) -> str:
        for vd in self._variables_list:
            row = self._convert_dict(vd)
            self._body = "\n".join([self._body, row])
        return self._header + self._body


class Outputs:
    def __init__(self, output_list):
        self._outputs_list = output_list
        self._header = "# Output\n|Name|Value|Description\n|---|---|---"
        self._body = ""

    def _convert_dict(self, out_dict: Dict) -> str:
        for out_name, out_attr in out_dict.items():
            return (
                f"|{out_name}"
                f"|{xstr(remove_special_chars(pop_list(out_attr.get('value'))))}"
                f"|{xstr(pop_list(out_attr.get('description')))}"
                f"|{remove_special_chars(type_str(pop_list(out_attr.get('type'))))}"
            )

    def create_table(self):
        for od in self._outputs_list:
            row = self._convert_dict(od)
            self._body = "\n".join([self._body, row])
        return self._header + self._body
