import math
import random
from copy import deepcopy


class Read:

	# Attributes
	filename = ""

	# Path1 = {"section": 0, "population": 2500, "max_rate": 40, "edges":[{"begin":0,"end":1,"duedate":15,"length":8,"capacity":25}]}
	paths_list = []

	#edge = {"begin","end","duedate","length","capacity","use":[]}
	edge_list = []

	terminal_node = 0

	#Solution =[{'section': 1, 'rate': 8, 'begin': 0}, {'section': 2, 'rate': 5, 'begin': 27}, {'section': 3, 'rate': 3, 'begin': 54}]
	

	def __init__(self, filename):
		self.filename = filename
		self.paths_list = []
		self.edge_list = []

	def parse_data(self):
		
		def find_edge(i, j):
			for edge in parse_edges:
				if (edge[0]==i and edge[1]==j) or (edge[1]==i and edge[0]==j):
					return edge
			return("ERROR NOT FOUND")

		file = open(self.filename, "r")
		lines = file.readlines()		
		
		parse_paths = []
		parse_edges = []
		num_paths =0
		num_edges =0
		count = 0
		for l in lines:
			tmp = l.strip().split()
			if tmp[0] == "c":
				count += 1
			elif count == 1:
				if len(tmp)==2:
					num_paths = int(tmp[0])
					self.terminal_node = int(tmp[1])
				else:
					parse_paths.append(tmp)
			elif count == 2:
				if len(tmp)==2:
					num_edges = int(tmp[1])
				else:
					parse_edges.append(tmp)

		for path in parse_paths:
			path_temp = {"section": int(path[0]), "population": int(path[1]), "max_rate": int(path[2]), "edges":[]}
			
			for i in range(4, len(path)-1):
				tmp_edge = find_edge(path[i], path[i+1])
				edge = {"begin":int(tmp_edge[0]),"end":int(tmp_edge[1]),"duedate":int(tmp_edge[2]),"length":int(float(tmp_edge[3])),"capacity":int(float(tmp_edge[4])), "use":[]}
				if edge not in (self.edge_list):
					self.edge_list.append(edge)
				edge = {"begin":int(tmp_edge[0]),"end":int(tmp_edge[1]),"duedate":int(tmp_edge[2]),"length":int(float(tmp_edge[3])),"capacity":int(float(tmp_edge[4]))}
				path_temp["edges"].append(edge)
				
			self.paths_list.append(path_temp)

	@staticmethod
	def parse_sol(filename):
		f = open(filename, "r")
		lines = f.readlines()
		nb_sec = int(lines[1])
		lines = lines[2:nb_sec+2]
		

		sol = []
		for l in lines:
			tmp = l.strip().split()
			sol.append({'section':int(tmp[0]), 'rate':int(tmp[1]), 'begin':int(tmp[2])}) 
		

		return sol

	def check_sol(self, sol):

		def find_edge(i,j):
			for edge in self.edge_list:
				if (edge["begin"]==i and edge["end"]==j):
					return edge
			return("ERROR NOT FOUND")

		for edge in self.edge_list:
			edge["use"] = []

		paths = self.paths_list
		finish = self.terminal_node
		solution = sol
		pairs = []
		validity = "valid"
		last_edge = self.edge_list[0]
		global_max = max(last_edge["use"],key = lambda x : x[0], default = (0,0))

		for n in range(len(solution)):
			pairs.append({'solution': solution[n], 'path': paths[n]})

		for pair in pairs:		# For each path
			time = pair["solution"]["begin"]
			rate = pair["solution"]["rate"]
			num_groups = math.ceil(float(pair["path"]["population"]) / float(pair["solution"]["rate"]))
			last_group = pair["path"]["population"] % pair["solution"]["rate"]

			for n in pair["path"]["edges"]:			# For each edge in that path
				edge = find_edge(n["begin"],n["end"])
				edge["use"].append((time,rate))
				edge["use"].append((time+num_groups-1,(rate-last_group) * (-1)))
				edge["use"].append((time+num_groups,last_group * (-1)))
				length = edge["length"]
				time = time + length

		for edge in self.edge_list:				#For each edge used by the evacuation
			fill = 0
			edge["use"].sort(key = lambda x : x[0]) # Petite lambda-fonction
			local_max = max(edge["use"],key = lambda x : x[0], default = (0,0)) #Recuperer le temps auquel l'arc est complètement vidé

			for n in edge["use"]:				#For every event in that edge
				fill += n[1]	
				if (fill > edge["capacity"]):		
					validity = "invalid"
			if (local_max[0] > global_max[0]):
				global_max = local_max

		return validity,global_max[0]

			
		
	def get_paths(self):
		return self.paths_list

	def get_safe_node(self):
		return self.terminal_node

	def get_edges(self):
		return self.edge_list

	def lower_bound(self):
		# Pour chaque sommet d'évacuation faire comme s'il était seul à évacuer
		# Trouver le max rate en fonction de plus petit arc
		# Calculer le temps d'évacuation = max rate + longueur du path
		# Prendre le max des temps d'évacuations

		solutions = [0]* len(self.paths_list)
		length = [0]* len(self.paths_list)
		rates = [0]* len(self.paths_list)
		ct = 0

		for path in self.paths_list:
			#Find min rate & find length of path
			rates[ct] = path["max_rate"]

			for edge in path["edges"]:
				length[ct] += edge["length"]
				if rates[ct] > edge["capacity"]:
					rates[ct] = edge["capacity"]

			#Solution = Population/min capacity
			solutions[ct] = (math.ceil(float(path["population"])/float(rates[ct])))
			ct += 1


		#TODO Checker la solution

		#Ecriture de la solution
		output = open(self.filename.split(".")[0]+".lower","w")
		
		output.write(self.filename.split(".")[0]+"\n")
		output.write(str(len(self.paths_list))+"\n")

		for path in range(len(solutions)):
			output.write(str(self.paths_list[path]["section"])+" "+str(rates[path])+" 0\n")
		output.write("???\n"+str(max([x + y for x, y in zip(solutions, length)]))+"\n???")
		output.write("\nlower bound V1")

		return solutions

	def upper_bound(self):

		#Commencer par lower_bound
		#Faire passer les sommets dans l'ordre, commençant dès que le précédent estvcomplètement fini 
		solutions = [0]* len(self.paths_list)
		length = [0]* len(self.paths_list)
		rates = [0]* len(self.paths_list)
		ct = 0

		for path in self.paths_list:
			#Find min rate & find length of path
			rates[ct] = path["max_rate"]

			for edge in path["edges"]:
				length[ct] += edge["length"]
				if rates[ct] > edge["capacity"]:
					rates[ct] = edge["capacity"]

			#Solution = Population/min capacity
			solutions[ct] = (math.ceil(float(path["population"])/float(rates[ct])))
			ct += 1

		beg_time = [0]*(len(solutions))
		beg_time[0] = 0
		for i in range(1, len(solutions)):
			beg_time[i] = beg_time[i-1]+[x + y for x, y in zip(solutions, length)][i-1]


		#TODO Checker la solution
		#Ecriture de la solution
		output = open(self.filename.split(".")[0]+".upper","w")
		
		output.write(self.filename.split(".")[0]+"\n")
		output.write(str(len(self.paths_list))+"\n")

		for path in range(len(solutions)):
			output.write(str(self.paths_list[path]["section"])+" "+str(rates[path])+" "+str(beg_time[path])+"\n")
		output.write("???\n"+str(beg_time[-1]+solutions[-1]+length[-1])+"\n???")
		output.write("\nupper bound V1")

	@staticmethod
	def successors(sol):
		#For each section +/- 1 on rate and begin date
		succ = []

		for i in range(len(sol)):
			for val in [-1,1]:
				tmp1 = deepcopy(sol)
				tmp1[i]['begin'] += val 
				succ.append(tmp1)

				tmp2 = deepcopy(sol)
				tmp2[i]['rate'] += val
				succ.append(tmp2)
		return succ

	#TODO Test
	def hill_climbing(self, init_state):
		state = deepcopy(init_state)

		nb_it = 0
		while True:
			succs = Read.successors(state)
			nb_it+=1
			
			# Keep the best successor
			best_succ = succs[0]
			for s in succs:
				val_best = self.check_sol(best_succ)
				val_tmp = self.check_sol(s)

				if val_tmp[0] == "valid" and val_tmp[1] <= val_best[1]:
					val_best = deepcopy(val_tmp)

			# Check if the successor is valid and better than the current state
			val_state = self.check_sol(state)
			val_succ = self.check_sol(best_succ)
			if val_succ[0] == "valid" and val_succ[1] >= val_state[1]:
				return state, nb_it

			state = deepcopy(best_succ)

	def compress_sol(self, sol):
		cpt = 0
		for s in sol:
			print(cpt)
			cpt +=1
			val = 1
			while True:
				if s['begin'] - val > 0:
					s['begin'] -= val

				if self.check_sol(sol)[0] == "invalid":
					s['begin'] += val
					if val == 1:
						break
					val = 1
				else:
					val *= 2
		return sol

	def random_restart(self, nb_sol):
		#Identique à la borne sup
		solutions = [0]* len(self.paths_list)
		length = [0]* len(self.paths_list)
		rates = [0]* len(self.paths_list)
		ct = 0

		for path in self.paths_list:
			#Find min rate & find length of path
			rates[ct] = path["max_rate"]

			for edge in path["edges"]:
				length[ct] += edge["length"]
				if rates[ct] > edge["capacity"]:
					rates[ct] = edge["capacity"]

			#Solution = Population/min capacity
			solutions[ct] = (math.ceil(float(path["population"])/float(rates[ct])))
			ct += 1

		possible_sols = []
		for i in range(nb_sol):
			#Randomize state

			rdm = [x for x in range(len(self.paths_list))]
			random.shuffle(rdm)
			rdm_sol = [0]* len(solutions)
			rdm_length = [0]* len(length)
			rdm_rates = [0]* len(rates)

			for i in range(len(rdm)):
				rdm_sol[i] = solutions[rdm[i]]
				rdm_length[i] = length[rdm[i]]
				rdm_rates[i] = rates[rdm[i]]

			#Generate solution

			beg_time = [0]*(len(rdm_sol))
			beg_time[0] = 0
			for i in range(1, len(rdm_sol)):
				beg_time[i] = beg_time[i-1]+[x + y for x, y in zip(rdm_sol, rdm_length)][i-1]

			init_state = []
			for path in range(len(rdm_sol)):
				init_state.append({'section':self.paths_list[rdm[path]]["section"], 'rate':rdm_rates[path], 'begin':beg_time[path]})

			init_state = self.compress_sol(init_state)

			possible_sols.append(self.hill_climbing(init_state))

		best = None
		best_val = possible_sols[0][1]
		for sol in possible_sols:
			if sol[1] > best_val:
				best = sol
				best_val = sol[1]

		return best



