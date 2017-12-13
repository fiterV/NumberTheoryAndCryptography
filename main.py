from tools import *

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
    print("Legendre symbol = {}".format(JacobiSymbol(a, b)))

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
    print("Menu:")
    print("1) Mobius function")
    print("2) Miller-Rabin test")
    print("3) Pollard: factorization")
    print("4) Eulers function")
    print("5) Rsa scheme")
    print("6) Pollard: discrete logarithm")
    print("7) Legendre symbol")
    print("8) Jacobi symbol")

while True:
    Announcement()
    picker = int(input("Pick a number from menu ? = "))
    if picker<1 or picker>8:
        print("Wrong index. Please try again")
    else:
        if (picker==1):
            MobiusInput()
        elif (picker==2):
            PrimeTestInput()
        elif (picker==3):
            FactorizeInput()
        elif (picker==4):
            PhiInput()
        elif (picker==5):
            RSASCHEME()
        elif (picker==6):
            DisLogInput()
        elif (picker==7):
            LegendreInput()
        elif (picker==8):
            JacobiInput()