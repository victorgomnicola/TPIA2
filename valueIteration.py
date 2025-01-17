import sys
import numpy as np
from scipy.sparse import csr_matrix

def carrega_arquivo(nome_arquivo):
    crs = open(nome_arquivo, "r")
    curenty_action = ''
    list_states = []
    dict_actions = {}
    initial_state = ''
    goal_state = ''

    session = [['states', 'endstates'], ['action', 'endaction'], ['cost', 'endcost'], ['initial_state', 'endinitial_state'], ['goal_state', 'endgoal_state']]
    curenty_session = ''

    index_to_state = {}
    cont = 1

    for i in range(1, 21):
        for j in range(1, 21):
            state = 'robot-at-x{a}y{b}'.format(a = i, b=j)
            index_to_state[state] = cont
            cont+=1

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
                    matrix_move_south = csr_matrix((matrix_propabilities,(matrix_curenty_index_state, matrix_next_index_state)), shape=(40401, 40401))
                    matrix_cost_move_south = csr_matrix((matrix_cost,(matrix_curenty_index_state, matrix_next_index_state)), shape=(40401, 40401))
                    matrix_curenty_index_state = []
                    matrix_next_index_state = []
                    matrix_curenty_index_action = []
                    matrix_propabilities = []
                    matrix_cost = []

                elif curenty_action == 'move-north':
                    matrix_move_north = csr_matrix((matrix_propabilities,(matrix_curenty_index_state, matrix_next_index_state)), shape=(40401, 40401))
                    matrix_cost_move_north = csr_matrix((matrix_cost,(matrix_curenty_index_state, matrix_next_index_state)), shape=(40401, 40401))
                    matrix_curenty_index_state = []
                    matrix_next_index_state = []
                    matrix_curenty_index_action = []
                    matrix_propabilities = []
                    matrix_cost = []

                elif curenty_action == 'move-west':
                    matrix_move_west = csr_matrix((matrix_propabilities,(matrix_curenty_index_state, matrix_next_index_state)), shape=(40401, 40401))
                    matrix_cost_move_west = csr_matrix((matrix_cost,(matrix_curenty_index_state, matrix_next_index_state)), shape=(40401, 40401))
                    matrix_curenty_index_state = []
                    matrix_next_index_state = []
                    matrix_curenty_index_action = []
                    matrix_propabilities = []
                    matrix_cost = []

                elif curenty_action == 'move-east':
                    matrix_move_east = csr_matrix((matrix_propabilities,(matrix_curenty_index_state, matrix_next_index_state)), shape=(40401, 40401))
                    matrix_cost_move_east = csr_matrix((matrix_cost,(matrix_curenty_index_state, matrix_next_index_state)), shape=(40401, 40401))
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

            elif columns[0] == 'initial_state':
                curenty_session = session[3][0]

            elif columns[0] == session[3][1]:
                curent_action = ''

            elif columns[0] == 'goal_state':
                curenty_session = session[4][0]

            elif columns[0] == session[4][1]:
                curent_action = ''
                break


            else:
                if len(columns) > 0:
                    if curenty_session == session[0][0]: #states
                        list_states = columns.copy()

                    elif curenty_session == session[1][0]: #action

                        curenty_index_state = index_to_state[columns[0]]
                        next_index_state = index_to_state[columns[1]]
                        propabilities = columns[2]

                        matrix_curenty_index_state = np.append(matrix_curenty_index_state, int(curenty_index_state),axis=None)
                        matrix_next_index_state = np.append(matrix_next_index_state, int(next_index_state),axis=None)
                        matrix_propabilities = np.append(matrix_propabilities, float(propabilities),axis=None)
                        matrix_cost = np.append(matrix_cost, 1,axis=None)

                    elif curenty_session == session[2][0]: #cost
                        cost = 1

                    elif curenty_session == session[3][0]: #initial_state
                        initial_state = columns[0]

                    elif curenty_session == session[4][0]: #goal_state
                        goal_state = columns[0]


    matrix_probabilties = [matrix_move_south, matrix_move_north, matrix_move_west, matrix_move_east]
    matrix_costs = [matrix_cost_move_south, matrix_cost_move_north, matrix_cost_move_west, matrix_cost_move_east]
    return matrix_probabilties, matrix_costs, curenty_action, list_states, dict_actions, initial_state, goal_state

def valueIteration(matrix_probabilties, matrix_costs, initial_state, goal_state, list_states, ehpistola):
    A = len(matrix_probabilties)
    S = 441 #len(list_states)
    V = np.zeros(S) + sys.maxsize-1000
    num_iteracoes = 0
    meta = 400
    V[meta] = 0
    while True:
        Q = np.zeros((A, S))
        for a in range(A):
            for s in range(S):
                
                if matrix_probabilties[a][s].getnnz() != 0:
                    Q[a][s] = 1
                    for p in matrix_probabilties[a][s]:
                        data = p.data
                        indice = p.indices
                        for i in range(len(data)):
                            Q[a][s] += 0.5*data[i]*V[indice[i]]
                else:
                    Q[a][s] = 0
                #print('a', a, 's', s, 'q', Q[a][s])

        num_iteracoes += 1
        print(num_iteracoes)
       

        v_antigo = V.copy()
        
        for s in range(S):
            minimo = sys.maxsize
            for a in range(A):
                if Q[a][s] < minimo:
                    minimo = Q[a][s]
            V[s] = minimo
        print(max(abs(v_antigo-V)))
        if max(abs(v_antigo-V)) < ehpistola:
            break
        
    print(V)

nome_arquivo = "C:/Users/Avell/Documents/2019 - 02/TPIA/EP2/TPIA2/TestesGrid/DeterministicGoalState/navigation_1.net"

matrix_probabilties, matrix_costs, curenty_action, list_states, dict_actions, initial_state, goal_state = carrega_arquivo(nome_arquivo)

valueIteration(matrix_probabilties, matrix_costs, initial_state, goal_state, list_states, 0.1 )