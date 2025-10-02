
def knuth_arrows(a=1, num_arrows=1, b=1, debug=False):
    if debug:
        print("a",type(a))
        print("b", type(b))
        print("num_arrows",type(num_arrows))


    if (a< 0) | (b<0) | (num_arrows <-2):
        print("Out of Bounds!")
        return -1
    else:
        if num_arrows == -2:
            if debug: print("Entered return branch with ",num_arrows,"arrows")
            return a + num_arrows*b
        elif num_arrows == -1:
            if debug: print("Entered return branch with ", num_arrows, "arrows")
            return a + b
        elif num_arrows == 0:
            if debug: print("Entered return branch with ", num_arrows, "arrows")
            return a*b
        elif num_arrows == 1:
            if debug: print("Entered return branch with ", num_arrows, "arrows")
            return a**b
        elif num_arrows > 0 and b==0:
            if debug: print("Entered return branch with ", num_arrows, "arrows")
            return 1
        else:
            if debug: print("recursing with arrows:",num_arrows-1," and b=",b-1)
            return knuth_arrows(a, num_arrows - 1, knuth_arrows(a, num_arrows, b - 1))




print(knuth_arrows(4, 2, 4))