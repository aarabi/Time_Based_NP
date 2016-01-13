class offgrid(object):
	def __init__(self):
		self.pvLifetime=4
		self.pvPanelCostPerKW=800
		self.minSysPVCap=0.05
		self.efficiencyLoss=0.5
		self.peakSunHours=1320
		self.MainCostFracTotalCost=0.05
		self.BalCostFracTotalCost=1.5
		self.PvBatteryCostperKWH=150
		self.PVBatteryKWHperKW=8
		self.batteryLifetime=4
		self.balanceLifetime=4
		self.timePeriod=30
		self.interestRate=0.15
	# PV comp Recurring cost 
	def calCapPV(self,NodalDemand):
		return (NodalDemand/((1-self.efficiencyLoss)*self.peakSunHours))
	def pvPanelActualCap(self,NodalDemand):
		return max(self.minSysPVCap,self.calCapPV(NodalDemand))
	def pvPanelCost(self,NodalDemand):
		return self.pvPanelActualCap(NodalDemand)*self.pvPanelCostPerKW
	def pvrecurrCost(self,NodalDemand):
		return (self.pvPanelCost(NodalDemand)/self.pvLifetime)

	
	# Photovoltaics com Operations and Maintenance cost per year
	def batteryCost(self,NodalDemand):
		return self.pvPanelActualCap(NodalDemand)*self.PvBatteryCostperKWH*self.PVBatteryKWHperKW
	def balanceCost(self,NodalDemand):
		return self.pvPanelCost(NodalDemand)*self.BalCostFracTotalCost
	def pvInitialCost(self,NodalDemand):
		return self.pvPanelCost(NodalDemand) + self.balanceCost(NodalDemand)+ self.batteryCost(NodalDemand)
	def pvOprMainCost(self,NodalDemand):
		return self.pvInitialCost(NodalDemand)*self.MainCostFracTotalCost


	
	# PV Battery replacement cost/year
	def batteryReplacementCost(self,NodalDemand):
		return self.batteryCost(NodalDemand)/self.batteryLifetime

	
	# PV Balance replacement Cost
	def balanceReplacementCost(self,NodalDemand):
		return self.balanceCost(NodalDemand)/self.balanceLifetime

	# recurring Cost
	def recurrCost(self,NodalDemand):
		# print "pv recurr cost " + str(self.pvrecurrCost(NodalDemand))
		# print "pvOprMainCost  " + str(self.pvOprMainCost(NodalDemand))
		# print "batteryReplacementCost " + str(self.batteryReplacementCost(NodalDemand))
		# print "balanceReplacementCost " + str(self.balanceReplacementCost(NodalDemand))
		return self.pvrecurrCost(NodalDemand) + self.pvOprMainCost(NodalDemand) + self.batteryReplacementCost(NodalDemand) + self.balanceReplacementCost(NodalDemand)

	# initial Cost
	def initialCost(self,NodalDemand):
		return self.pvInitialCost(NodalDemand)

	def discountedCashFlowFact_Recurr(self,NodalDemand,hh,years):
		finalCost=0
		self.timePeriod=years
		for i in range(1,self.timePeriod):
			finalCost+=1/(1+self.interestRate)**i
		return finalCost

	def discountedCashFlowFact_Initial(self,NodalDemand,hh):
		return self.initialCost(NodalDemand)
	def calculateCost(self,NodalDemand,hh,years):
		NodalDemand=NodalDemand*hh
		return self.discountedCashFlowFact_Initial(NodalDemand,hh),self.recurrCost(NodalDemand),self.discountedCashFlowFact_Recurr(NodalDemand,hh,years)

def main():
	Node3=offgrid()
	i,r,f=Node3.calculateCost(48,20,30)
	print i
	print r
	print i+r*f


if __name__=='__main__':
	main()