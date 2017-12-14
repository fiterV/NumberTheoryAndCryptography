from tools import *

def test_MillerRabin():
	assert MillerRabin(5) == 1
	assert MillerRabin(15) == 0
	assert MillerRabin(1231238210381203812031) == 1
	assert MillerRabin(102162237073053133567) == 1