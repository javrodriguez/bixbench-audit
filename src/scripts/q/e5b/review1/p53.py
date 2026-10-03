import gzip,re,pandas as pd
A='/Users/<user>/aegis-builds/e5b-bixbench-lane/runs/data-2026-10-01/annot/'
gsh=None
for line in open(A+'KEGG_2019_Mouse.gmt'):
    p=line.rstrip('\n').split('\t')
    if p[0].strip().lower()=='glutathione metabolism': gsh={g.strip().upper() for g in p[2:] if g.strip()}
m={}
with gzip.open(A+'Mus_musculus.GRCm38.102.gtf.gz','rt') as f:
    for line in f:
        if line.startswith('#'): continue
        c=line.split('\t',9)
        if c[2]=='gene':
            nm=re.search(r'gene_name "([^"]+)"',c[8])
            if nm: m[re.search(r'gene_id "([^"]+)"',c[8]).group(1)]=nm.group(1).upper()
for xk in ['X4','X6']:
    t=pd.read_csv(f'/Users/<user>/aegis-builds/e5b-bixbench-lane/runs/fits-2026-10-01/r1/origin-bix53/bix-53-origin-{xk}.csv',na_values=['NA'],keep_default_na=False).set_index('gene')
    for pk in ['pvalue','padj']:
        for bm in ['>=','>']:
            s=t[t[pk].notna()&(t[pk]<0.05)&(t.lfc_apeglm.abs()>1)&((t.baseMean>=10) if bm=='>=' else (t.baseMean>10))]
            h={m[g] for g in s.index if g in m}&gsh
            print(xk,pk,'baseMean',bm,'10: sig',len(s),'overlap',len(h))
