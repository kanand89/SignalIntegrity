import SignalIntegrity.Lib as si
from numpy import array
D=si.sd.SystemDescription()
D.AddDevice('D1',2)
D.AddDevice('D2',2)
D.ConnectDevicePort('D1',2,'D2',1)
D.AddPort('D1',1,1)
D.AddPort('D2',2,2)
SC=si.sd.SystemSParameters(D)
n=SC.NodeVector()
W=SC.WeightsMatrix()
m=SC.StimulusVector()
print('node vector:')
print(n)
print('weights matrix:')
print(array(W))
print('stimulus vector:')
print(m)
AN=SC.PortBNames()
BN=SC.PortANames()
print('AN:')
print(AN)
print('BN:')
print(BN)
XN=SC.OtherNames(AN+BN)
Wba=SC.WeightsMatrix(BN,AN)
Wbx=SC.WeightsMatrix(BN,XN)
Wxa=SC.WeightsMatrix(XN,AN)
Wxx=SC.WeightsMatrix(XN,XN)
print('Wba')
print(Wba)
print('Wbx')
print(Wbx)
print('Wxa')
print(Wxa)
print('Wxx')
print(Wxx)