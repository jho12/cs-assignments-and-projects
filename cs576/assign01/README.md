# Assignment 1
In this assignment, I was given two toy programs (vuln_prog1.bin and vuln_prog2.bin) that include a stack overflow in function complex_verify(). The goal of this assignment was to write a set of exploits that perform code injection on the binaries. We were given several assumptions:

* Disable stack protection: the option -fno-stack-protector was passed to GCC when compiling the victim programs.
* Executable stack: the option -z execstack was passed to GCC when linking the victim programs.
* Disabled ASLR: to exploit the vulnerable programs you will have to disable ASLR in one of the following ways 
  * Run you program using the setarch utility:
    * `$ setarch x86_64 -R ./vuln_prog1.bin`
  * Running programs through gdb disables ASLR to assist in debugging
    * `$ gdb ./vuln_prog1.bin`
    * `$ gdb> run arguments_list ...`

Brief overviews for each task for the assignment can be seen in the `task` files. Implemented in Assembly and Python.