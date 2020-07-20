# coding: utf-8
"""
Batch-convert MD and HTML files to DITA.
"""

import os
import sys
import re
import argparse
from MarkUP import (progressbar as pb,
                    exit_prompt,
                    markdown_str_to_html_str,
                    html_str_to_markdown_str,
                    markdown_str_to_dita_str,
                    html_str_to_dita_str,
                    read_file,
                    enter_filepath,
                    save_str_as_file,
                    files_list,
                    file_extension
                    )
__version__ = "0.1"
__author__ = "Rafał Karoń <rafalkaron@gmail.com>"

def convert_folder(source, input_extension, converter, output_folder, output_extension):
    for input_filepath in files_list(source, input_extension):
        output_file = os.path.basename(re.sub(f".{input_extension}", f".{output_extension}", input_filepath, flags=re.IGNORECASE))
        output_str = converter(read_file(input_filepath), output_file)
        save_str_as_file(output_str, output_folder + "/" + output_file)

def convert_file(input_filepath, converter, output_extension):
    input_extension = file_extension(input_filepath)
    output_file = os.path.basename(re.sub(f".{input_extension}", f".{output_extension}", input_filepath, flags=re.IGNORECASE))
    output_folder = os.path.dirname(os.path.abspath(input_filepath))
    output_str = converter(read_file(input_filepath), output_file)
    save_str_as_file(output_str, output_folder + "/" + output_file)

def main():
    par = argparse.ArgumentParser(description="Batch-convert Markdown and HTML files to DITA.", formatter_class=argparse.RawTextHelpFormatter)
    par.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    par.add_argument("-in", "--input", metavar="source", help="manually specify the input folder (defualts to MarkUP executable folder)")
    par.add_argument("-out", "--output", metavar="output_folder", help="manually specify the output folder (defaults to the input folder)")
    par.add_argument("-md_html", "--markdown_to_html", action="store_true", help="convert Markdown files to HTML files")
    par.add_argument("-html_md", "--html_to_markdown", action="store_true", help="convert HTML files to Markdown files")
    par.add_argument("-md_dita", "--markdown_to_dita", action="store_true", help="convert Markdown files to DITA files")
    par.add_argument("-html_dita", "--html_to_dita", action="store_true", help="convert HTML files to DITA files")
    par.add_argument("-ex", "--exit", action ="store_true", help="exits without a prompt (defaults to prompt on exit)")
    args = par.parse_args()

    if getattr(sys, 'frozen', False):
        exe_path = os.path.dirname(sys.executable)
    elif __file__:
        exe_path = os.path.dirname(__file__)

    if not args.input:
        source = exe_path
    if args.input:
        source = args.input
    if not args.output:
        output_folder = source
    if args.output:
        output_folder = args.output

    if args.markdown_to_html:
        convert_file(source, markdown_str_to_html_str, "html")
        #convert_folder(source, "md", markdown_str_to_html_str, output_folder, "html")
    if args.html_to_markdown:
        convert_folder(source, "html", html_str_to_markdown_str, output_folder, "md")
    if args.markdown_to_dita:
        convert_folder(source, "md", markdown_str_to_dita_str, output_folder, "dita")
    if args.html_to_dita:
        convert_folder(source, "html", html_str_to_dita_str, output_folder, "dita")

    if not args.markdown_to_html and not args.html_to_markdown and not args.markdown_to_dita and not args.html_to_dita and not args.exit:
        par.print_help()
    if not args.exit:
        exit_prompt("\nTo exit MarkUP, press [Enter]")

if __name__ == "__main__":
    main()