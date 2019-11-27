import sys
import numpy as np
from scipy.sparse import csr_matrix
import time

def carrega_arquivo(nome_arquivo,tamanhoGrid):
    crs = open(nome_arquivo, "r")
    curenty_action = ''
    list_states = []
    dict_actions = {}
    initial_state = ''
    goal_state = ''
    
    session = [['states', 'endstates'], ['action', 'endaction'], ['cost', 'endcost'],
               ['initialstate', 'endinitialstate'], ['goalstate', 'endgoalstate']]
    curenty_session = ''

    index_to_state = {}
    cont = 1
    
    
    M = np.zeros(tamanhoGrid*tamanhoGrid+1)
    tamanhoGrid = tamanhoGrid + 1
    for i in range(1, tamanhoGrid):
        for j in range(1, tamanhoGrid):
            state = 'robot-at-x{a}y{b}'.format(a=j, b=i)
            index_to_state[state] = cont
            M[cont] = tamanhoGrid-j + tamanhoGrid-i - 2
            cont += 1
            

    matrix_curenty_index_state = np.array([])
    matrix_next_index_state = np.array([])
    matrix_curenty_index_action = np.array([])
    matrix_propabilities = np.array([])
    matrix_cost = np.array([])

    matrix_move_south = []
    matrix_move_north = []
    matrix_move_west = []
    matrix_move_east = []

    matrix_cost_move_south = []
    matrix_cost_move_north = []
    matrix_cost_move_west = []
    matrix_cost_move_east = []

    for columns in (raw.strip().split() for raw in crs):
        if len(columns) != 0:

            if columns[0] == 'states':
                curenty_session = session[0][0]

            elif columns[0] == session[0][1]:
                curent_action = ''

            elif columns[0] == 'action':
                curenty_session = session[1][0]
                curenty_action = columns[1]

            elif columns[0] == session[1][1]:
                if curenty_action == 'move-south':
                    matrix_move_south = csr_matrix(
                        (matrix_propabilities, (matrix_curenty_index_state, matrix_next_index_state)),
                        shape=(tamanhoGrid * tamanhoGrid, tamanhoGrid * tamanhoGrid))
                    matrix_cost_move_south = csr_matrix(
                        (matrix_cost, (matrix_curenty_index_state, matrix_next_index_state)), shape=(tamanhoGrid*tamanhoGrid, tamanhoGrid*tamanhoGrid))
                    matrix_curenty_index_state = []
                    matrix_next_index_state = []
                    matrix_curenty_index_action = []
                    matrix_propabilities = []
                    matrix_cost = []

                elif curenty_action == 'move-north':
                    matrix_move_north = csr_matrix(
                        (matrix_propabilities, (matrix_curenty_index_state, matrix_next_index_state)),
                        shape=(tamanhoGrid * tamanhoGrid, tamanhoGrid * tamanhoGrid))
                    matrix_cost_move_north = csr_matrix(
                        (matrix_cost, (matrix_curenty_index_state, matrix_next_index_state)),  shape=(tamanhoGrid*tamanhoGrid, tamanhoGrid*tamanhoGrid))
                    matrix_curenty_index_state = []
                    matrix_next_index_state = []
                    matrix_curenty_index_action = []
                    matrix_propabilities = []
                    matrix_cost = []

                elif curenty_action == 'move-west':
                    matrix_move_west = csr_matrix(
                        (matrix_propabilities, (matrix_curenty_index_state, matrix_next_index_state)),
                        shape=(tamanhoGrid * tamanhoGrid, tamanhoGrid * tamanhoGrid))
                    matrix_cost_move_west = csr_matrix(
                        (matrix_cost, (matrix_curenty_index_state, matrix_next_index_state)),  shape=(tamanhoGrid*tamanhoGrid, tamanhoGrid*tamanhoGrid))
                    matrix_curenty_index_state = []
                    matrix_next_index_state = []
                    matrix_curenty_index_action = []
                    matrix_propabilities = []
                    matrix_cost = []

                elif curenty_action == 'move-east':
                    matrix_move_east = csr_matrix(
                        (matrix_propabilities, (matrix_curenty_index_state, matrix_next_index_state)),
                        shape=(tamanhoGrid * tamanhoGrid, tamanhoGrid * tamanhoGrid))
                    matrix_cost_move_east = csr_matrix(
                        (matrix_cost, (matrix_curenty_index_state, matrix_next_index_state)),  shape=(tamanhoGrid*tamanhoGrid, tamanhoGrid*tamanhoGrid))
                    matrix_curenty_index_state = []
                    matrix_next_index_state = []
                    matrix_curenty_index_action = []
                    matrix_propabilities = []
                    matrix_cost = []

                curent_action = ''

            elif columns[0] == 'cost':
                curenty_session = session[2][0]

            elif columns[0] == session[2][1]:
                curent_action = ''

            elif columns[0] == 'initialstate':
                curenty_session = session[3][0]

            elif columns[0] == session[3][1]:
                curent_action = ''

            elif columns[0] == 'goalstate':
                curenty_session = session[4][0]

            elif columns[0] == session[4][1]:
                curent_action = ''
                break


            else:
                if len(columns) > 0:
                    if curenty_session == session[0][0]:  # states
                        list_states = []
                        for a in columns:
                            replaced_state = a.replace(',','')
                            

                            list_states.append(index_to_state[replaced_state])

                    elif curenty_session == session[1][0]:  # action
                        
                        curenty_index_state = index_to_state[columns[0]]
                        next_index_state = index_to_state[columns[1]]
                        propabilities = columns[2]

                        matrix_curenty_index_state = np.append(matrix_curenty_index_state, int(curenty_index_state),
                                                               axis=None)
                        matrix_next_index_state = np.append(matrix_next_index_state, int(next_index_state), axis=None)
                        matrix_propabilities = np.append(matrix_propabilities, float(propabilities), axis=None)
                        matrix_cost = np.append(matrix_cost, 1, axis=None)

                    elif curenty_session == session[2][0]:  # cost
                        cost = 1

                    elif curenty_session == session[3][0]:  # initial_state
                        initial_state = index_to_state[columns[0]]

                    elif curenty_session == session[4][0]:  # goal_state
                        goal_state = index_to_state[columns[0]]
                    
    matrix_probabilties = [matrix_move_south, matrix_move_north, matrix_move_west, matrix_move_east]
    matrix_costs = [matrix_cost_move_south, matrix_cost_move_north, matrix_cost_move_west, matrix_cost_move_east]
    
    for s in range(len(M)):
        if M[s] not in list_states:
            M[s] = sys.maxsize - 1000
    return matrix_probabilties, matrix_costs, curenty_action, list_states, dict_actions, initial_state, goal_state, M



