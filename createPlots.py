import matplotlib.pyplot as plt
import pandas as pd
import network, csv
import numpy as np
def households_perc_time(NodeList,completedSet,inputfilepath,outputfilepath,maxyears):
	filename2=inputfilepath+'/metrics-local.csv'
	df = pd.read_csv(filename2, skiprows=1)
	saved_column_grid=df["metric_sys"]
	saved_column_pop=df["Population"]
	timebased=[0]*(maxyears+1)
	totalhh=0
	for item in completedSet:
		if item.getYears()!=100:
			timebased[int(item.getYears())]+=item.getHouseholds()
	for item in NodeList:
		totalhh+=item.getHouseholds()
	timebased=np.cumsum(timebased)
	timebased_perc=[float(x/totalhh) for x in timebased]
	plt.plot(timebased_perc,label="Time Based",color='b')

	nps=0
	for i in xrange(0,len(saved_column_grid)):
		if saved_column_grid[i]=='grid':
			if saved_column_pop[i]>5000:
				nps+=saved_column_pop[i]/5.8
			else:
				nps+=saved_column_pop[i]/6.1
	x=[0,30]
	y=[0,nps/totalhh]
	plt.plot(x,y,label="Network Planner",color='r')
	plt.ylim(0,1)
	plt.xlim(0,31)
	plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	plt.ylabel('Percentage of households')
   	plt.xlabel('Time (years)')
	plt.savefig(outputfilepath+'/Household_perc.png', bbox_inches='tight')
	plt.close()

	plt.plot(timebased,label="Time Based",color='b')
	x=[0,30]
	y=[0,nps]
	plt.plot(x,y,label="Network Planner",color='r')
	plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	plt.ylabel('Number of households')
   	plt.xlabel('Time (years)')
   	plt.xlim(0,31)
	plt.savefig(outputfilepath+'/Household.png', bbox_inches='tight')
	plt.close()



def NPV_time(NodeList,completedSet,inputfilepath,outputfilepath,maxyears):
	# rows = list(csv.reader(file(inputfilepath+'/metrics-global.csv', 'rb')))
	# np_cost = float(rows[1][2])/1000000
	SolarMinigrid_Cost=[0]*(maxyears+1)
	grid_cost=[0]*(maxyears+1)
	offgrid_cost=[0]*(maxyears+1)
	total_cost=[0]*(maxyears+1)
	households_count=[0]*(maxyears+1)
	# for item in completedSet:
	# 	if item.getNPV_temp()==item.getOffGridCost_Initial()+item.getOffGridCost_recurr()*item.getDiscountFact_offgrid():
	# 		if t==1:
	# 			offgrid_cost[t]+=item.getOffGridCost_Initial()
	# 		else:
	# 			offgrid_cost[t]+=item.getOffGridCost_recurr()
	# 	else:
	# 		if t==1:
	# 			SolarMinigrid_Cost[t]+=item.getSolarMinigridCost_Initial()
	# 		else:
	# 			SolarMinigrid_Cost[t]+=item.getSolarMinigridCost_recurr()
	# elif t==item.getYears():
	# 	grid_cost[t]+=item.getGridCost_Initial()
	# else:
	# 	grid_cost[t]+item.getGridCost_recurr()
	# total_cost[t]=offgrid_cost[t]+SolarMinigrid_Cost[t]+grid_cost[t]


	# total_cost_perc=[float(x/1000000) for x in total_cost]
	# plt.plot(total_cost_perc,label="total_cost",color='r')
	
	# grid_cost_perc=[float(x/1000000) for x in grid_cost]
	# plt.plot(grid_cost_perc,label="grid_cost",color='g')
	
	# offgrid_cost_perc=[float(x/1000000) for x in offgrid_cost]
	# plt.plot(offgrid_cost_perc,label="offgrid_cost",color='b')
	
	# solarminigrid_cost_perc=[float(x/1000000) for x in SolarMinigrid_Cost]
	# plt.plot(solarminigrid_cost_perc,label="SolarMinigrid_Cost",color='y')
	# plt.xlim(0,int(maxyears)+1)
	# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	# plt.xlabel('Time (years)')
	# plt.ylabel('Millions of Dollars')
	# plt.savefig(outputfilepath+'/Cost.png', bbox_inches='tight')
	# plt.close()
	
	# ax = plt.subplot(111)
	# ax.bar([0,1], [0,grid_cost/1000000],width=0.1,color='b',align='center',label="Time Based (grid only)")
	# ax.bar([0,2], [0,temp_cost/1000000],width=0.1,color='y',align='center',label="Time Based (temp cost)")
	# ax.bar([0,3], [0,timebased/1000000],width=0.1,color='g',align='center',label="Time Based (total)")
	# ax.bar([0,4], [0,np_cost],width=0.1,color='r',align='center',label="Network Planner")
	# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	# plt.ylabel('NPV')
	# plt.xlim(0,5)
 #   	plt.xlabel('Time (years)')
	# plt.savefig(outputfilepath+'/NPV.png', bbox_inches='tight')
	# plt.close()


