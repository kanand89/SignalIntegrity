from numpy import matrix
from numpy import diag
from numpy import sqrt

def Z0KHelper(Z0K,P):
    (Z0,K)=Z0K
    if Z0 is None:
        Z0=matrix(diag([50.0]*P))
    elif isinstance(Z0,list):
        Z0=matrix(diag([float(i.real)+float(i.imag)*1j for i in Z0]))
    elif isinstance(Z0,float) or isinstance(Z0,int):
        Z0=matrix(diag([float(Z0.real)+float(Z0.imag)*1j]*P))
    if K is None:
        K=sqrt(Z0)
    elif isinstance(K,list):
        K=matrix(diag([float(i.real)+float(i.imag)*1j for i in K]))
    elif isinstance(K,float) or isinstance(K,int):
        K=matrix(diag([float(K.real)+float(K.imag)*1j]*P))
    return (Z0,K)