def valueIteration(matrix_probabilties, list_states, goal_state, numStates, ehpistola, V):
    
    A = len(matrix_probabilties)
    S = numStates
   
    num_iteracoes = 0
    meta = goal_state
    V[meta] = 0
    while True:
        Q = np.zeros((A, S))
        for a in range(A):
            for s in list_states:

                if matrix_probabilties[a][s].getnnz() != 0:
                    if s != meta:
                        Q[a][s] = 1
                    for p in matrix_probabilties[a][s]:
                        data = p.data
                        indice = p.indices
                        for i in range(len(data)):
                            Q[a][s] += 0.99 * data[i] * V[indice[i]]
                else:
                    Q[a][s] = sys.maxsize - 1000

        num_iteracoes += 1

        v_antigo = V.copy()

        for s in range(S):
            minimo = sys.maxsize
            for a in range(A):
                if Q[a][s] < minimo:
                    minimo = Q[a][s]
            V[s] = minimo
        if max(abs(v_antigo - V)) < ehpistola:
            break
    return V, num_iteracoes


def melhorS(F, Gv, V):
	Fv = []
	for estado in F:
	    if estado in Gv:
	        Fv.append(estado)
	if len(Fv): return Fv[np.argmin(V[Fv])]
	else: return None


#essa funcao encontra os sucessores de n e adiciona-os a G1
#e retorna a lista de sucessores
def expandPartialSolution(G, G1, s, V, goal_state):
    lista_sucessores = []
    A = 4
    
    for a in range(A):
        if G[a][s].getnnz() != 0:
            for p in G[a][s]:
                indice = p.indices
                for i in range(len(indice)):
                    if indice[i] not in lista_sucessores and indice[i] not in G1:
                        lista_sucessores.append(indice[i])
                        G1.append(indice[i])

    return lista_sucessores


def achievableStates(G,G1,s):
    GT = [G[x].transpose(copy=True) for x in range(4)]
    result = []
    
    result.append(s)
    
    resultCopy = result.copy()
    
    while len(resultCopy)!=0 :
        
        sLinha = resultCopy.pop()
        
        for aa in range(4):
            for states in GT[aa].getrow(sLinha):
                for state in states.indices:
                    if state not in result and state in G1:
                        result.append(state)
                        resultCopy.append(state)
                    
    return result




def rebuildGv(G, G1, V, initial_state):
    Gv_novo = [initial_state]
    melhor_estado = initial_state
    while True:
        estados_alcancaveis = []
        acao_estado = []
        for a in range(4):
            if G[a][melhor_estado].getnnz() != 0:
                for p in G[a][melhor_estado]:
                    indice = p.indices
                    for i in range(len(indice)):
                        if indice[i] in G1 and indice[i] not in estados_alcancaveis and indice[i] not in Gv_novo:
                            estados_alcancaveis.append(indice[i])
                            acao_estado.append(a)

        if len(estados_alcancaveis) == 0:
            break
            
        estado_atual = melhor_estado
        melhor_estado = estados_alcancaveis[np.argmin(V[estados_alcancaveis])]
        
        acao_melhor_estado = acao_estado[np.argmin(V[estados_alcancaveis])]
       
        for p in G[acao_melhor_estado][estado_atual]:
            indice = p.indices
            for i in range(len(indice)):
                if indice[i] not in Gv_novo:
                    Gv_novo.append(indice[i])
    return Gv_novo


