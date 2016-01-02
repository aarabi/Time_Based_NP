class solarMinigrid(object):
	def __init__(self):
		self.pvLifetime=7
		self.pvPanelCostPerKW=800
		self.minSysPVCap=0.05
		self.efficiencyLoss=0.5
		self.peakSunHours=1320
		self.MainCostFracTotalCost=0.05
		self.BalCostFracTotalCost=1.5
		self.PvBatteryCostperKWH=150
		self.PVBatteryKWHperKW=6
		self.batteryLifetime=7
		self.balanceLifetime=7
		self.timePeriod=30
		self.interestRate=0.07
		self.wirecosts=0.75
		self.meterCostsperHH=100
		self.lvCostperMeter=12.6
		self.interhouseholddistance=22
		self.wireLifetime=7
		self.smartmeterLifetime=7
	# PV comp Recurring cost 
	def calCapPV(self,NodalDemand):
		return (NodalDemand/(1-self.efficiencyLoss)/self.peakSunHours)
	def pvPanelActualCap(self,NodalDemand):
		return max(self.minSysPVCap,self.calCapPV(NodalDemand))
	def pvPanelCost(self,NodalDemand):
		print self.pvPanelActualCap(NodalDemand)
		return self.pvPanelActualCap(NodalDemand)*self.pvPanelCostPerKW
	def pvrecurrCost(self,NodalDemand):
		return (self.pvPanelCost(NodalDemand)/self.pvLifetime)

	# Wire costs
	def wireCost(self,NodalDemand,hh):
		return self.wirecosts*self.interhouseholddistance*hh
	def smartCost(self,NodalDemand,hh):
		return hh*self.meterCostsperHH

	
	# Photovoltaics com Operations and Maintenance cost per year
	def batteryCost(self,NodalDemand):
		return self.pvPanelActualCap(NodalDemand)*self.PvBatteryCostperKWH*self.PVBatteryKWHperKW
	def balanceCost(self,NodalDemand):
		return self.pvPanelCost(NodalDemand)*self.BalCostFracTotalCost
	def pvInitialCost(self,NodalDemand,hh):
		return self.pvPanelCost(NodalDemand) + self.balanceCost(NodalDemand)+ self.batteryCost(NodalDemand) + self.wireCost(NodalDemand,hh) + self.smartCost(NodalDemand,hh)
	def pvOprMainCost(self,NodalDemand,hh):
		return self.pvInitialCost(NodalDemand,hh)*self.MainCostFracTotalCost


	
	# PV Battery replacement cost/year
	def batteryReplacementCost(self,NodalDemand):
		return self.batteryCost(NodalDemand)/self.batteryLifetime

	
	# PV Balance replacement Cost
	def balanceReplacementCost(self,NodalDemand):
		return self.balanceCost(NodalDemand)/self.balanceLifetime

	# wire costs replacement 
	def wireReplacement(self,NodalDemand,hh):
		return self.wireCost(NodalDemand,hh)/self.wireLifetime
	def smartReplacement(self,NodalDemand,hh):
		return self.smartCost(NodalDemand,hh)/self.smartmeterLifetime
	
	# recurring Cost
	def recurrCost(self,NodalDemand,hh):
		# print "pv recurr cost " + str(self.pvrecurrCost(NodalDemand))
		# print "pvOprMainCost  " + str(self.pvOprMainCost(NodalDemand))
		# print "batteryReplacementCost " + str(self.batteryReplacementCost(NodalDemand))
		# print "balanceReplacementCost " + str(self.balanceReplacementCost(NodalDemand))
		return self.pvrecurrCost(NodalDemand) + self.pvOprMainCost(NodalDemand,hh) + self.batteryReplacementCost(NodalDemand) + self.balanceReplacementCost(NodalDemand) + self.wireReplacement(self,NodalDemand,hh) + self.smartReplacement(self,NodalDemand,hh)

	# initial Cost
	def initialCost(self,NodalDemand,hh):
		return self.pvInitialCost(NodalDemand,hh)

	def discountedCashFlowFact_Recurr(self,NodalDemand,hh):
		finalCost=0
		for i in range(1,self.timePeriod):
			finalCost+=1/(1+self.interestRate)**i
		return finalCost

	def discountedCashFlowFact_Initial(self,NodalDemand,hh):
		return self.initialCost(NodalDemand,hh)

	def calculateCost(self,NodalDemand,hh):
		NodalDemand=NodalDemand*hh
		return self.discountedCashFlowFact_Initial(NodalDemand,hh),self.recurrCost(NodalDemand,hh),self.discountedCashFlowFact_Recurr(NodalDemand,hh)



def main():
	Node3=solarMinigrid()
	offgrid_cost,rec,fact=Node3.calculateCost(48,20)
	print offgrid_cost
	print rec
	print offgrid_cost+rec*fact


if __name__=='__main__':
	main()