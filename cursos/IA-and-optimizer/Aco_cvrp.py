import math
import random
import time

# Utilizando uma matriz para feromonio e para distancias

pontos = []
capacity = []
pontos.append((float(0.0), float(0.0)))
capacity.append(int(0))
capacidade = 0

cont = 0
for linha in open('vrpc_locais.txt'):
    c = linha.split(' ')
    if c[0] == 'CAPACITY':
        capacidade = int(c[2])
    if (linha == 'NODE_COORD_SECTION\n' or linha == 'DEMAND_SECTION\n' or linha == 'DEPOT_SECTION\n'):
        cont += 1
        continue
    if cont == 1:
        ponto, _coordx, _coordy = linha.split(' ')
        pontos.append((float(_coordx), float(_coordy)))
    if cont == 2:
        ponto, _capacity = linha.split(' ')
        capacity.append(int(_capacity))
        
total = sum(capacity)
qtde = math.ceil(total/capacidade)
      

melhor_resp = []
#for linha in open('melhor_reduzido.txt'):
#for linha in open('locais_resp.txt'):
    #print(linha)
 #   _ponto = linha
 #   melhor_resp.append((int(_ponto)))

visit = []
mAdj = []
ferAdj = []
for i in range(len(pontos)):
    mAdj.append([0]*len(pontos))
    ferAdj.append([1]*len(pontos))
    
for i in range(1, len(pontos)):   
    for j in range(i+1, len(pontos)):
        _val = (math.sqrt((pontos[i][0]-pontos[j][0])**2 + (pontos[i][1]-pontos[j][1])**2))
        mAdj[i][j] = mAdj[j][i] = _val
        
def funcao_custo(solucao):
    custoFim = 0
    for j in solucao:
        custo = mAdj[j[-1]][j[0]]
        for i in range(len(j)-1):
            custo += mAdj[j[i]][j[i+1]]
        custoFim += custo
    return custoFim



def probabs(visit, vertice):
    dists = []
    fer = []
    pos = []
    for i in range(1, len(mAdj[vertice])):
        distancia = mAdj[vertice][i]
        if (visit[i] == 1):
            distancia = 0
        if distancia != 0:
            pos.append(i)
            dists.append(distancia)
            fer.append(ferAdj[vertice][i])
    
    atratividades = []
    for i in range(len(dists)):
        atract = fer[i] * (1/dists[i])
        atratividades.append(atract)
    
    soma = sum(atratividades)
    probs = []
    k = 0
    for i in atratividades:
        prob = (i/soma)
        probs.append((prob,pos[k]))
        k += 1
    return probs


def escolhaAresta(visit, vertice):
    
    probab = probabs(visit, vertice)
    limiares = []
    soma = 0
    for i in probab:
        soma += i[0]
        limiares.append(soma)
    r = random.random()
    
    cont = 0
    for i in limiares:
        if r > i:
            cont += 1
    
    if (len(probab) == 0):
        return -1
    else:
        return probab[cont][1]


def gera_formiga(inicio, cap):
    
    caminho = []
    visit = [0]*len(pontos)
    visit[inicio] = 1
    for i in range(qtde):
        caminho.append([inicio])
    
    k = 0
    while True:
        adj = caminho[k][-1]
        adj_random = escolhaAresta(visit, adj)
        if (adj_random == -1):
            break
        if (cap[k] + capacity[adj_random] > capacidade):
            k = (k + 1)%qtde
            continue
        cap[k] += capacity[adj_random]
        caminho[k].append(adj_random)
        visit[adj_random] = 1
        k = (k + 1)%qtde
    return caminho



def evaporacao(evap):
    for i in range(len(ferAdj)):
        for j in range(len(ferAdj)):
            ferAdj[i][j] = ferAdj[i][j]*(1-evap)
            
def atualiza_feromonio(formigas):
    for i in formigas:
        ferom = 1/funcao_custo(i)
        for k in i:
            j = 1
            while j < len(k):            
                ferAdj[k[j-1]][k[j]] += ferom
                j += 1
            ferAdj[k[j-1]][k[0]] += ferom
        
            

def aco_algorithm(x, evapora, qtdeFormigas, inicio, fim):
    for i in range(x):
        evaporacao(evapora)
        formigas = []
        for j in range(qtdeFormigas):
            cap = ([0]*qtde)
            formigas.append(gera_formiga(inicio, cap))
        atualiza_feromonio(formigas)
     
    soma = 923456789456123
    resp = []
    for i in formigas:
       custo = funcao_custo(i)
       if soma > custo:
           soma = custo
           resp = i
        
    return resp

#custo_melhor = funcao_custo(melhor_resp)
start = time.time()
solucao_aco_cvrp = aco_algorithm(200, 0.3, 20, 1, -1)
end = time.time()
custo_aco_cvrp = funcao_custo(solucao_aco_cvrp)
print(solucao_aco_cvrp) 
print(end - start)