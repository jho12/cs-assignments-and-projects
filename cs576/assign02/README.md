# Assignment 2
In this assignment, I was given vuln_prog1.bin (a 32-bit vulnerable program) and vuln_prog2.bin (a 64-bit vulnerable program). The goal of this assignment was to write a set of exploits that perform return-to-libc attacks on dynamically linked applications of different architectures. Additionally, this assignment gave us several assumptions:

* Disabled stack protection: the option -fno-stack-protector was passed to GCC when compiling the victim programs. 
* Disabled ASLR: to exploit the vulnerable programs you will have to disable ASLR
  * i.e., `$ setarch x86_64 -R ./vuln_prog1.bin` 
* Dynamic linked binary: both the 32-bit and 64-bit binaries are dynamically linked. This means that libc is loaded during runtime and thus its location needs to be discovered. Libc functions are located in a fixed offset inside the library.

I was additionally given source code to the binaries. Overviews of each task to be done are within each `task` file. Implementation in Python.