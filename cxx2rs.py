#!/usr/bin/env python
""" Usage: call with <filename> <typename>
"""

import sys
import clang.cindex

from ctypes.util import find_library
clang.cindex.Config.set_library_file(find_library('clang'))

from rustify import *
from stringify import *
import itertools
import sets

header = """
#![crate_type = "lib"]
#![crate_name = "ssh"]

extern crate libc;
use std::mem;

use std::collections::enum_set::CLike;

"""

def unique(input):
    output = []
    for el in input:
        if el not in output:
            output.append(el)
    return output

def main():
    index = clang.cindex.Index.create()

    args = sys.argv[1:]
    link_name = args.pop(0)
    fname = args.pop(0)

    tu = index.parse(fname, args, options=0x80 | 0x01 | 0x02)

    print header

    all_functions1, all_functions2 = itertools.tee(get_functions(tu.cursor, tu.spelling))
    for func in all_functions1:
        print "/*\n%s*/" % stringify_function_declaration(func)
        print rustify_function_declaration(func, link_name)
        print

    all_structs = unique(get_structs(tu.cursor, tu.spelling) +
                            get_function_arg_structs(all_functions2))
    for struct in all_structs:
        print "/*\n%s*/" % stringify_struct_declaration(struct)
        print rustify_struct_declaration(struct)

    all_enums = get_enums(tu.cursor, tu.spelling)
    for enum in all_enums:
        print "/*\n%s*/" % stringify_enum_declaration(enum)
        print rustify_enum_declaration(enum)

    all_macros = get_macros(tu.cursor, tu.spelling)
    for m in all_macros:
        print "/* %s */" % stringify_macro_declaration(m)
        print rustify_macro_declaration(m)

"""
    get_arguments = lambda arg: arg._tu
    all_args = map(lambda fn: map(get_arguments, fn.get_arguments()), get_functions(tu.cursor, tu.spelling))
    #print set(reduce(lambda a,b: a+b, all_args))
"""

if __name__ == "__main__":
    main()