def retorna_politica(G, grafo_otimo, V):
    politica = []
    
    for estado in grafo_otimo:
        estados_alcancaveis = []
        acao_estado = []
        for a in range(4):
            if G[a][estado].getnnz() != 0:
                for p in G[a][estado]:
                    indice = p.indices
                    for i in range(len(indice)):
                        if indice[i] not in estados_alcancaveis:
                            estados_alcancaveis.append(indice[i])
                            acao_estado.append(a)
                        

        acao_melhor_estado = acao_estado[np.argmin(V[estados_alcancaveis])]
        
        politica.append((estado, acao_melhor_estado))

    return politica
    

def onde_esta_o_LAO(G, M, initial_state, goal_state, numStates):
    V = M.copy()
    F = [initial_state]
    I = []
    G1 = [initial_state]
    Gv = [initial_state]
    
    cont = 0
    while True:
        
        cont += 1

        s = melhorS(F, Gv, V)

        if not s:
            break

        lista_sucessores = expandPartialSolution(G, G1, s, V, goal_state)        

        F.remove(s)
        
        for sucessor in lista_sucessores:
            if sucessor not in F:
                F.append(sucessor)
                
        I.append(s)
        
        Z = achievableStates(G, G1, s)
        
        V, iteracoes = valueIteration(G, Z, goal_state, numStates, 0.01, V)

        Gv = rebuildGv(G, G1, V, initial_state)
        
        
    politica = retorna_politica(G, Gv, V)
    return politica, cont, V


def rodaTudo(algoritmo, problemas, det):
	
	current_milli_time = lambda: int(round(time.time() * 1000))
	list_tamGrid = np.zeros(len(problemas))

	div_arquivo = ''
	for i in range(len(problemas)):
		list_tamGrid[i] = int(problemas[i]*20)
		div_arquivo += str(problemas[i]) + '_'

	

	if det == 0:
		d = 'DeterministicGoalState'
	else:
		d = 'RandomGoalState'

	resp = ''
	cont = 0
	if algoritmo == 0: alg = 'It_value'
	else: alg = 'LAO'
	f = open("resp" + alg + "_" + str(div_arquivo) + d + ".txt", "a")
	try:
		f.write("Inicio dos resultados\n")

		for problema in problemas:
			print('Iniciando problema ' + str(problema) +  ' - '  + d + ' - ' + alg)
			tamGrid = int(list_tamGrid[cont])
			cont += 1
			nome_arquivo = "TestesGrid/" + d + "/navigation_" + str(problema) + ".net"

			G, matrix_costs, curenty_action, list_states, dict_actions, initial_state, goal_state, M = carrega_arquivo(nome_arquivo, tamGrid)
			S = tamGrid*tamGrid + 1
			
			f.write('\n\n******************** PROBLEMA ' + str(problema) +  ' - ' + d + ' - ' + alg + ' *********************\n')
			value = []
			iteracoes = 0
			if algoritmo == 0:
				value = np.zeros(S) + sys.maxsize - 1000
				t = current_milli_time()
				value, iteracoes = valueIteration(G, list_states, goal_state, S, 0.01, value)
				
				politica = retorna_politica(G, list_states, value)
				t = current_milli_time() - t
			else:
				t = current_milli_time()

				politica, iteracoes, value = onde_esta_o_LAO(G, M, initial_state, goal_state, S)
				t = current_milli_time() - t
				lista_estados = []

				for el in politica:
				    lista_estados.append(el[0])

				for i in range(tamGrid, 0, -1):
				    for j in range(1, tamGrid + 1):
				        estado = (i-1)*tamGrid  + (j-1) + 1
				        if  estado in lista_estados:
				            f.write('x ')
				        elif estado in list_states:
				            f.write('1 ')
				        else:
				            f.write('0 ')
				    f.write('\n')



			f.write('\n******************** Politica ' + str(problema) +  ' - '  + d + ' - ' + alg + ' *********************\n')
			for tupla in politica:
				f.write(str(tupla) + '\n')
			f.write('\n******************** Valor ' + str(problema) +  ' - '  + d + ' - ' + alg + ' *********************\n')
			
			for v_estado in range(1, len(value)):
				f.write(str(v_estado) + ': ' + str(value[v_estado]) + '\n')
			f.write('\n******************** Tempo ' + str(problema) +  ' - '  + d + ' - ' + alg + ' *********************\n')
			f.write(str(t) + ' milissegundos\n')
			f.write(str(iteracoes) + ' iteracoes\n')

			print('Problema ' + str(problema) +  ' - '  + d + ' - ' + alg + 'concluido')
	except Exception as e:
		print("\nDeu ruim\n")
		f.write(str(e) + "\n")

	finally:
		f.close()
	

if __name__ == '__main__':
	
    problemas = [3]
    rodaTudo(1, problemas, 0)
    print('Acabou! :)')
