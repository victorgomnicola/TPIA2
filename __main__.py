import pymdptoolbox.src.mdptoolbox.example as ex 
import pymdptoolbox.src.mdptoolbox.mdp as mdp


def carrega_arquivo(nome_arquivo):
	crs = open(nome_arquivo, "r")
	curenty_action = ''
	list_states = []
	dict_actions = {}
	initial_state = ''
	goal_state = ''

	session = [['states', 'endstates'], ['action', 'endaction'], ['cost', 'endcost'], ['initial_state', 'endinitial_state'], ['goal_state', 'endgoal_state']]
	curenty_session = ''

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
		    			tupla = (curenty_action,columns[0],columns[1])
		    			dict_actions[tupla] = columns[2] 
		    		
		    		elif curenty_session == session[2][0]: #cost
	    				#TO DO cost
	    				cost = 1
	    			
	    			elif curenty_session == session[3][0]: #initial_state
	    				initial_state = columns[0]
	    			
	    			elif curenty_session == session[4][0]: #goal_state
	    				goal_state = columns[0]
	return curenty_action, list_states, dict_actions, initial_state, goal_state


if __name__ == "__main__":

	nome_arquivo = "C:/Users/Avell/Documents/2019 - 02/TPIA/EP2/TPIA2/TestesGrid/DeterministicGoalState/navigation_1.net"

	curenty_action, list_states, dict_actions, initial_state, goal_state = carrega_arquivo(nome_arquivo)

	vi = mdp.ValueIteration(dict_actions, dict_actions, 0.96)
