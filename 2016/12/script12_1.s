	.file	"script12.c"
	.text
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	"%d\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB23:
	.cfi_startproc
	endbr64
	subq	$8, %rsp
	.cfi_def_cfa_offset 16
	movl	$33, %ecx
	movl	$1, %edx
	movl	$1, %esi
	jmp	.L2
.L6:
	movl	%edi, %esi
.L2:
.L3:
	endbr64
	movl	%edx, %eax
.L4:
	subl	$1, %eax
	jne	.L4
	leal	(%rsi,%rdx), %edi
	movl	%esi, %edx
	subl	$1, %ecx
	jne	.L6
	movl	$19, %eax
.L5:
	subl	$1, %eax
	jne	.L5
	leal	266(%rdi), %edx
	leaq	.LC0(%rip), %rsi
	movl	$1, %edi
	movl	$0, %eax
	call	__printf_chk@PLT
	movl	$0, %eax
	addq	$8, %rsp
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE23:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	 1f - 0f
	.long	 4f - 1f
	.long	 5
0:
	.string	 "GNU"
1:
	.align 8
	.long	 0xc0000002
	.long	 3f - 2f
2:
	.long	 0x3
3:
	.align 8
4:
