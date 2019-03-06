class s:
		def __init__(self, code):
			self.code = code
		def execute(self):
			exec(self.code)
			print(fitness([1,4,5,6,3,2,17,9]))


def execute(code):
	print(code)
	exec(code)
	print(fitness([1,4,5,6,3,2,17,9]))


code = """
def fitness(board):
		fitness = 0
		for i in range(len(board)):
			isSafe = True
			for j in range(len(board)):
				if i!=j:
					if (board[i] == board[j]) or (abs(board[i] - board[j]) == abs(i-j)):
						isSafe = False
						break
			if(isSafe==True):
				fitness += 1
		return fitness
"""

execute(code)

#exec(code)
#print(fitness([1,4,5,6,3,2,17,9]))

#t = s(code)
#t.execute()
