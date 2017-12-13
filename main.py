from tools import *
from termcolor import colored


MENU_ERROR = colored("Wrong index. Please try again", 'red')
MENU=colored("""1) Mobius function
2) Eulers function
3) Legendre symbol
4) Jacobi symbol
5) Miller-Rabin test
6) Pollard: factorization
7) Rsa scheme
8) Pollard: discrete logarithm""", 'green')


def DisLogInput():
	p = input("P = ")
	a = input("A = ")
	b = input("B = ")
	p, a, b = (int(p), int(a), int(b))
	if (not MillerRabin(p)):
		print("First number is not prime")
		return
	ans = PollardAlgorithmForDiscreteLogarithms(a, b, p)
	print("Pollard for discrete logarithms")
	print("A = {} B = {} P = {}".format(a, b, p))
	print("Ans = ", ans)
	print("{0}^{1} % {3} = {2}".format(a, ans, pow(a, ans, p), p))

def PhiInput():
	a = int(input("N = "))
	print("Φ({}) = {}".format(a, PhiFastComputation(a)))

def MobiusInput():
	a = int(input("N = "))
	print("μ({}) = {}".format(a, MobiusFastComputation(a)))

def JacobiInput():
	a = int(input("A = "))
	b = int(input("B = "))

	print("Jacobi symbol = {}".format(JacobiSymbol(a, b)))

def LegendreInput():
    a = int(input("A = "))
    b = int(input("B = "))
    print("Legendre symbol = {}".format(LegendreSymbol(a, b)))

def PrimeTestInput():
	a = int(input("N = "))
	res = "{} is ".format(a)
	if not MillerRabin(a):
		res+="not "
	res+="prime"
	print(res)

def FactorizeInput():
	a = int(input("N = "))
	res = FastFactorizationUsingStack(a)
	before=0
	print("{} = ".format(a), end='')
	for key in sorted(res.keys()):
		for j in range(res[key]):
			if before:
				print("* ", end='')
			print("{} ".format(key), end='')
			before = 1
	print()

def Announcement():
    print(MENU)    
    
functions = [
	'MobiusInput', 
	'PhiInput', 
	'LegendreInput', 
	'JacobiInput',
	'PrimeTestInput',
	'FactorizeInput',
	'RSASCHEME',
	'DisLogInput',
]

while True:
    Announcement()
    picker = int(input("Pick a number from menu ? = "))
    if picker<1 or picker>8:
        print(MENU_ERROR)
    else:
    	globals()[functions[picker-1]]()