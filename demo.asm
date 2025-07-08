ADDI X0, XZR, #8	// X0 la dia chi mang
AND X1, XZR, X1	// X1 luu tong mang
CBZ X3, #2	// X3 la chi so mang
ORRI X3, XZR, #0
ADDI X4, XZR, #5	// X4 la so phan tu mang
SUBS XZR, X3, X4
B.GE #6
LDUR X2, [X0, #0]
ADD X1, X1, X2
ADDI X3, X3, #1
ADDI X0, X0, #8
B #-6
STUR X1, [XZR, #0]
ADDI X6, X5, #1