	.file	"script12.c"
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	$0, -16(%rbp)
	movl	$0, -12(%rbp)
	movl	$0, -8(%rbp)
	movl	$0, -4(%rbp)
	movl	$1, -8(%rbp)
	movl	$1, -16(%rbp)
	movl	$1, -12(%rbp)
	movl	$26, -4(%rbp)
	cmpl	$0, -8(%rbp)
	je	.L16
	nop
.L3:
	endbr64
	movl	$7, -8(%rbp)
.L5:
	addl	$1, -4(%rbp)
	subl	$1, -8(%rbp)
	cmpl	$0, -8(%rbp)
	je	.L17
	jmp	.L5
.L4:
.L16:
	nop
	jmp	.L10
.L17:
	nop
.L6:
.L10:
	movl	-16(%rbp), %eax
	movl	%eax, -8(%rbp)
.L7:
	addl	$1, -16(%rbp)
	subl	$1, -12(%rbp)
	cmpl	$0, -12(%rbp)
	je	.L8
	jmp	.L7
.L8:
	movl	-8(%rbp), %eax
	movl	%eax, -12(%rbp)
	subl	$1, -4(%rbp)
	cmpl	$0, -4(%rbp)
	je	.L9
	jmp	.L10
.L9:
	movl	$19, -8(%rbp)
.L11:
	movl	$14, -4(%rbp)
.L12:
	addl	$1, -16(%rbp)
	subl	$1, -4(%rbp)
	cmpl	$0, -4(%rbp)
	je	.L13
	jmp	.L12
.L13:
	subl	$1, -8(%rbp)
	cmpl	$0, -8(%rbp)
	je	.L14
	jmp	.L11
.L14:
	movl	$0, %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
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
