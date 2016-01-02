
class minigrid(object):
	def __init__(self):
		self.discountedCashFlow=12.409041183505854
		self.dieselGeneratorOprMainFracTotalCost=0.1
		self.dieselFuelCostperKW=150
		self.demandToPeakConversionFactor=0.000365
		self.availableSystemCap=25
		self.distributionLoss=0.1
		self.dieselFuelCostperLitre=0.87
		self.dieselFuelLitresperKWH=0.5
		self.peakElectricHoursOpr=1460
		self.dieselGeneratorLifetime=5
		self.lvOprMainFracTotalCost=0.01
		self.lvCostperConnection=100
		self.lvLifetime=30
		self.lvCostperMeter=12.6
		self.interHouseHoldDistance=22
		self.dieselGeneratorInstallFracTotalCost=0.5
		self.timePeriod=7
		self.interestRate=0.07
	# Diesel generator Operation and Maintanance Cost
	def dieselDesiredSystemCap(self,NodalDemand):
		return (NodalDemand*self.demandToPeakConversionFactor)/(1-self.distributionLoss)
	def dieselActualSystemCap(self,NodalDemand):
		return max(self.availableSystemCap,self.dieselDesiredSystemCap(NodalDemand))
	def dieselGeneratorCost(self,NodalDemand):
		return self.dieselActualSystemCap(NodalDemand)*self.dieselFuelCostperKW
	def dieselOprMainCost(self,NodalDemand):
		return self.dieselGeneratorCost(NodalDemand)*self.dieselGeneratorOprMainFracTotalCost

	# Diesel fuel costs per year
	def dieselGeneratorHoursOpr(self,NodalDemand):
		return max(NodalDemand/self.dieselActualSystemCap(NodalDemand)/(1-self.distributionLoss),self.peakElectricHoursOpr)
	def dieselFuelCost(self,NodalDemand):
		return self.dieselFuelCostperLitre*self.dieselFuelLitresperKWH*self.dieselActualSystemCap(NodalDemand)*self.dieselGeneratorHoursOpr(NodalDemand)

	# Diesel replacement cost
	def dieselGeneratorReplacementCost(self,NodalDemand):
		return self.dieselGeneratorCost(NodalDemand)/self.dieselGeneratorLifetime

	# Low Volatge Operations and Maintainance cost per year
	def lvEquipment(self,hh):
		return hh*self.lvCostperConnection
	def lvLineEquipOprMainCost(self,hh):
		return self.lvEquipment(hh)*self.lvOprMainFracTotalCost


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
	def recurrCost(self,NodalDemand,hh):
		return self.dieselOprMainCost(NodalDemand)+self.dieselFuelCost(NodalDemand)+self.dieselGeneratorReplacementCost(NodalDemand)+self.lvLineEquipOprMainCost(hh)+self.lvRecurringCost(hh)

	# initial cost
	def dieselGeneratorInstallationCost(self,NodalDemand):
		return self.dieselGeneratorCost(NodalDemand)*self.dieselGeneratorInstallFracTotalCost
	def initialCost(self,NodalDemand,hh):
		return self.lvEquipment(hh)+self.dieselGeneratorInstallationCost(NodalDemand)+self.dieselGeneratorCost(NodalDemand)+self.lvInitialCost(hh)

	def discountedCashFlowFact_Recurr(self,NodalDemand,hh):
		recurrCost=self.recurrCost(NodalDemand,hh)
		finalCost=0
		for i in range(2,self.timePeriod+1):
			finalCost+=recurrCost/(1+self.interestRate)**i
		return finalCost

	def discountedCashFlowFact_Initial(self,NodalDemand,hh):
		return self.initialCost(NodalDemand,hh)/(1+self.timePeriod)
	def calculateCost(self,NodalDemand,hh):
		NodalDemand=NodalDemand*hh
		return self.discountedCashFlowFact_Initial(NodalDemand,hh) + self.discountedCashFlowFact_Recurr(NodalDemand,hh)


def main():
	m=minigrid()
	print m.calculateCost(800,76)




if __name__=='__main__':
	main()