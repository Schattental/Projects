import math

def kreuz():
    print("Normalvektoren eingeben:")
    v1a = int(input("n1a = "))
    v1b = int(input("n1b = "))
    v1c = int(input("n1c = "))

    v2a = int(input("n2a = "))
    v2b = int(input("n2b = "))
    v2c = int(input("n2c = "))

    print(v1a, "   ", v2a)
    print(v1b, " X ", v2b)
    print(v1c, "   ", v2c)

    neg = -1

    vf1 = (v1b * v2c)-(v1c * v2b)
    vf2 = (v1a * v2c)-(v1c * v2a)
    vf3 = (v1a * v2b)-(v1b * v2a)
    print(vf1)
    print(vf2 * neg)
    print(vf3)



def dEP():
    Ex = int(input("Ex "))
    Ey = int(input("Ey "))
    Ez = int(input("Ez "))
    En = int(input("last number but already inside " ))
    Px = int(input("Px "))
    Py = int(input("Py "))
    Pz = int(input("Pz "))

    nx = int(input("nx "))
    ny = int(input("ny "))
    nz = int(input("nz "))

    n = math.sqrt((nx**2)+(ny**2)+(nz**2))

    E = (Ex*Px)+(Ey*Py)+(Ez*Pz) + En

    print("   ",E)
    print("-------")
    print("   ",n)
    #print(E/n)

kreuz()
