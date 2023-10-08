import algoritmos_otmizacao as algo

dormitorios = ['Sao Paulo', 'Flamengo', 'Coritiba', 'Cruzeiro', 'Fortaleza']

preferencias = [('Amanda', ('Cruzeiro', 'Coritiba')),
                ('Pedro', ('Sao Paulo', 'Fortaleza')),
                ('Marcos', ('Flamengo', 'Sao Paulo')),
                ('Priscilla', ('Sao Paulo', 'Fortaleza')),
                ('Jessica', ('Flamengo', 'Cruzeiro')),
                ('Paulo', ('Coritiba', 'Fortaleza')),
                ('Fred', ('Fortaleza', 'Flamengo')),
                ('Suzana', ('Cruzeiro', 'Coritiba')),
                ('Laura', ('Cruzeiro', 'Coritiba')),
                ('Ricardo', ('Coritiba', 'Flamengo'))]
                
                
# (0,9), (0,8), (0,7), ..., (0,0)

dominio = [(0, (len(dormitorios) * 2) - i - 1) for i in range(0, len(dormitorios) * 2)]             
                
def imprimir_solucao(solucao):
    vagas = []
    for i in range(len(dormitorios)):
        vagas += [i, i]
    for i in range(len(solucao)):
        atual = solucao[i]
        dormitorio = dormitorios[vagas[atual]]
        print(preferencias[i][0], dormitorio)
        del vagas[atual]
                

imprimir_solucao([6, 1, 2, 1, 2, 0, 2, 2, 0, 0])
                
         
def funcao_custo(solucao):
    custo = 0
    vagas = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
    for i in range(len(solucao)):
        atual = solucao[i]
        dormitorio = dormitorios[vagas[atual]]
        preferencia = preferencias[i][1]
        if preferencia[0] == dormitorio:
            custo += 0
        elif preferencia[1] == dormitorio:
            custo += 1
        else:
            custo += 3
        del vagas[atual]
        
    return custo

funcao_custo([6, 1, 2, 1, 2, 0, 2, 2, 0, 0])


        
solucao_randomica = algo.pesquisa_randomica(dominio, funcao_custo)
custo_randomica = funcao_custo(solucao_randomica)
imprimir_solucao(solucao_randomica)        
        
solucao_hillclimb = algo.subida_encosta(dominio, funcao_custo)
custo_hillclimb = funcao_custo(solucao_hillclimb)
imprimir_solucao(solucao_hillclimb)   

solucao_tempera = algo.tempera_simulada(dominio, funcao_custo)
custo_tempera = funcao_custo(solucao_tempera)
imprimir_solucao(solucao_tempera)  

solucao_genetica = algo.genetico(dominio, funcao_custo)
custo_genetica = funcao_custo(solucao_genetica)
imprimir_solucao(solucao_genetica)         
        
        
        


