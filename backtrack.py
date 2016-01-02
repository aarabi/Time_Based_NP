from sympy import *
import matplotlib.pyplot as plt
def backtrackOffgrid():
	discountedCashFlow=12.409041183505854
	transformerLifetime=10
	transformerCostperKW=50
	demandToPeakConversionFactor=0.000365
	distributionLoss=0.15
	transformerOprMainFracTotalCost=0.03
	electricityCostperKWH=0.13
	lvOprMainFracTotalCost=0.01
	lvCostperConnection=100
	lvLifetime=30
	lvCostperMeter=12.6
	installationCostperConnection=200
	lvlineEquipCostperConnection=175
	interHouseHoldDistance=22


	pvLifetime=20
	pvPanelCostPerKW=800
	minSysPVCap=0.05
	efficiencyLoss=0.1
	peakSunHours=1320
	MainCostFracTotalCost=0.05
	BalCostFracTotalCost=1
	PvBatteryCostperKWH=150
	PVBatteryKWHperKW=6
	batteryLifetime=3
	balanceLifetime=10

	#cost = Symbol("cost", positive=True)

	demand = Symbol("demand", positive=True)
	cost = Symbol("cost", positive=True)
	hh=Symbol("hh",positive=True)
	expr = cost \
	- discountedCashFlow*demand*hh*pvPanelCostPerKW/((1-efficiencyLoss)*peakSunHours*pvLifetime) \
	- discountedCashFlow*MainCostFracTotalCost*demand*hh*pvPanelCostPerKW/((1-efficiencyLoss)*peakSunHours) \
	- discountedCashFlow*MainCostFracTotalCost*BalCostFracTotalCost*demand*hh*pvPanelCostPerKW/((1-efficiencyLoss)*peakSunHours) \
	- discountedCashFlow*MainCostFracTotalCost*PvBatteryCostperKWH*PVBatteryKWHperKW*demand*hh/((1-efficiencyLoss)*peakSunHours) \
	- discountedCashFlow*PvBatteryCostperKWH*PVBatteryKWHperKW*demand*hh/(batteryLifetime*peakSunHours-efficiencyLoss*batteryLifetime*peakSunHours) \
	- discountedCashFlow*demand*hh*BalCostFracTotalCost*pvPanelCostPerKW/((1-efficiencyLoss)*peakSunHours*balanceLifetime) \
	- demand*hh*pvPanelCostPerKW/((1-efficiencyLoss)*peakSunHours) \
	- demand*hh*pvPanelCostPerKW*BalCostFracTotalCost/((1-efficiencyLoss)*peakSunHours) \
	- PvBatteryCostperKWH*PVBatteryKWHperKW*demand*hh/((1-efficiencyLoss)*peakSunHours)
	# print expr
	# print " ---- "
	expr2=solve(expr,demand)[0]
	return expr
	
def backtrackSolarMinigrid():
	discountedCashFlow=12.409041183505854
	transformerLifetime=10
	transformerCostperKW=50
	demandToPeakConversionFactor=0.000365
	distributionLoss=0.15
	transformerOprMainFracTotalCost=0.03
	electricityCostperKWH=0.13
	lvOprMainFracTotalCost=0.01
	lvCostperConnection=100
	lvLifetime=30
	lvCostperMeter=12.6
	installationCostperConnection=200
	lvlineEquipCostperConnection=175
	interHouseHoldDistance=22

	pvLifetime=20
	pvPanelCostPerKW=800
	minSysPVCap=0.05
	efficiencyLoss=0.1
	peakSunHours=1320
	MainCostFracTotalCost=0.05
	BalCostFracTotalCost=1
	PvBatteryCostperKWH=150
	PVBatteryKWHperKW=6
	batteryLifetime=3
	balanceLifetime=10
	wirecosts=0.75
	meterCostsperHH=100

	#cost = Symbol("cost", positive=True)

	demand = Symbol("demand", positive=True)
	cost = Symbol("cost", positive=True)
	hh=Symbol("hh",positive=True)
	expr = cost \
	- discountedCashFlow*demand*hh*pvPanelCostPerKW/((1-efficiencyLoss)*peakSunHours*pvLifetime) \
	- discountedCashFlow*MainCostFracTotalCost*demand*hh*pvPanelCostPerKW/((1-efficiencyLoss)*peakSunHours) \
	- discountedCashFlow*wirecosts*lvCostperMeter*MainCostFracTotalCost \
	- discountedCashFlow*hh*meterCostsperHH*MainCostFracTotalCost \
	- discountedCashFlow*MainCostFracTotalCost*BalCostFracTotalCost*demand*hh*pvPanelCostPerKW/((1-efficiencyLoss)*peakSunHours) \
	- discountedCashFlow*MainCostFracTotalCost*PvBatteryCostperKWH*PVBatteryKWHperKW*demand*hh/((1-efficiencyLoss)*peakSunHours) \
	- discountedCashFlow*PvBatteryCostperKWH*PVBatteryKWHperKW*demand*hh/((1-efficiencyLoss)*peakSunHours*batteryLifetime) \
	- discountedCashFlow*demand*hh*BalCostFracTotalCost*pvPanelCostPerKW/((1-efficiencyLoss)*peakSunHours*balanceLifetime) \
	- demand*hh*pvPanelCostPerKW/((1-efficiencyLoss)*peakSunHours) \
	- demand*hh*pvPanelCostPerKW*BalCostFracTotalCost/((1-efficiencyLoss)*peakSunHours) \
	- PvBatteryCostperKWH*PVBatteryKWHperKW*demand*hh/((1-efficiencyLoss)*peakSunHours) \
	- wirecosts*lvCostperMeter \
	- hh*meterCostsperHH
	# print expr
	# print " ---- "
	expr2=solve(expr,demand)[0]
	return expr

# def main():
# 	#backtrackOffgrid(4661647.72727273,250)
# 	expr1=backtrackMinigrid()
# 	cost = Symbol("cost", positive=True)
# 	expr1=eval('cost-expr1')
# 	expr1='%s' % expr1
# 	demand = 24
# 	hh=76
# 	a=compile(expr1,'','eval')
# 	print eval(a)
# # 	y=[]
# # 	x=[]
# # 	print "offgrid costs"
# # 	for i in range(0,2000):
# # 		demand=i
# # 		x.append(i)
# # 		a=compile(expr1,'','eval')
# # 		y.append(eval(a))
# # 		print str(i)+" "+str(eval(a))
# # 	plt.plot(x,y,label="offgrid costs")

	
# # 	expr1,expr2=backtrackMinigrid()
# # 	cost = Symbol("cost", positive=True)
# # 	hh=1
# # 	expr1=eval('cost-expr1')
# # 	print expr1
# # 	expr1='%s' % expr1
# # 	m=[]
# # 	n=[]
# # 	print "minigrid costs"
# # 	for i in range(0,2000):
# # 		demand=i
# # 		m.append(i)
# # 		a=compile(expr1,'','eval')
# # 		n.append(eval(a))
# # 		print str(i)+" "+str(eval(a))
# # 	plt.plot(m,n,label="minigrid costs")
# # 	plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	
# # 	plt.savefig('mini_off_grid_Costs.png',bbox_inches='tight')




# if __name__=='__main__':
# 	main()