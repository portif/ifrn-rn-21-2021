#!/usr/bin/env python3

from collections import defaultdict

texto = open('rn-21-2021.txt', 'r', encoding='utf-8').read()
linhas = texto.splitlines()

ini_cap = {}
for i,l in enumerate(linhas):
    if l.startswith('CAPÍTULO'):
        _,cap = l.split()
        ini_cap[int(cap)] = i

tit_cap = {cap:linhas[i+1] for cap,i in ini_cap.items()}
fim_cap = {c:ini_cap[c+1]-1 for c in range(1, 18)}
fim_cap[18] = -1

ini_art = {}
fim_art = {}
arts_cap = defaultdict(list)

for cap in range(1, 18+1):
    ini = ini_cap[cap]
    fim = fim_cap[cap]
    for i,l in enumerate(linhas[ini:fim], start=ini):
        if l.startswith('Art.'):
            _,art,_ = l.split(maxsplit=2)
            art = int(art.replace('º', '').replace('.', ''))
            ini_art[art] = i
            arts_cap[cap].append(art)
    for art in arts_cap[cap][:-1]:
        fim_art[art] = ini_art[art+1]
    fim_art[arts_cap[cap][-1]] = fim_cap[cap]

artigos = {}
for art in range(1, 46+1):
    ini = ini_art[art]
    fim = fim_art[art]
    conteudo = '\n'.join(linhas[ini:fim])
    artigos[art] = conteudo
    with open(f'art-{art}.md', mode='w', encoding='utf-8') as arq_art:
        arq_art.write(f'''\
(art-{art})=

# Artigo {art}

{conteudo}
''')

for cap in range(1, 18+1):
    with open(f'capitulo-{cap}.md', mode='w', encoding='utf-8') as arq_cap:
        arq_cap.write(f'''\
(cap-{cap})=

# Cap. {cap} -- {linhas[ini_cap[cap]+1].lower().capitalize()}

```{{toctree}}
''')
        for art in arts_cap[cap]:
            arq_cap.write(f'art-{art}.md\n')
        
        arq_cap.write('```')
