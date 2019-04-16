


class Read:

	#Attributes
	filename = ""

	#Path1 = {"section": 0, "population": 2500, "max_rate", 40, "edges":[{"begin":0,"end":1,"duedate":15,"length":8,"capacity":25}]}
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

if __name__ == '__main__':
	f = Read("test.full")
	f.parse()
	
	out = open("out", "w")
	out.write(str(f.get_safe_node())+"\n")
	for p in f.get_paths():
		out.write(str(p)+"\n")




