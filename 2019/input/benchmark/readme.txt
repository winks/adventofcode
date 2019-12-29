https://www.reddit.com/r/adventofcode/comments/egq9xn/2019_day_9_intcode_benchmarking_suite/

sum-of-primes: This program takes a single input and produces a single output, the sum of all primes up to the input
For example, when run with input 10, it should produce 17. When run with input 2000000, it should produce 142913828922.

sum-of-primes requires O(n) memory.


ackermann: This program takes two numbers m and n and produces a single output, the two-argument Ackermann function A(m, n).
For example, when run with input 2 and 4, it should produce 11. When run with input 3 and 2, it should produce 29. Can you make it halt for inputs 4 and 1?

ackermann requires O(A(m, n)) memory.


isqrt: This program takes one non-negative number and produces its integer square root.
For example, when run with input 16, it should produce 4. When run with input 130, it should produce 11. It's quite slow since it relies on division by repeated subtraction, and I can't be bothered to improve it.


divmod: This program takes two positive numbers a and b, and returns the quotient and remainder of their Euclidean division a / b and a % b. It works by binary long division, so it's quite efficient. If your intcode VM implementation supports big integers, it can deal with inputs up to 2^200. It works with 64 bit and 32 bit ints, too, but relies on signed overflow in this case.
For example, when run with inputs 1024 and 3, it should produce 341 and 1. When run with inputs 2842238103274937687216392838982374232734 and 2384297346348274, it should produce 1192065288177262577484639 and 768603395069648, assuming your intcode VM supports big integers.


factor: This program takes in a number and produces its prime factorization.
For example, when run with input 399, it should produce 3, 7, and 19. When run with input -1024, it should produce -1, then 2 ten times. When run with input 2147483647, it should produce 2147483647. When run with input 19201644899, it should produce 138569 and 138571.

factor requires O(sqrt(n)) memory.
