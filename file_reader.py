import math


class Read:

	#Attributes
	filename = ""

	#Path1 = {"section": 0, "population": 2500, "max_rate": 40, "edges":[{"begin":0,"end":1,"duedate":15,"length":8,"capacity":25}]}
	paths_list = []

	terminal_node = 0
	

	def __init__(self, filename):
		self.filename = filename

	def parse(self):
		
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
				edge = find_edge(path[i], path[i+1])
				path_temp["edges"].append({"begin":int(edge[0]),"end":int(edge[1]),"duedate":int(edge[2]),"length":int(float(edge[3])),"capacity":int(float(edge[4]))})
				
			self.paths_list.append(path_temp)

		
		
	def get_paths(self):
		return self.paths_list

	def get_safe_node(self):
		return self.terminal_node


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

if __name__ == '__main__':
	f = Read("dense_10_30_3_1.full")
	f.parse()
	f.lower_bound()
	#print(lb_rates)
	f.upper_bound()

	# out = open("out", "w")
	# out.write(str(f.get_safe_node())+"\n")
	# for p in f.get_paths():
	# 	out.write(str(p)+"\n")




