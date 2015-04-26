from numpy import matrix

def ShuntDeviceFourPort(D,DebugMode=None):
    D11=D[0][0]
    D12=D[0][1]
    D21=D[1][0]
    D22=D[1][1]
    DetD=D11*D22-D12*D21
    DN=-9.-3.*D11-3.*D22-DetD
    S=matrix([[3.-3.*D11+D22-DetD,-4.*D12,-6.-6.*D11-2.*D22-2*DetD,-4.*D12],
        [-4.*D21,3+D11-3.*D22-DetD,-4.*D21,-6.-2.*D11-6.*D22-2*DetD],
        [-6.-6.*D11-2.*D22-2.*DetD,-4.*D12,3.-3.*D11+D22-DetD,-4.*D12],
        [-4.*D21,-6.-2.*D11-6.*D22-2.*DetD,-4.*D21,3.+D11-3.*D22-DetD]])
    S=(S/DN).tolist()
    return S


