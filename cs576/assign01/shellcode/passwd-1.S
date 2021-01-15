# passwd-1.S
# I pledge my honor that I have abided by the Stevens Honor System.
# Justin Ho
	
	.global _start

	.text
_start:
	# open(passwd, 0, 0)
	xor %eax, %eax				# clear rax
	addb $2, %al				# syscall 2 is open
	xor %esi, %esi				# set flags to 0
	xor %edx, %edx				# set mode to 0
	xor %rdi, %rdi				# clear rdi
	lea passwd+0x44444401(%rip), %rdi	
	sub $0x44444401, %rdi			# set filename to /etc/passwd
	xor %r8, %r8				# clear r8
	add $8, %r8				# set r8 to 8
	mov %edx, 3(%rdi, %r8, 1)		# null terminate filename string
	syscall

	# read(fd, buffer, 48)
	xor %edi, %edi		# clear rdi
	mov %eax, %edi		# read passwd file at fd in rax
	xor %eax, %eax		# syscall 0 is read
	sub $0x30, %rsp		# create buffer in stack
	mov %rsp, %rsi		# assign buffer
	addb $0x30, %dl		# read 48 characters
	syscall

	# write(1, buffer, 48)
	xor %eax, %eax
	inc %eax		# syscall 1 is write
	xor %edi, %edi
	inc %edi		# fd 1 is stdout
	syscall

	# exit(0)
	xor %eax, %eax		# clear rax
	addb $60, %al
	xor %edi, %edi
	syscall
passwd:
	.ascii "/etc/passwd"
