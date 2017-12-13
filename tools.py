from fractions import gcd
from math import sqrt
import random

def MillerRabin(n):
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
	d = FastFactorizationUsingStack(n)
	res = n
	for key in d:
		res*=key-1
		res//=key
	return res

def MobiusFastComputation(n):
	if n==1:
		return 1
	d = FastFactorizationUsingStack(n)
	for key in d:
		if (d[key]>=2):
			return 0
	return (1 if len(d.keys())%2==0 else -1)

def GetRandomPrime(l, r):
    while (not MillerRabin(l)):
        l+=1
    return l

def gcd_ex(a, b):
	if (a==0):
		return (0, 1)
	xx = gcd_ex(b%a, a)
	x = xx[1]-(b//a)*xx[0]
	y = xx[0]
	return (x, y)

def RSASCHEME():
	# 2 random prime numbers
	p = GetRandomPrime(random.randint(10**30, 10**35), 10**35)
	q = GetRandomPrime(random.randint(10**30, 10**35), 10**35)
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
	if (MillerRabin(b)):
		return JacobiSymbol(a, b)
	return "2nd number is not prime"

def InverseElementInCircleByMod(a, p):
	return pow(a, PhiFastComputation(p) - 1, p)


def PollardAlgorithmForDiscreteLogarithms(a, b, p):
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
		return ((dv%pm1) * InverseElementInCircleByMod(du % pm1, pm1)) % pm1
	pm1dd = pm1//d
	bmodp = b % p
	l = (( dv % pm1dd ) * InverseElementInCircleByMod(du % pm1dd, pm1dd)) % pm1dd
	for m in range(0, d+1):
		if (pow(a, l, p)==bmodp):
			return l
		l = (l+pm1dd)%pm1
	return "Solution has not been found"