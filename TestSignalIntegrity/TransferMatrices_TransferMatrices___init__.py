class TransferMatrices(object):
    def __init__(self,f,d):
        self.f=FrequencyList(f)
        self.Matrices=d
        self.Inputs=len(d[0][0])
        self.Outputs=len(d[0])
...
    def __len__(self):
        return len(self.f)
    def __getitem__(self,item):
        return self.Matrices[item]
    def FrequencyResponse(self,o,i):
        return FrequencyResponse(self.f,[Matrix[o-1][i-1]
            for Matrix in self.Matrices])
    def FrequencyResponses(self):
        return [[self.FrequencyResponse(o+1,s+1)
            for s in range(self.Inputs)] for o in range(self.Outputs)]
    def ImpulseResponses(self,td=None):
        fr = self.FrequencyResponses()
        if td is None or isinstance(td,float) or isinstance(td,int):
            td = [td for m in range(len(fr[0]))]
        return [[fro[m].ImpulseResponse(td[m]) for m in range(len(fro))]
            for fro in fr]
