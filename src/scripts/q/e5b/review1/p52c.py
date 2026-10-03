import glob, pandas as pd, numpy as np
from scipy import stats, optimize
d=glob.glob('/Users/<user>/aegis-builds/e5b-bixbench-lane/runs/data-2026-10-01/data/bix-52/CapsuleData-*')[0]
c=pd.read_csv(f'{d}/ZF_AgeRelated_CpG_noMT_Final.csv',dtype={'Chromosome':str})
ln=pd.read_csv(f'{d}/ZF_Chromosome_Length.csv',encoding='utf-8-sig',dtype={'Chromosome':str}).dropna(subset=['Length'])
ln=ln.set_index(ln.Chromosome.str.strip()).Length.astype(float)
print(ln.sort_values(ascending=False).head(12).to_dict())
x=(c.MethylationPercentage>90)|(c.MethylationPercentage<10)
fs=c[x].groupby('Chromosome').Pos.nunique()
al=c.groupby('Chromosome').Pos.nunique()
keys=[k for k in fs.index if k in ln.index]
O=fs.reindex(keys).astype(float); L=ln.reindex(keys); E=L/L.sum()*O.sum()
contrib=((O-E)**2/E).sort_values(ascending=False)
print(pd.DataFrame({'O':O,'E':E.round(2),'contrib':contrib.round(1),'all_sites':al.reindex(keys)}).sort_values('contrib',ascending=False).head(8))
for scale4 in [1,4,8.6]:
    L2=L.copy(); L2['4']*=scale4; E2=L2/L2.sum()*O.sum()
    print('chr4 length x',scale4, 'chi2', round(((O-E2)**2/E2).sum(),1))
