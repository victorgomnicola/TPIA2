crs = open("C:/Users/Trevisan/Desktop/8 sem/Tópicos em Planejamento de Inteligencia Artificial/EP2/TestesGrid/DeterministicGoalState/navigation_1.net", "r")

curenty_action = ''
list_states = []
dict_actions = {}
initialstate = ''
goalstate = ''

session = [['states', 'endstates'], ['action', 'endaction'], ['cost', 'endcost'], ['initialstate', 'endinitialstate'], ['goalstate', 'endgoalstate']]
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
    			if curenty_session == session[0][0]: #states
    				list_states = columns.copy()

	    		elif curenty_session == session[1][0]: #action
	    			tupla = (curenty_action,columns[0],columns[1])
	    			dict_actions[tupla] = columns[2] 
	    		
	    		elif curenty_session == session[2][0]: #cost
    				#TO DO cost
    				cost = 1
    			
    			elif curenty_session == session[3][0]: #initialstate
    				initialstate = columns[0]
    			
    			elif curenty_session == session[4][0]: #goalstate
    				goalstate = columns[0]
    			
    			
#print(dict_actions)
print(type(dict_actions))