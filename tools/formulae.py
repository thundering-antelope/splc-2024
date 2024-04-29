from z3 import *

def b2i(input_bool):
	return If(input_bool, 1, 0)

def i2b(input_int):
	return If(input_int > 0, True, False)

def i2b0(input_int):
	return If(input_int >= 0, True , False)

class Formula:
	def __init__(self, resource_type, get_Rd, Rp, get_Zr, I):
		self.r = tuple(resource_type)
		self.Rd = get_Rd
		self.Rp = Rp
		self.Zr = get_Zr
		self.I = I
	
	def nnil(self, value):
		_, _, p3 = self.r
		if (p3==1 and value.as_long() == sys.maxsize) or (p3!=1 and value.as_long() == 0):
			return False
		return True
	
	def zrn(self, i):
		return And(self.Zr(i), self.nnil(self.Rd(i)))

	def get_formula(self):
		return self.decideP2()

	def decideP2(self):
		_, p2, _ = self.r
		if p2: return And(
				self.decideP3(),
				Sum([self.zrn(i) for i in range(self.I)]) <= 1
			)
		else: return self.decideP3()

	def decideP3(self):
		_, _, p3 = self.r
		if p3 == 0: return self.decideP1(0)
		elif p3 == 1: return self.decideP1(1)
		else: return And(self.decideP1(0), self.decideP1(1))

	def decideP1(self, p3):
		Zr = self.Zr
		Rd = self.Rd
		Rp = self.Rp
		I = self.I
		p1, _, _ = self.r
		f = [[
				And([i2b0(Rp - Rd(i)*b2i(Zr(i))) for i in range(I)]), # ffL
				And([i2b0(Rd(i) - Rp*b2i(self.zrn(i))) for i in range(I)]) # ffU
			], [
				Sum([Rd(i) * b2i(Zr(i)) for i in range(I)]) 
					<= Rp, # tfL
				Sum([Rd(i) * b2i(self.zrn(i)) for i in range(I)])
					>= Rp * b2i(Or([self.zrn(i) for i in range(I)])) # tfU
			]]

		return f[p1][p3]