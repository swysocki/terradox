from sys import stdin
from pprint import pprint

from terradox import document

if __name__ == "__main__":
    dox = document.Document(stdin)
    dox.read()
    print(dox.output_table)
    print(dox.vars_table)