import glob, pandas as pd, numpy as np
from scipy import stats
d=glob.glob('/Users/<user>/aegis-builds/e5b-bixbench-lane/runs/data-2026-10-01/data/bix-52/CapsuleData-*')[0]
for sp in ['ZF','JD']:
    c=pd.read_csv(f'{d}/{sp}_AgeRelated_CpG_noMT_Final.csv',dtype={'Chromosome':str})
    ln=pd.read_csv(f'{d}/{sp}_Chromosome_Length.csv',encoding='utf-8-sig',dtype={'Chromosome':str}).dropna(subset=['Length'])
    ln=ln.set_index(ln.Chromosome.str.strip()).Length.astype(float)
    x=(c.MethylationPercentage>90)|(c.MethylationPercentage<10)
    print(sp,'rows',len(c),'sites',c.Pos.nunique(),'filtered rows',x.sum(),'filtered sites',c.loc[x,'Pos'].nunique(), 'samples',c.Sample.nunique())
    fs=c[x].groupby('Chromosome').Pos.nunique(); al=c.groupby('Chromosome').Pos.nunique()
    nf=al-fs.reindex(al.index,fill_value=0)
    tab=pd.DataFrame({'f':fs.reindex(al.index,fill_value=0),'nf':nf})
    tab2=tab[tab.sum(1)>0]
    print(' contingency filtered vs not (all chroms)',stats.chi2_contingency(tab2.T.values,correction=False)[0])
    t3=tab2[tab2.index.isin(ln.index)]
    print(' contingency, length-table chroms',stats.chi2_contingency(t3.T.values,correction=False)[0])
    # per-sample site counts: mean per sample rows filtered by chromosome
    for col in ['Sample']:
        ps=c[x].groupby('Chromosome').size()/c.Sample.nunique()
        k=ps[ps.index.isin(ln.index)]; e=ln.reindex(k.index); e=e/e.sum()*k.sum()
        print(' mean-per-sample filtered rows, length-prop K2',stats.chisquare(k,e)[0])
    # equal expected across chromosomes with sites (K2 E2) distinct filtered
    k=fs[fs.index.isin(ln.index)]
    print(' K2 E2 distinct',stats.chisquare(k)[0], 'K3 E2', stats.chisquare(fs)[0])
    # all chromosomes in length table incl zeros, length-prop, distinct
    k=fs.reindex([i for i in ln.index if i.upper()!='MT'],fill_value=0); e=ln.reindex(k.index); e=e/e.sum()*k.sum()
    print(' K1 E1 distinct',stats.chisquare(k,e)[0])
    # filter on site mean
    m=c.groupby('Pos').agg(ch=('Chromosome','first'),m=('MethylationPercentage','mean'),md=('MethylationPercentage','median'))
    print(' sites mean extreme', ((m.m>90)|(m.m<10)).sum(), 'median extreme',((m.md>90)|(m.md<10)).sum())
    # chromosomes missing
    print(' data chroms not in length table', sorted(set(c.Chromosome)-set(ln.index)), 'filtered sites there', fs[~fs.index.isin(ln.index)].to_dict())
