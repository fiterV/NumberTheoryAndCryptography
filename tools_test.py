from tools import *

def test_MillerRabin():
	assert MillerRabin(5) == 1
	assert MillerRabin(15) == 0
	assert MillerRabin(1231238210381203812031) == 1
	assert MillerRabin(102162237073053133567) == 1



def test_FastFactorizationUsingStack():
	assert FastFactorizationUsingStack(5) == {5:1}
	assert FastFactorizationUsingStack(1000000000000) == {2:12, 5:12}
	assert FastFactorizationUsingStack(1234567846153486513248) == {
		2:5,
		3:1,
		359:1,
		7393781:1,
		4844876347:1,
	}

def test_PhiFastComputation():
	assert PhiFastComputation(5) == 4
	assert PhiFastComputation(1231238210381203812031) == 1231238210381203812030
	assert PhiFastComputation(146513864351212222222) == 70420840241004504000

def test_MobiusFastComputation():
	assert MobiusFastComputation(1)==1
	assert MobiusFastComputation(146513864351212222222)==-1
	assert MobiusFastComputation(1465138643512122222)==0
	assert MobiusFastComputation(18)==0

def test_JacobiSymbol():
	assert JacobiSymbol(3, 5)==-1
	assert JacobiSymbol(14, 21)==0
	assert JacobiSymbol(3212133, 122231312115)==0
	assert JacobiSymbol(32121338, 122231312115)==-1
	assert JacobiSymbol(321214851313548653415311338, 1224865316854315153231312115)==1
	assert JacobiSymbol(3212148513135486534153113380, 1224865316854315153231312115)==0

def test_InverseElementInFieldByMod():
	assert InverseElementInFieldByMod(7, 18)==13
	assert InverseElementInFieldByMod(7213321213, 1821213231)==470021461
	assert InverseElementInFieldByMod(76123862138213321213, 36513826235816521386218136528)==12660939889295529791553442709

def test_PollardAlgorithmForDiscreteLogarithms():
	assert PollardAlgorithmForDiscreteLogarithms(2, 86120, 1000003)==3321
	assert PollardAlgorithmForDiscreteLogarithms(23268, 661477, 1000003)==33221
	assert PollardAlgorithmForDiscreteLogarithms(23268, 599113293, 1000000007)==123870410
	
