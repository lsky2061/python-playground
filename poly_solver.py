import math

def quad(a,b,c):
    # x = (1/2a)*-b pm sqrt(b^2 - 4ac)
    D = math.pow(b,2) -4*a*c
    if(D<0):
        print("Equation has two complex roots")
        print(f'x = {-b/(2*a)} +- i {math.sqrt(-D)/(2*a)}')
    elif (D==0):
        x = -b/(2*a)
        print(f"Equation has one real root: {x}")
    else:
        print("Equation has two real roots")
        x_1 = (1/(2*a))*(-b + math.sqrt(D))
        x_2 = (1/(2*a))*(-b - math.sqrt(D))
        print(f'x_1 = {x_1}')
        print(f'x_2 = {x_2}')





def cubic(a,b,c,d):
    Delta_0 = math.pow(b,2) -3*a*c
    Delta_1 = 2*math.pow(b,3) - 9*a*b*c + 27*math.pow(a,2)*d

    print(f"D_0 = {Delta_0}")
    print(f'D_1 = {Delta_1}')

    dis = math.pow(Delta_1,2) - 4*math.pow(Delta_0,3)
    if(dis < 0):
        print("imaginary solution. Implementation tbd")
        return "i";

    C_cubed = (Delta_1 + math.sqrt(dis))/2

    print(f'Under square root = {dis}')
    print(f'C^3 = {C_cubed}')

    C = 0
    if(C_cubed >= 0):
        C = math.pow(C_cubed, 1/3)
    else:
        C = -math.pow(-C_cubed,1/3)

    print(f'C = {C}')
    x_1 = (-1/3*a)*(b + C + (Delta_0/C))

    fx = a*math.pow(x_1,3) + b*math.pow(x_1,2) + c*x_1 + d
    print(f'Is {fx} = 0?')

    return  x_1
