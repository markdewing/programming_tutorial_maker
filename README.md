# Programming Tutorial Maker

Tutorials that explain a code as a series of small incremental steps are helpful but time consuming to write.  This project attempts to create a more standardized format to make tutorials easier to create.

The ingredients at each step are
 - a description of the step
 - the source (eventually snippets, highlights, or diffs)
 - test code (optional)
 - compile command and output (optional)
 - output of the test code


The ultimate goal is that entire programs will be represented in this incremental form.  The code in each step will be connected by AST transformations, rather than manually created.  See [Programming by Transformation](https://github.com/markdewing/next_steps_in_programming/blob/master/programming_by_transformations.md) for more thoughts.
