import time
import random
import math


def get_minutos(hora):
    x = time.strptime(hora, '%H:%M')
    minutos = x[3] *60 + x[4]
    return minutos



# coisas que tem que levar em consideracao::

#  tempo de espera
#  custo extra, caso pegue voo tarde e tem que pagar uma diaria a mais do aluguel do carro
#  custo das passagens
#  duracao dos voos
#  combinar tudo em um unico valor
#  horario de saida
#  horario de chegada
    

#pesquisa randomica

def pesquisa_randomica(dominio, funcao_custo):
    melhor_custo = 999999999
    for i in range(0, 100):
        solucao = [random.randint(dominio[i][0], dominio[i][1]) for i in range(len(dominio))]
        custo = funcao_custo(solucao)
        if custo < melhor_custo:
            melhor_custo = custo
            melhor_solucao = solucao
    return melhor_solucao
        


#melhor encontrado = 3542 para a pesquisa randomica


#Hill Climb

def subida_encosta(dominio, funcao_custo):
    solucao = [random.randint(dominio[i][0], dominio[i][1]) for i in range(len(dominio))]
    while True:
        vizinhos = []
        
        for i in range(len(dominio)):
            if solucao[i] > dominio[i][0]:
                if solucao[i] != dominio[i][1]:
                    vizinhos.append(solucao[0:i] + [solucao[i] + 1] + solucao[i + 1:])
            if solucao[i] < dominio[i][1]:
                if solucao[i] != dominio[i][0]:
                    vizinhos.append(solucao[0:i] + [solucao[i] - 1] + solucao[i + 1:])
        atual = funcao_custo(solucao)
        melhor = atual
        for i in range(len(vizinhos)):
            custo = funcao_custo(vizinhos[i])
            if custo < melhor:
                melhor = custo
                solucao = vizinhos[i]
            
        if melhor == atual:
            break
    return solucao


                
#melhor encontrado = 3051 para o hill climb


#Têmpora(recozimento) Simulada (Simulated Annealing)

def tempera_simulada(dominio, funcao_custo, temperatura = 10000.0, resfriamento = 0.95, passo = 1):
    solucao = [random.randint(dominio[i][0], dominio[i][1]) for i in range(len(dominio))]
    
    while temperatura > 0.1:
        i = random.randint(0, len(dominio) - 1)
        direcao = random.randint(-passo, passo)
        
        solucao_temp = solucao[:]
        solucao_temp[i] +=direcao
        if solucao_temp[i] < dominio[i][0]:
            solucao_temp[i] = dominio[i][0]
        elif solucao_temp[i] > dominio[i][1]:
            solucao_temp[i] = dominio[i][1]
            
        custo_solucao = funcao_custo(solucao)
        custo_solucao_temp = funcao_custo(solucao_temp)
        probabilidade = pow(math.e, (-custo_solucao_temp - custo_solucao) / temperatura)
        
        if (custo_solucao_temp < custo_solucao or random.random() < probabilidade):
            solucao = solucao_temp
            
        temperatura = temperatura * resfriamento
        
    return solucao



#melhor encontrado = 3028 para o simulated Annealing


#Algoritmo Genetico

def mutacao(dominio, passo, solucao):
    i = random.randint(0, len(dominio) - 1)
    mutante = solucao
    
    if random.random() < 0.5:
        if solucao[i] != dominio[i][0]:
            mutante = solucao[0:i] + [solucao[i] - passo] + solucao[i+1:]
    else:
        if solucao[i] != dominio[i][1]:
            mutante = solucao[0:i] + [solucao[i] + passo] + solucao[i+1:]
    
    return mutante



def cruzamento(dominio, solucao1, solucao2):
    i = random.randint(1, len(dominio) - 2)
    return solucao1[0:i] + solucao2[i:]




def genetico(dominio, funcao_custo, tamanho_populacao = 50, passo = 1,
                probabilidade_mutacao = 0.2, elitismo = 0.2, numero_geracoes = 100):
    populacao = []
    for i in range(tamanho_populacao):
        solucao = [random.randint(dominio[i][0], dominio[i][1]) for i in range(len(dominio))]
        populacao.append(solucao)
        
    numero_elitismo = int(elitismo * tamanho_populacao)
    
    for i in range(numero_geracoes):
        custos = [(funcao_custo(individuo), individuo) for individuo in populacao]
        custos.sort()
        individuos_ordenados = [individuo for (custo, individuo) in custos]
        
        populacao = individuos_ordenados[0:numero_elitismo]
        
        while len(populacao) < tamanho_populacao:
            if random.random() < probabilidade_mutacao:
                m = random.randint(0, numero_elitismo)
                populacao.append(mutacao(dominio, passo, individuos_ordenados[m]))
            else:
                c1 = random.randint(0, numero_elitismo)
                c2 = random.randint(0, numero_elitismo)
                populacao.append(cruzamento(dominio, individuos_ordenados[c1], 
                                            individuos_ordenados[c2]))
                
    return custos[0][1]


