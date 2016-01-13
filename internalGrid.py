class internalGrid(object):
	def __init__(self):
		self.transformerLifetime=10
		self.transformerCostperKW=50
		self.demandToPeakConversionFactor=0.000365
		self.distributionLoss=0.15
		self.transformerOprMainFracTotalCost=0.03
		self.electricityCostperKWH=0.13
		self.lvOprMainFracTotalCost=0.01
		self.lvCostperConnection=100
		self.lvLifetime=30
		self.lvCostperMeter=12.6
		self.installationCostperConnection=200
		self.lvlineEquipCostperConnection=175
		self.interHouseHoldDistance=22
		self.timePeriod=30
		self.interestRate=0.07
	#transformer replacement cost
	def transformerDesiredSysCap(self,demand,hh):
		return demand*hh*(self.demandToPeakConversionFactor)/(1-self.distributionLoss)
	def gridTransActualSysCap(self,demand,hh):
		return max(self.transformerDesiredSysCap(demand,hh),self.transformerCostperKW)
	def transformerCost(self,demand,hh):
		return self.transformerCostperKW*self.gridTransActualSysCap(demand,hh)
	def transformerReplacement(self,demand,hh):
		return self.transformerCost(demand,hh)/self.transformerLifetime

	#transformer Operations and Maintainance cost
	def transformerOprMainCost(self,demand,hh):
		return self.transformerCost(demand,hh)*self.transformerOprMainFracTotalCost

	# electricity cost per year
	def electricityCost(self,demand,hh):
		return demand*hh*self.electricityCostperKWH/(1-self.distributionLoss)

	# Low Volatge Operations and Maintainance cost per year
	def lvEquipment(self,hh):
		return hh*self.lvCostperConnection
	def lvLineEquipOprMainCost(self,hh):
		return self.lvEquipment2(hh)*self.lvOprMainFracTotalCost


	# Low Volatge recurring cost 
	def totalLvLength(self,hh):
		return (hh-1)*self.interHouseHoldDistance
	def lvInitialCost(self,hh):
		return self.lvCostperMeter*self.totalLvLength(hh)
	def lvReplacementCost(self,hh):
		return self.lvInitialCost(hh)/self.lvLifetime
	def lvOprMainCost(self,hh):
		return self.lvOprMainFracTotalCost*self.lvInitialCost(hh)
	def lvRecurringCost(self,hh):
		return self.lvReplacementCost(hh)+self.lvOprMainCost(hh)

	# recurring cost
	def recurrCost(self,demand,hh):
		return self.transformerReplacement(demand,hh) + self.transformerOprMainCost(demand,hh)+self.electricityCost(demand,hh)+self.lvLineEquipOprMainCost(hh)+self.lvRecurringCost(hh)
	
	# initial cost
	def installationCost(self,hh):
		return hh*self.installationCostperConnection
	def lvEquipment2(self,hh):
		return (hh+0.4)*self.lvlineEquipCostperConnection
	def initialCost(self,demand,hh):
		return self.installationCost(hh)+self.transformerCost(demand,hh)+self.lvEquipment2(hh)+self.lvInitialCost(hh)
	def discountedCashFlowFact_Recurr(self,NodalDemand,hh,years):
		finalCost=0
		self.timePeriod=years
		for i in range(1,self.timePeriod):
			finalCost+=1/(1+self.interestRate)**i
		return finalCost

	def discountedCashFlowFact_Initial(self,NodalDemand,hh,distance_cost):
		return (self.initialCost(NodalDemand,hh)+ distance_cost)
	def calculateCost(self,NodalDemand,hh,distance_cost,years):
		return self.discountedCashFlowFact_Initial(NodalDemand,hh,distance_cost),self.recurrCost(NodalDemand,hh),self.discountedCashFlowFact_Recurr(NodalDemand,hh,years)


def main():
	#backtrackOffgrid(4661647.72727273,250)
	node = internalGrid()
	i,r,f=node.calculateCost(500,18,0,30)
	print i+r*f
if __name__=='__main__':
	main()