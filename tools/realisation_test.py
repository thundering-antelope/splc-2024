from z3 import *
from file_utils import *
import formulae

class RealisationTester:
	def __init__(self, path_name, Rt, Rp, Rd):
		self.path_name = path_name
		self._set_resource_types(Rt)
		self._set_resource_provisionings(Rp)
		self._set_resource_demands(Rd)
		self._set_constraints()

	def _get_z3_value(self, value, resource_type):
		if value == -1:
			if resource_type[2] == 1: return IntVal(sys.maxsize) # p3=U
			else: return IntVal(0) # p3=L or p3=E
		else: return IntVal(value)

	def _set_resource_types(self, Rt):
		self.Rt = Rt
		self.K = len(self.Rt)
	
	def _set_resource_provisionings(self, Rp):
		J = len(Rp)
		for j in range(J):
			for k in range(self.K):
				Rp[j][k] = self._get_z3_value(Rp[j][k], self.Rt[k]) # init z3 type instances
		self.Rp = Rp
		self.J = J
	
	def _set_resource_demands(self, Rd):
		I = len(Rd)
		for i in range(I):
			for k in range(self.K):
				Rd[i][k] = self._get_z3_value(Rd[i][k], self.Rt[k]) # init z3 type instances
		self.Rd = Rd
		self.I = I
	
	def _set_constraints(self):
		I = self.I
		J = self.J
		K = self.K

		Zr = [[[
					Bool(f'z_{i}_{j}_{k}') for k in range(K)
				] for j in range(J)
			] for i in range(I)
		]

		# component assignments Z[i][j]
		Zc = [[
				Bool(f'z_{i}_{j}') for j in range(J)
			] for i in range(I)
		]

		s = Solver()

		# global constraints
		for i in range(I):
			for j in range(J):
				c = Zc[i][j] == And([Zr[i][j][k] for k in range(K)])
				s.add(c)

		# component assignment constraints
		for i in range(I):
			c = Sum([Zc[i][j] for j in range(J)]) == 1
			s.add(c)
		
		# resource constraints
		for j in range(J):
			for k in range(K):
				c = formulae.Formula(
					self.Rt[k], # resource_type
					lambda i: self.Rd[i][k], # get_Rd
					self.Rp[j][k], # Rp
					lambda i: Zr[i][j][k], # get_Zr
					I).get_formula()
				s.add(c)
		
		self.s = s
	
	def solve(self): return self.s.check() == sat