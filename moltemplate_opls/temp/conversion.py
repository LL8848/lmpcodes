

def Fourier2RB(Flist):
    # lammps standard opls style dihedral:
    # v_dihedral = f1*(1+cos(fi))/2 + f2*(1-cos(2fi))/2 + f3*(1+cos(3fi))/2
#     Flist = [f1,f2,f3,f4]
    [f1,f2,f3,f4] = Flist
    c0 = f2 + (f1+f3)/2.0
    c1 = 0.5 * (-1.0*f1+3*f3)
    c2 = -1.0*f2 + 4*f4
    c3 = -2 * f3

    return [c0,c1,c2,c3]


def Fourier2RB_Siu(Flist):
    # lopls paper by Siu et al. 2012
    # v_dihedral = f0 + f1*(1+cos(fi))/2 + f2*(1-cos(2fi))/2 + f3*(1+cos(3fi))/2
    #
    [f0,f1,f2,f3] = Flist
    c0 = 0.5*(f1+2*f2+f3)+f0
    c1 = -0.5*(f1-3*f3)
    c2 = -f2
    c3 = -2*f3

    return [c0,c1,c2,c3]


def RB2Fourier(RBlist):
    # convert RB dihedral form to lammps's opls standard form
    # RB: v_RB = c0 + c1*cos(fi) + c2*cos(fi)^2 + c3*cos(fi)^3
    [c0,c1,c2,c3] = RBlist

    f3 = -0.5*c3
    f2 = -c2
    f1 = -1.5*c3-2*c1

    return [f1,f2,f3,0]


def RB2Fourier_Siu(RBlist):
    # convert RB dihedral form to Siu 2012's opls form
    [c0,c1,c2,c3] = RBlist
    f3 = -0.5*c3
    f2 = -c2
    f1 = -1.5*c3-2*c1
    f0 = c0 - 0.5*(f1+2*f2+f3)
    
    return [f0,f1,f2,f3]
