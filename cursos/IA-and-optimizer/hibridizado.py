# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 14:29:35 2022

@author: Vanessa
"""

# hibridizacao

import math
import random
import time


# Leitura dos arquivos
pontos = []
pontos.append((float(0.0), float(0.0)))
for linha in open('locais.txt'):
    #print(linha)
    _ponto, _coordx, _coordy = linha.split(' ')
    pontos.append((float(_coordx), float(_coordy)))
    
melhor_resp = []
for linha in open('locais_resp.txt'):
    #print(linha)
    _ponto = linha
    melhor_resp.append((int(_ponto)))


# Criacao da matriz de adjacencia
mAdj = []
ferAdj = []
for i in range(len(pontos)):
    mAdj.append([0]*len(pontos))
    ferAdj.append([1]*len(pontos))
    
for i in range(1, len(pontos)):   
    for j in range(i+1, len(pontos)):
        _val = (math.sqrt((pontos[i][0]-pontos[j][0])**2 + (pontos[i][1]-pontos[j][1])**2))
        mAdj[i][j] = mAdj[j][i] = _val
        
#Funcao de custo
def funcao_custo(solucao):
    custo = mAdj[solucao[-1]][solucao[0]]
    for i in range(len(solucao)-1):
        custo += mAdj[solucao[i]][solucao[i+1]]
    return custo



#Algorithm genetico -> mutacao
def mutacao(solucao):
    x = random.randint(1, len(solucao) - 2)
    y = random.randint(1, len(solucao) - 2)

    if (x == y):
        y += 1
        
    if (x > y):
        x, y = y, x
    
    mutante = solucao[0:x] + solucao[x:y][::-1] + solucao[y:]
    return mutante



# Algorithm ACO
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
    for i in range(len(ferAdj)):
        for j in range(len(ferAdj)):
            ferAdj[i][j] = ferAdj[i][j]*(1-evap)
            
def atualiza_feromonio(formigas):
    for i in formigas:
        ferom = 1/funcao_custo(i)
        j = 1
        while j < len(i):            
            ferAdj[i[j-1]][i[j]] += ferom
            j += 1






def hibridizado(funcao_custo, tamanho_populacao = 100, passo = 1
             , elitismo = 0.3, numero_geracoes = 200, inicio = 1, evapora = 0.3):
    populacao = []
    individuos_ordenados = []
    evaporacao(evapora)
    numero_elitismo = int(elitismo * tamanho_populacao)
    for i in range(numero_elitismo):
        individuos_ordenados.append(gera_formiga(inicio))
    atualiza_feromonio(populacao)
        
    
    
    for i in range(numero_geracoes):
        populacao = individuos_ordenados[0:numero_elitismo]
        
        while len(populacao) < tamanho_populacao:
            m = random.randint(0, numero_elitismo-1)
            populacao.append(mutacao(individuos_ordenados[m]))
            populacao.append(gera_formiga(inicio))
        atualiza_feromonio(populacao)
        evaporacao(evapora)
        custos = [(funcao_custo(individuo), individuo) for individuo in populacao]
        custos.sort()
        individuos_ordenados = [individuo for (custo, individuo) in custos]
        
        
        
    custos = [(funcao_custo(individuo), individuo) for individuo in populacao]
    custos.sort()
    
    return custos[0][1]



custo_melhor = funcao_custo(melhor_resp)
start = time.time()
solucao_hibrida_integrado = hibridizado(funcao_custo)
end = time.time()
custo_hibrida_integrado = funcao_custo(solucao_hibrida_integrado)
print(solucao_hibrida_integrado)   
print(end - start)