if __name__ == '__main__':
	f = Read("dense_10_30_3_1_I.full")
	f.parse_data()

	f.upper_bound()
	f.lower_bound()
	print(f.check_sol(Read.parse_sol("dense_10_30_3_1_I.lower")))
	print(f.check_sol(Read.parse_sol("dense_10_30_3_1_I.upper")))

	print(Read.parse_sol("dense_10_30_3_1_I.upper"))
	print(f.hill_climbing(Read.parse_sol("dense_10_30_3_1_I.upper")))
	print(f.check_sol(f.hill_climbing(Read.parse_sol("dense_10_30_3_1_I.upper"))))

	# files = ["dense_10_30_3_1_I.full", "dense_10_30_3_2_I.full", "dense_10_30_3_3_I.full",
	# 		 "medium_10_30_3_1_I.full", "medium_10_30_3_2_I.full", "medium_10_30_3_3_I.full",
	# 		 "sparse_10_30_3_1_I.full", "sparse_10_30_3_2_I.full", "sparse_10_30_3_3_I.full"]
	#
	# for file in files:
	# 	f = Read(file)
	# 	f.parse_data()
	#
	# 	f.upper_bound()
	# 	f.lower_bound()
	# 	print(file)
	# 	print("Upper " + str(f.check_sol(Read.parse_sol(file.split(".")[0]+".upper"))))
	# 	print("Lower " + str(f.check_sol(Read.parse_sol(file.split(".")[0]+".lower"))))
	# 	print("\n")

	# for s in succ:
	# 	print(s)

	# out = open("out", "w")
	# out.write(str(f.get_safe_node())+"\n")
	# for p in f.get_paths():
	# 	out.write(str(p)+"\n")




