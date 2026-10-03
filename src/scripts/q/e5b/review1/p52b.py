import glob, pandas as pd, numpy as np
from scipy import stats, optimize
d=glob.glob('/Users/<user>/aegis-builds/e5b-bixbench-lane/runs/data-2026-10-01/data/bix-52/CapsuleData-*')[0]
c=pd.read_csv(f'{d}/ZF_AgeRelated_CpG_noMT_Final.csv',dtype={'Chromosome':str})
ln=pd.read_csv(f'{d}/ZF_Chromosome_Length.csv',encoding='utf-8-sig',dtype={'Chromosome':str}).dropna(subset=['Length'])
ln=ln.set_index(ln.Chromosome.str.strip()).Length.astype(float)
x=(c.MethylationPercentage>90)|(c.MethylationPercentage<10)
fs=c[x].groupby('Chromosome').Pos.nunique()
print(fs.sort_values(ascending=False).head(8).to_dict(), 'total',fs.sum())
# notebook set: chromosomes with sites and a length (K2); plus variant adding 1A,4A with free length
for lo,hi in [(0.5,2),(0.25,4)]:
  for add in [False,True]:
    keys=[k for k in fs.index if k in ln.index]
    base=ln.reindex(keys).values
    O=fs.reindex(keys).values.astype(float)
    if add:
        keys=keys+['1A','4A']; O=np.append(O,[fs['1A'],fs['4A']]); base=np.append(base,[ln['1']*0.7, ln['4']*2])
    def f(t):
        L=base*np.exp(t); p=L/L.sum(); E=p*O.sum(); return ((O-E)**2/E).sum()
    b=[(np.log(lo),np.log(hi))]*len(O)
    if add: b[-2]=(np.log(0.01),np.log(10)); b[-1]=(np.log(0.01),np.log(10))
    r=optimize.minimize(f,np.zeros(len(O)),bounds=b,method='L-BFGS-B')
    print('lengths within x%.2f-x%.0f of table, add1A4A=%s: min chi2=%.1f (at table lengths %.1f)'%(lo,hi,add,r.fun,f(np.zeros(len(O)))))
