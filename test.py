import os

def is_sorted(filename):

    prevline = ''

    with open(filename) as infile:
        for line in infile:
            if line < prevline:
                return False
        return True


def test0():

    # very badly designed test, just for start and show usage
    # for bigdata test set strnum >= 10**8

    strnum = 100000000

    if os.path.exists('bigtext_test'):
        assert False
    
    if any([
        os.system("gcc gen.c -o gen"),
        os.system("./gen bigtext_test 50 %s && echo generated bigtext_test file" % strnum),
        os.system("python3 outersort.py bigtext_test"),
        ]):
        assert False

    assert is_sorted('bigtext_test')

    # we dont remove this file for your convinience to check
    # os.remove('bigtext_test') 
