import math
import random
from copy import deepcopy

pontos = []
pontos.append((float(0.0), float(0.0)))
#for linha in open('locais_reduzido.txt'):
for linha in open('locais.txt'):
    #print(linha)
    _ponto, _coordx, _coordy = linha.split(' ')
    pontos.append((float(_coordx), float(_coordy)))
    
melhor_resp = []
#for linha in open('melhor_reduzido.txt'):
for linha in open('locais_resp.txt'):
    #print(linha)
    _ponto = linha
    melhor_resp.append((int(_ponto)))

visit = []
mAdj = []
for i in range(len(pontos)):
    mAdj.append([(0,1)]*len(pontos))
    
for i in range(1, len(pontos)):   
    for j in range(i+1, len(pontos)):
        _val = (math.sqrt((pontos[i][0]-pontos[j][0])**2 + (pontos[i][1]-pontos[j][1])**2))
        mAdj[i][j] = mAdj[j][i] = (_val, 1)
        
def funcao_custo(solucao):
    custo = mAdj[solucao[-1]][solucao[0]][0]
    for i in range(len(solucao)-1):
        custo += mAdj[solucao[i]][solucao[i+1]][0]
    return custo


def probabs(visit, vertice):
    arestas = mAdj[vertice]
    dists = []
    fer = []
    pos = []
    k = 0
    for i in arestas:
        distancia = i[0]
        if (visit[k] == 1):
            distancia = 0
        if distancia != 0:
            pos.append(k)
            dists.append(distancia)
            fer.append(i[1])
        k += 1
    
    atratividades = []
    cont = 0
    while cont < len(dists):
        atract = fer[cont] * (1/dists[cont])
        atratividades.append(atract)
        cont += 1
    
    soma = sum(atratividades)
    probs = []
    k = 0
    for i in atratividades:
        prob = (i/soma)*100
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
    r = random.random() * 100
    
    cont = 0
    for i in limiares:
        if r > i:
            cont += 1
    
    if (len(probab) == 0):
        return -1
    else:
        return probab[cont][1]


def gera_formiga(inicio):
    
    caminho = [inicio]
    visit = [0]*len(pontos)
    visit[inicio] = 1
    
    for i in caminho:
        adj = caminho[-1]
        adj_random = escolhaAresta(visit, adj)
        if (adj_random == -1):
            break
        caminho.append(adj_random)
        visit[adj_random] = 1
    return caminho



def evaporacao(evap):
    for i in range(len(mAdj)):
        for j in range(len(mAdj)):
            mAdj[i][j] = (mAdj[i][j][0], mAdj[i][j][1]*(1-evap))
            
def atualiza_feromonio(formigas):
    for i in formigas:
        ferom = 1/funcao_custo(i)
        j = 1
        while j < len(i):            
            mAdj[i[j-1]][i[j]] = (mAdj[i[j-1]][i[j]][0], mAdj[i[j-1]][i[j]][1] + ferom)
            j += 1
        
            

def aco_algorithm(x, evapora, qtdeFormigas, inicio, fim):
    for i in range(x):
        evaporacao(evapora)
        formigas = []
        for j in range(qtdeFormigas):
            formigas.append(gera_formiga(inicio))
        atualiza_feromonio(formigas)
     
    soma = 123456789
    resp = []
    for i in formigas:
       custo = funcao_custo(i)
       if soma > custo:
           soma = custo
           resp = i
        
    return resp

custo_melhor = funcao_custo(melhor_resp)
solucao_aco = aco_algorithm(200, 0.3, 50, 1, -1)
custo_aco = funcao_custo(solucao_aco)
print(custo_melhor)
print(custo_aco)
print(solucao_aco) 
print(len(solucao_aco))  