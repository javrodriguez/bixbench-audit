import pandas as pd, numpy as np
x=pd.read_csv('/Users/<user>/aegis-builds/e5b-bixbench-lane/runs/fits-2026-10-01/r1/bix-3_normcount.csv')
x=x.set_index('GeneID'); print(x.shape)
nc=x.T  # samples x genes
keep=nc.columns[nc.sum(axis=0)>=10]; ncc=nc[keep]
sc=(ncc*1e6/ncc.sum()).round().astype(int)
ctl=sc[sc.index.str.contains('Control')]
# median-of-ratios size factors
lg=np.log(ctl.replace(0,np.nan)); gm=lg.mean(axis=0); ok=gm.notna() & (ctl>0).all(axis=0)
sf=np.exp((lg.loc[:,ok]-gm[ok]).median(axis=1))
bm=(ctl.div(sf,axis=0)).mean(axis=0)
print('genes after filter',len(keep),'baseMean<10 in Control fit (approx):',int((bm<10).sum()),'min',bm.min().round(2),'median',bm.median().round(0))
# lane path: unscaled rounded counts
ctl0=nc[nc.index.str.contains('Control')].round()
print('lane path: genes with Control mean <10:', int((ctl0.mean(axis=0)<10).sum()), 'of', ctl0.shape[1])
