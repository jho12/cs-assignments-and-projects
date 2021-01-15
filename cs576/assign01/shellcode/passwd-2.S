# passwd-2.S
# I pledge my honor that I have abided by the Stevens Honor System.
# Justin Ho
	
	.global _start

	.text
_start:
	# open(passwd, 0, 0)
	xor %eax, %eax				# clear eax
	addb $2, %al				# syscall 2 is open
	xor %esi, %esi				# set flags to 0
	xor %edx, %edx				# set mode to 0
	lea passwd+0x44444401(%rip), %rdi
	sub $0x44444401, %rdi			# set filename as /etc/passwd
	xor %r8, %r8				# clear r8
	add $8, %r8				# set r8 to 9
	mov %edx, 3(%rdi, %r8, 1)		# null terminate the string
	syscall

	# read(fd, buffer, 1)
	mov %eax, %r8d		# put passwd fd in r8d
	dec %rsp		# create 1-char buffer in stack
	mov %rsp, %rsi		# assign buffer to rsi
	xor %edx, %edx		# clear edx
	inc %dl			# read a character at a time

.read:				# jumpable section for looping through file
	xor %rdi, %rdi
	mov %r8, %rdi		# set rdi to passwd fd
	xor %eax, %eax		# syscall 0 is read
	syscall
	test %eax, %eax		# test if read syscall returns 0
	je .exit		# if syscall returns 0, go to .exit

	xor %eax, %eax		# filler instruction to pad je instruction
	
	# write(1, buffer, 1)
	xor %eax, %eax
	inc %eax		# syscall 1 is write
	xor %edi, %edi
	inc %edi		# fd 1 is stdout
	syscall
	jmp .read		# loop back to .read

.exit:	# jumpable section once program reaches EOF
	# exit(0)
	# xor eax, eax excluded because eax is already cleared
	addb $60, %al
	xor %edi, %edi
	syscall
passwd:
	.ascii "/etc/passwd"
