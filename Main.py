entrada = """5 9
.n..T..n.
.T..n....
.n..#..n.
....n..T.
.n..T..n."""

linhas = entrada.strip().split('\n')
dimensoes = list(map(int, linhas[0].split()))
r, s = dimensoes[0], dimensoes[1]
mapa = linhas[1:]

for linha in mapa:
    print(linha)
