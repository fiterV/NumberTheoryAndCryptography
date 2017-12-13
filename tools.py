from fractions import gcd
from math import sqrt
import random

def MillerRabin(n):
	"""
		Probabilistic primality test.
		Returns 1 if number is probable prime, 0 otherwise.
		Theory: https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
	"""
	if (n==2 or n==3):return 1
	if (n%2==0): return 0
	m = n-1
	t = 0
	while (m%2==0):
		m//=2
		t+=1
	for i in range(1, 10):
		a = random.randrange(2, n-2)
		u = pow(a, m, n)
		if u!=1:
			j = 1
			while u!=n-1 and j<t:
				u = (u*u % n)
				j+=1
			if (u!=n-1):
				return 0
	return 1

def PollardRhoForFactorization(n):
	"""
		Pollard's rho algorithm for integer factorization. Function returns random divisor of n
		Theory: https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm
	"""
	if (MillerRabin(n)):
		return n
	p = int(sqrt(n))
	if (p**2==n):
		return p
	start = 1
	while True:
		start+=1
		x = start
		f = lambda x: (x**2 + 1) % n
		y = f(x)
		d = 1
		while d == 1:
			x = f(x); y = f(f(y))
			d = gcd(abs(x-y), n)
		if d != n:
			return d


def FastFactorizationUsingStack(n):
	"""
		Complete factorization of a number using Pollard's rho algorithm. Returns dictionary where (key, value) means that n is divisible by key^value
	"""
	d={}
	x = [n]
	while len(x)>0:
		n = x.pop()
		if (MillerRabin(n)):
			d[n] = (1 if not (n in d) else d[n]+1)
		else:
			div = PollardRhoForFactorization(n)
			x.append(div)
			x.append(n//div)
	return d


def PhiFastComputation(n):
	"""
		Returns Euler's totient function of n using FastFactorizationUsingStack
		Theory: https://en.wikipedia.org/wiki/Euler%27s_totient_function
	"""
	d = FastFactorizationUsingStack(n)
	res = n
	for key in d:
		res*=key-1
		res//=key
	return res

def MobiusFastComputation(n):
	"""
		Returns Mobius function of n using FastFactorizationUsingStack
		Theory: https://en.wikipedia.org/wiki/M%C3%B6bius_function
	"""
	if n==1:
		return 1
	d = FastFactorizationUsingStack(n)
	for key in d:
		if (d[key]>=2):
			return 0
	return (1 if len(d.keys())%2==0 else -1)

def GetRandomPrime(bits):
	"""
		Returns random prime number with certain number of bits
	"""
	x = random.randint(2**bits, 2**(bits+1)-1)
	while (not MillerRabin(x)):
		x+=1
	return x

def gcd_ex(a, b):
	"""
		Extended Euclidean algorithm : a*x+b*y=gcd(a, b) . In this library is used in RSA scheme in order to find inverse element in some field
		Theory: eng: https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
				rus version: http://e-maxx.ru/algo/extended_euclid_algorithm
	"""
	if (a==0):
		return (0, 1)
	xx = gcd_ex(b%a, a)
	x = xx[1]-(b//a)*xx[0]
	y = xx[0]
	return (x, y)

def RSASCHEME():
	"""
		Outputs RSA scheme: creating base, randomly picking a number, ciphering and deciphering it
		Theory and inspiration: https://www.youtube.com/watch?v=wXB-V_Keiu8
	"""
	# 2 random prime numbers
	p = GetRandomPrime(100)
	q = GetRandomPrime(100)
	N = p*q
	phiN = (p-1)*(q-1)

	print("Two random prime numbers: ", p, q)
	e = 13 #public_exponent
	while gcd(phiN, e)>1: e+=1
	print("E(public exponent) = ", e)
	k = 1
	d = gcd_ex(e, phiN)[0]
	d = (d % phiN + phiN)%phiN
	print("D(private key) = ", d)
	print("N = ", N)
	m = random.randrange(10, 1000000000000000000)
	print("we pick M, let's say : ", m)
	# n and e form and open lock
	# At this point, Alice sends n and e to Bob
	# Bob locks his message by calculating m^e % n = c
	# c - encrypted message
	c = pow(m, e, N)
	print("Encode M into C = ", c)
	# Bob sends c back to Alice

	#Alice calculates m by: c^d % n = m
	m2 = pow(c, d, N)
	print("Decoding C : ", m2)

def JacobiSymbol(a, n):
	"""
		Returns Jacobi symbol for a/n .
		Theory and properties were taken from: 
			https://en.wikipedia.org/wiki/Jacobi_symbol
			http://2000clicks.com/mathhelp/NumberTh27JacobiSymbolAlgorithm.aspx
	"""
	if (n == 1 and a==0):
		return 1
	if (gcd(a, n)!=1):
		return 0
	if (a>=n):
		return JacobiSymbol(a % n, n)
	if (a==1 or a==0):
		return a
	if (a%2==0):
		return (1 if (n%8==1 or n%8==7) else -1) * JacobiSymbol(a // 2, n)
	if (a%2==1 and n%2==1):
		if (a%4==3 and n%4==3):
			return -JacobiSymbol(n, a)
		return JacobiSymbol(n, a)

def LegendreSymbol(a, b):
	"""
		Returns Legendre symbol for a/b.
	"""
	if (MillerRabin(b)):
		return JacobiSymbol(a, b)
	return "2nd number is not prime"

def InverseElementInFieldByMod(a, p):
	"""
		Returns inverse element for a in field p using Euler's theorem( https://en.wikipedia.org/wiki/Euler%27s_theorem )
	"""
	return pow(a, PhiFastComputation(p) - 1, p)


def PollardAlgorithmForDiscreteLogarithms(a, b, p):
	"""
		Pollard's rho algorithm for logarithms for solving discrete logarithm problem
		Theory: https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm_for_logarithms
	"""
	u1 = 0
	u2 = 0
	v1 =0
	v2 =0
	z1 = 1
	z2 = 1
	pm1 = p-1
	pd3=(p//3)
	pd32=pd3*2
	def f(u, v, z):
		if (z<pd3):
			u+=1
			u = u % pm1
			z = (b*z)%p
		elif (pd32<z):
			v+=1
			v = v % pm1
			z = ( a * z) % p
		else:
			u = (u*2)%pm1
			v = (v*2)%pm1
			z = (z * z)%p
		return (u, v, z)
	u2, v2, z2 = f(u2, v2, z2)
	while True:
		u1, v1, z1= f(u1, v1, z1)
		u2, v2, z2 = f(u2, v2, z2)
		u2, v2, z2 = f(u2, v2, z2)
		if z1==z2:
			break
	du = u1 - u2
	dv = v2 - v1
	d = gcd(du, pm1)
	if (d==1):
		return ((dv%pm1) * InverseElementInFieldByMod(du % pm1, pm1)) % pm1
	pm1dd = pm1//d
	bmodp = b % p
	l = (( dv % pm1dd ) * InverseElementInFieldByMod(du % pm1dd, pm1dd)) % pm1dd
	for m in range(0, d+1):
		if (pow(a, l, p)==bmodp):
			return l
		l = (l+pm1dd)%pm1
	return "Solution has not been found"