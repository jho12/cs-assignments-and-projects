# shell.S
# I pledge my honor that I have abided by the Stevens Honor System.
# Justin Ho

	.global _start

	.text
_start:
	xor %rax, %rax			# clear rax
	addb $59, %al			# syscall 58 is execve
	xor %rsi, %rsi			# clear rsi
	xor %rdx, %rdx			# clear rdx
	xor %rdi, %rdi			# clear rdi
	lea bash+0x44444402(%rip), %rdi
	sub $0x44444402, %rdi		# set rdi to bash
	xor %r8, %r8			# clear r8
	add $8, %r8			# add 8
	mov %rsi, 1(%rdi, %r8, 1)	# null terminate string
	syscall

	# exit(0)
	xor %rax, %rax			# clear rax
	addb $60, %al
	xor %rdi, %rdi
	syscall
bash:
	.ascii "/bin/bash"