def lengthWire_time(NodeList,completedSet,inputfilepath,outputfilepath,maxyears):
	filename2=inputfilepath+'/metrics-local.csv'
	df = pd.read_csv(filename2, skiprows=1)
	saved_column_grid=df["metric_sys"]
	saved_column_pop=df["Population"]
	rows = list(csv.reader(file(inputfilepath+'/metrics-global.csv', 'rb')))
	np_len = float(rows[11][2])
	timebased=[0]*(maxyears)
	totalhh=0
	total_households=[0]*(maxyears)	
	for item in completedSet:
		timebased[int(item.getYears())]+=item.getDistance()
		total_households[int(item.getYears())]+=item.getHouseholds()
	timebased=np.cumsum(timebased)
	total_households=np.cumsum(total_households)
	for i in range(0,len(timebased)):
		if total_households[i]!=0:
			timebased[i]/=total_households[i]
		else:
			timebased[i]=0
	plt.plot(timebased,label="Time Based",color='b')

	nps=0
	for i in xrange(0,len(saved_column_grid)):
		if saved_column_grid[i]=='grid':
			if saved_column_pop[i]>5000:
				nps+=saved_column_pop[i]/5.8
			else:
				nps+=saved_column_pop[i]/6.1
	x=[0,30]
	y=[0,np_len/nps]
	plt.plot(x,y,label="Network Planner",color='r')
	plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	plt.ylabel('Length of Wire (meters per households)')
	plt.xlim(0,31)
   	plt.xlabel('Time (years)')
	plt.savefig(outputfilepath+'/MVMax.png', bbox_inches='tight')
	plt.close()



	total_wire=[0]*(maxyears+1)
	total_households=[0]*(maxyears+1)
	for item in completedSet:
		total_wire[item.getYears()]+=item.getDistance()
		total_households[item.getYears()]+=item.getHouseholds()

	for i in range(0,len(total_wire)):
		if total_households[i]!=0:
			total_wire[i]/=total_households[i]
		else:
			total_wire[i]=0
	total_wire_perc=[float(x) for x in total_wire]
	plt.plot(total_wire_perc,label="total_wire",color='r')
	plt.xlabel('Time (years)')
	plt.savefig(outputfilepath+'/annual_wire.png', bbox_inches='tight')
	plt.close()


def plotRevenue(NodeList,completedSet,outputfilepath,maxyears):
	offGrid_revenue=[0]*(maxyears+1)
	SolarMiniGrid_revenue=[0]*(maxyears+1)
	grid_revenue=[0]*(maxyears+1)
	for item in completedSet:
		if item.getNPV_temp()==item.getOffGridCost_Initial()+item.getOffGridCost_recurr()*item.getDiscountFact_offgrid():
			offGrid_revenue[item.getYears()]+=item.getStartDemand()*((1.25)**item.getYears())*5*item.getHouseholds()
		else:
			SolarMiniGrid_revenue[item.getYears()]+=item.getStartDemand()*((1.25)**item.getYears())*2*item.getHouseholds()
		grid_revenue[item.getYears()]+=item.getStartDemand()*((1.25)**item.getYears())*0.20*item.getHouseholds()

	plt.plot(offGrid_revenue,label="offGrid_revenue")
	plt.plot(SolarMiniGrid_revenue,label="SolarMiniGrid_revenue")
	plt.plot(grid_revenue,label="grid_revenue")
	plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	plt.ylabel('Revenue')
	plt.xlim(1,maxyears+1)
   	plt.xlabel('Time (years)')
	plt.savefig(outputfilepath+'/revenue.png', bbox_inches='tight')
	plt.close()


def plotValue(NodeList,completedSet,outputfilepath,maxyears):
	offGrid_revenue=[0]*(maxyears+1)
	SolarMiniGrid_revenue=[0]*(maxyears+1)
	grid_revenue=[0]*(maxyears+1)
	for item in completedSet:
		if item.getNPV_temp()==item.getOffGridCost_Initial()+item.getOffGridCost_recurr()*item.getDiscountFact_offgrid():
			offGrid_revenue[item.getYears()]+=item.getStartDemand()*((1.25)**item.getYears())*5*item.getHouseholds()
		else:
			SolarMiniGrid_revenue[item.getYears()]+=item.getStartDemand()*((1.25)**item.getYears())*3*item.getHouseholds()
		grid_revenue[item.getYears()]+=item.getStartDemand()*((1.25)**item.getYears())*0.75*item.getHouseholds()

	plt.plot(offGrid_revenue,label="offGrid_Value")
	plt.plot(SolarMiniGrid_revenue,label="SolarMiniGrid_Value")
	plt.plot(grid_revenue,label="grid_Value")
	plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	plt.ylabel('Value')
	plt.xlim(1,maxyears+1)
   	plt.xlabel('Time (years)')
	plt.savefig(outputfilepath+'/Value.png', bbox_inches='tight')
	plt.close()
