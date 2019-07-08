#!/bin/env python
from __future__ import print_function

import glob
import os
import sys

# This script creates step-by-step programming tutorials from a set of
# structured directories.  Output format is currently markdown.
# The input elements for each step in the tutorial are a description, the source code,
# a test code, the run command, and the output of the run command.

# Input on the command line is a list of directories (in order).
# This script also assumes a directory named 'overview'.

# Certain metadata is entered in desc.txt on lines with '% key: value'.

# The 'overview' directory contains the file 'desc.txt' with a description
# of the tutorial.  Expected metadata in the file is 'name', which is
# the name of the tutorial.  It will used as the heading on this page and other pages.
# Output is 'index.md' containing the descriptin and navigation to the list of steps.

# Individual step directories have more files.  Expected is a 'desc.txt' file which is
# a description of this step of the tutorial.  The 'name' key is the title of this step.
# Optional files are:
#  *.hpp - source code
#  test_main.cpp - test driver
#  sample_run.sh - the run command
#  sample_output.txt - output of the test driver




# Helper functions for producing markdown

def escape_code(s):
  out = "```\n"
  out += s
  out += "```\n"
  return out

def make_link(link_addr, name):
    return "[%s](%s)"%(name,link_addr)

def make_header(text, level=3):
  return "#"*level + " " + text + "\n"


# Text file processing
# Comment lines start with %
# Metadata has the form % <key> : <value>

def process_text_file(f):
  text = ""
  metadata = dict()
  for line in f:
    if line.startswith('%'):
      line = line[1:]
      vals = line.split(':')
      if len(vals) > 1:
        key = vals[0].strip().lower()
        value = vals[1].strip()
        metadata[key] = value
    else:
      text += line

  return text, metadata


# Convert one step to a structured format (markdown for now)

def compile_one_step(dirname, overall_name=""):
  out = ''
  fnames = os.listdir(dirname)
  if 'desc.txt' in fnames:
    with open(os.path.join(dirname,'desc.txt'),'r') as f:
      desc_text, desc_metadata = process_text_file(f)
      step_name = desc_metadata["name"]
      out += make_header(overall_name, level=1)
      out += make_header(step_name, level=2)
      out += desc_text
      out += "\n"

  src_files = glob.glob(dirname + "/*.hpp")
  if src_files:
    out += make_header("Source")
    out += src_files[0] + '\n'
    with open(src_files[0], 'r') as f:
      out += escape_code(f.read())
      out += "\n"

  test_desc_file = os.path.join(dirname, "/test_desc.txt")
  if os.path.exists(test_desc_file):
    with open(test_desc_file, 'r') as f:
      out += f.read()
      out += "\n"

  test_files = glob.glob(dirname + "/test_main.cpp")
  if test_files:
    out += make_header("Test code")
    out += test_files[0] + '\n'
    with open(test_files[0], 'r') as f:
      out += escape_code(f.read())
      out += "\n"

  run_cmd_file = 'sample_run.sh'
  try:
    with open(os.path.join(dirname, run_cmd_file), 'r') as f:
      out += "\n"
      out += make_header("Run command")
      out += escape_code(f.read())
      out += "\n"
  except IOError:
    pass

  output_file = 'sample_output.txt'
  with open(os.path.join(dirname, output_file), 'r') as f:
    out += "\n"
    out += "### Run output \n"
    out += escape_code(f.read())
    out += "\n"

  return out, step_name

def get_overview(dirname):
  overview_file = os.path.join(dirname, "desc.txt")
  with open(overview_file,'r') as f:
    text, metadata = process_text_file(f)
    return text, metadata

  return "", dict()


# Add navigation to next/previous steps
def add_step_nav(out, prev_step=None, next_step=None, home_step=None):
  if next_step:
    next_name = next_step[0]
    next_file = next_step[1]
    out += "Next: " + make_link(next_file, next_name) + "\n"

  if prev_step:
    prev_name = prev_step[0]
    prev_file = prev_step[1]
    out += "\nPrev: " + make_link(prev_file, prev_name) + "\n"

  return out


# Convert all the steps and the overview

def compile_steps(dirnames, overall_name):
  outputs = []
  for dirname in dirnames:
    out, step_name = compile_one_step(dirname, overall_name)
    outputs.append( (dirname, step_name, out) )

  outputs_with_nav = []
  for idx, (dirname, step_name, out) in enumerate(outputs):
    next_step = None
    if idx+1 < len(outputs):
      step = outputs[idx+1][0]
      next_step_name = outputs[idx+1][1]
      next_step_fname = 'out_' + step + '.md'
      next_step = (next_step_name, next_step_fname)

    prev_step = None
    if idx > 0:
      step = outputs[idx-1][0]
      prev_step_name = outputs[idx-1][1]
      prev_step_fname = 'out_' + step + '.md'
      prev_step = (prev_step_name, prev_step_fname)


    out = add_step_nav(out, prev_step=prev_step, next_step=next_step)
    outputs_with_nav.append( (dirname, out) )

  for dirname, out in outputs_with_nav:
    out_fname = 'out_' + dirname + '.md'
    with open(out_fname,'w') as f:
      f.write(out)

  return outputs


def compile_overview(overview_text, steps, overall_name):
  out = make_header(overall_name, level=1)
  out += overview_text

  out += make_header("Steps")
  for (i,(dirname, step_name, step_text)) in enumerate(steps):
    step_idx = i+1
    step_fname = 'out_' + dirname + '.md'
    out += "%d. "%step_idx + make_link(step_fname, step_name) + "\n"

  out_fname = 'index.md'
  with open(out_fname, 'w') as f:
    f.write(out)


if __name__ == '__main__':
  if len(sys.argv) > 1:
    dirnames = sys.argv[1:]
  else:
    dirnames = [os.getcwd()]

  overview_text, overview_metadata = get_overview('overview')
  overall_name = overview_metadata["name"]

  steps = compile_steps(dirnames, overall_name)
  compile_overview(overview_text, steps, overall_name)
