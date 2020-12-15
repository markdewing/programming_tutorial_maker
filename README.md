# Programming Tutorial Maker

Tutorials that explain a code as a series of small incremental steps are helpful but time consuming to write.  This project attempts to create a more standardized format to make tutorials easier to create.

The ingredients at each step are
 - a description of the step
 - the source (eventually snippets, highlights, or diffs)
 - test code (optional)
 - compile command and output (optional)
 - output of the test code


The ultimate goal is that entire programs will be represented in this incremental form.  The code in each step will be connected by AST transformations, rather than manually created.  See [Programming by Transformation](https://github.com/markdewing/next_steps_in_programming/blob/master/programming_by_transformations.md) for more thoughts.

## Examples
[Mini C++ MPI3 wrapper](examples/mini_mpi3/output_md/index.md)

## Future
* The current implementation shows the entire source files.  Even for this small example, it gets hard to see the changes from step to step.  Flexible viewing of the source code and changes is essential. A diff view is the most important view to start with.
* Current implementation writes to Markdown. In support to better source code viewing, it will probably need to write to HTML or a JS framework.

## Other Projects

* Software Carpentry has a [lesson template](https://carpentries.github.io/lesson-example/) and guides for creating lessons.
* The HEP Software Foundation has some lessons based on the Software Carpentry templates https://hepsoftwarefoundation.org/training/curriculum.html
* Generator for code walkthrough videos: https://github.com/sleuth-io/code-video-generator
