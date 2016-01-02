import fiona
from sympy import *
from rtree import *
from math import *
from shapely.geometry import Polygon, Point, LineString, MultiLineString, mapping, shape
import internalGrid, shapefile, createPlots, minigrid, offgrid, solarminigrid, saveData

class node(object):
	def __init__(self,index,longitude,latitude,households):
		self.index=index
		self.longitude=longitude
		self.latitude=latitude
		self.households=households
		self.startDemand=25
		self.currentDemand=25
		self.maxDemand=800
		self.nearestGrid_x=0
		self.nearestGrid_y=0
		self.NPV_grid=0
		self.NPV_temp=0
		self.years=100
		self.Mv_hh=0
		self.distance=0
		self.solarminigrid_initialcost=0
		self.solarminigrid_recurcost=0
		self.offgrid_initialcost=0
		self.offgrid_recurrcost=0
		self.grid_initialcost=0
		self.grid_recurrcost=0
		self.discountFactor_grid=0
		self.discountFactor_offgrid=0
		self.discountFactor_minigrid=0

	def getLongitude(self):
		return self.longitude

	def getLatitude(self):
		return self.latitude

	def getHouseholds(self):
		return self.households

	def getStartDemand(self):
		return self.startDemand

	def getMaxDemand(self):
		return self.maxDemand

	def getYears(self):
		return self.years

	def getNPV_grid(self):
		return self.NPV_grid

	def getDistance(self):
		return self.distance

	def getNPV_temp(self):
		return self.NPV_temp

	def getCurrentDemand(self):
		return self.currentDemand

	def getNearestGrid_x(self):
		return self.nearestGrid_x

	def getNearestGrid_y(self):
		return self.nearestGrid_y

	def getSolarMinigridCost_Initial(self):
		return self.solarminigrid_initialcost

	def getOffGridCost_Initial(self):
		return self.offgrid_initialcost

	def getGridCost_Initial(self):
		return self.grid_initialcost

	def getGridCost_recurr(self):
		return self.grid_recurrcost

	def getSolarMinigridCost_recurr(self):
		return self.solarminigrid_recurcost

	def getOffGridCost_recurr(self):
		return self.offgrid_recurrcost

	def getDiscountFact_solarminigrid(self):
		return self.discountFactor_minigrid

	def getDiscountFact_offgrid(self):
		return self.discountFactor_offgrid

	def getDiscountFact_grid(self):
		return self.discountFactor_grid

	def setDistance(self,distance):
		self.distance=distance

	def setCurrentDemand(self,currentDemand):
		self.currentDemand=currentDemand

	def setNearestGrid_x(self,nearestGrid_x):
		self.nearestGrid_x=nearestGrid_x

	def setNearestGrid_y(self,nearestGrid_y):
		self.nearestGrid_y=nearestGrid_y

	def setYear(self,year):
		self.years=year

	def setNPV_grid(self,cost):
		self.NPV_grid=cost

	def setNPV_temp(self,cost):
		self.NPV_temp=cost

	def setSolarMinigridCost_Initial(self,cost):
		self.solarminigrid_initialcost=cost

	def setOffGridCost_Initial(self,cost):
		self.offgrid_initialcost=cost

	def setSolarMinigridCost_recurr(self,cost):
		self.solarminigrid_recurcost=cost

	def setOffGridCost_recurr(self,cost):
		self.offgrid_recurrcost=cost

	def setDiscountFact_solarminigrid(self,factor):
		self.discountFactor_minigrid=factor

	def setDiscountFact_offgrid(self,factor):
		self.discountFactor_offgrid=factor

	def setGridCost_Initial(self,cost):
		self.grid_initialcost=cost

	def setGridCost_recurr(self,cost):
		self.grid_recurrcost=cost

	def setDiscountFact_grid(self,factor):
		self.discountFactor_grid=factor

def PreExistingGrid(inputfilepath):
	with fiona.open(inputfilepath+'networks-existing.shp') as source:
		lines_list=[]
		for pt in source:
			for l in range(0,len(pt['geometry']["coordinates"])-1,1):
				point1= pt['geometry']["coordinates"][l]
				point2=pt['geometry']["coordinates"][l+1]
				lines_list.append(LineString([Point(point1),Point(point2)]))
	return lines_list

def createSets(NodeList):
	length=len(NodeList)
	viableSet=[]
	nonViableSet=NodeList
	return viableSet,nonViableSet

def calculateDistance(lon1,lat1,lon2,lat2):
	#print str((lon1,lat1)) + " and "+ str((lon2,lat2))
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	dlon = lon2 - lon1 
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a))
	km = 6367 * c
	#print " distance " + str(km)
	return km

def pnt2line(pnt,poly_idx,preExistingGridLines):
	point = Point(pnt)
	dist=(preExistingGridLines[poly_idx[0]].project(point))
	np_x = preExistingGridLines[poly_idx[0]].interpolate(preExistingGridLines[poly_idx[0]].project(point)).x
	np_y = preExistingGridLines[poly_idx[0]].interpolate(preExistingGridLines[poly_idx[0]].project(point)).y
	dist=calculateDistance(pnt[0],pnt[1],np_x,np_y)
	return dist,(np_x,np_y)

def offGridCosts(current_node):
	demand=current_node.getCurrentDemand()
	hh=current_node.getHouseholds()
	Node3=offgrid.offgrid()
	offgrid_initialcost,offgrid_recurrcost,discountFactor_offgrid=Node3.calculateCost(demand,hh)
	return offgrid_initialcost,offgrid_recurrcost,discountFactor_offgrid


def miniSolarGridCosts(current_node):
	demand=current_node.getCurrentDemand()
	hh=current_node.getHouseholds()
	Node3=solarminigrid.solarMinigrid()
	solarminigrid_initialcost,solarminigrid_recurcost,discountFactor_minigrid=Node3.calculateCost(demand,hh)
	return solarminigrid_initialcost,solarminigrid_recurcost,discountFactor_minigrid

def gridCosts(current_node,idx,preExistingGridLines):
	point = Point(current_node.getLongitude(),current_node.getLatitude())
	poly_idx=list(idx.nearest((point.coords[0])))
	distance,nearest=pnt2line((current_node.getLongitude(),current_node.getLatitude()),poly_idx,preExistingGridLines)
	distance_cost=float(distance)*1000*22
	Node3=internalGrid.internalGrid()
	grid_initialcost,grid_recurrcost,discountFactor_grid = Node3.calculateCost(current_node.getCurrentDemand(),current_node.getHouseholds(),distance_cost)
	current_node.setNearestGrid_x(nearest[0])
	current_node.setNearestGrid_y(nearest[1])
	return grid_initialcost,grid_recurrcost,discountFactor_grid


def calculateYears(current_node,idx,preExistingGridLines):
	
	offgrid_initialcost,offgrid_recurrcost,discountFactor_offgrid=offGridCosts(current_node)
	offgrid_cost=offgrid_initialcost+offgrid_recurrcost*discountFactor_offgrid
	grid_initialcost,grid_recurrcost,discountFactor_grid=gridCosts(current_node,idx,preExistingGridLines)
	grid_cost=grid_initialcost+grid_recurrcost*discountFactor_grid
	solarminigrid_initialcost,solarminigrid_recurcost,discountFactor_minigrid=miniSolarGridCosts(current_node)
	miniSolargrid_cost=solarminigrid_initialcost+solarminigrid_recurcost*discountFactor_minigrid
	minimum_cost=min(offgrid_cost,grid_cost,miniSolargrid_cost)
	newGridCost=0
	print "grid costs " + str(grid_cost)
	print "offgrid_cost " +str(offgrid_cost)
	print "miniSolargrid_cost "+ str(miniSolargrid_cost)
	if current_node.getCurrentDemand()<=current_node.getMaxDemand():
		if minimum_cost==grid_cost:
			current_node.setYear(0)
			current_node.setNPV_grid(grid_cost)
			# current_node.setOffGridCost_Initial(offgrid_initialcost)
			# current_node.setSolarMinigridCost_Initial(solarminigrid_initialcost)
			current_node.setGridCost_Initial(grid_initialcost)
			# current_node.setOffGridCost_recurr(offgrid_recurrcost)
			# current_node.setSolarMinigridCost_recurr(solarminigrid_recurcost)
			current_node.setGridCost_recurr(grid_recurrcost)
			# current_node.setDiscountFact_offgrid(discountFactor_offgrid)
			# current_node.setDiscountFact_solarminigrid(discountFactor_minigrid)
			current_node.setDiscountFact_grid(discountFactor_grid)
	return current_node

def calculateViableSet(nonViableSet,preExistingGridLines):
	idx=createRtree(preExistingGridLines)
	viableSet=[]
	for currentNode in nonViableSet:
		print currentNode.getHouseholds()
		current_node=calculateYears(currentNode,idx,preExistingGridLines)
		if current_node.getYears()==0:
			viableSet.append(currentNode)
	return viableSet

def createRtree(preExistingGridLines):
	idx = index.Index()
	for pos, poly in enumerate(preExistingGridLines):
		idx.insert(pos, poly.bounds)
	return idx


def decrementremainingSet(nonViableSet,viableSet):
	for item in viableSet:
		nonViableSet.remove(item)
	return nonViableSet

def getIndex_LeastMV_hh(viableSet):
	minMV_hh=10000
	index=0
	for item in viableSet:
		item_mv_hh=calculateDistance(item.getLongitude(),item.getLatitude(),item.getNearestGrid_x(),item.getNearestGrid_y())/item.getHouseholds()
		if minMV_hh>item_mv_hh:
			minMV_hh=item_mv_hh
			index=item
	return index

def addLinetoLinesList(pt1_x,pt1_y,pt2_x,pt2_y,preExistingGridLines):
	preExistingGridLines.append(LineString([Point(pt1_x,pt1_y),Point(pt2_x,pt2_y)]))
	print "length of lines list"
	print len(preExistingGridLines)
	return preExistingGridLines

def addLine(current_node,year,proposed,preExistingGridLines):
	proposed.line(parts=[[[float(current_node.getLongitude()),float(current_node.getLatitude())],[float(current_node.getNearestGrid_x()),float(current_node.getNearestGrid_y())]]])
	preExistingGridLines=addLinetoLinesList(float(current_node.getLongitude()),float(current_node.getLatitude()),float(current_node.getNearestGrid_x()),float(current_node.getNearestGrid_y()),preExistingGridLines)
	current_node.setDistance(1000*calculateDistance(float(current_node.getLongitude()),float(current_node.getLatitude()),float(current_node.getNearestGrid_x()),float(current_node.getNearestGrid_y())))
	proposed.record(int(year))
	current_node.setNPV_grid(current_node.getNPV_grid())
	current_node.setCurrentDemand(current_node.getStartDemand()*((1.25)**(year/2)))
	offgrid_initialcost,offgrid_recurrcost,discountFactor_offgrid=offGridCosts(current_node)
	offgrid_cost=offgrid_initialcost+offgrid_recurrcost*discountFactor_offgrid
	solarminigrid_initialcost,solarminigrid_recurcost,discountFactor_minigrid=miniSolarGridCosts(current_node)
	miniSolargrid_cost=solarminigrid_initialcost+solarminigrid_recurcost*discountFactor_minigrid
	minimum_cost=min(offgrid_cost,miniSolargrid_cost)
	if year<=5:
		current_node.setNPV_temp(offgrid_cost)
		current_node.setOffGridCost_Initial(offgrid_initialcost)
		current_node.setOffGridCost_recurr(offgrid_recurrcost)
		current_node.setDiscountFact_offgrid(discountFactor_offgrid)
	elif year>=6 and year<10:
		current_node.setNPV_temp(miniSolargrid_cost)
		current_node.setSolarMinigridCost_Initial(solarminigrid_initialcost)
		current_node.setSolarMinigridCost_recurr(solarminigrid_recurcost)
		current_node.setDiscountFact_solarminigrid(discountFactor_minigrid)
	elif year>=10 and year<16:
		if current_node.getHouseholds()>20:
			current_node.setNPV_temp(miniSolargrid_cost)
			current_node.setSolarMinigridCost_Initial(solarminigrid_initialcost)
			current_node.setSolarMinigridCost_recurr(solarminigrid_recurcost)
			current_node.setDiscountFact_solarminigrid(discountFactor_minigrid)
		else:
			current_node.setNPV_temp(offgrid_cost)
			current_node.setOffGridCost_Initial(offgrid_initialcost)
			current_node.setOffGridCost_recurr(offgrid_recurrcost)
			current_node.setDiscountFact_offgrid(discountFactor_offgrid)
	else:
		current_node.setCurrentDemand(current_node.getStartDemand())
		offgrid_initialcost,offgrid_recurrcost,discountFactor_offgrid=offGridCosts(current_node)
		offgrid_cost=offgrid_initialcost+offgrid_recurrcost*discountFactor_offgrid
		current_node.setNPV_temp(offgrid_cost)
		current_node.setOffGridCost_Initial(offgrid_initialcost)
		current_node.setOffGridCost_recurr(offgrid_recurrcost)
		current_node.setDiscountFact_offgrid(discountFactor_offgrid)
	current_node.setYear(year)
	return proposed,current_node,preExistingGridLines
	
def increaseCurrentDemand(nonViableSet,year):
	for item in nonViableSet:
		item.setCurrentDemand(item.startDemand*(1.25**year))
	return nonViableSet

def runBorvuka(viableSet,nonViableSet,preExistingGridLines,proposed,maxyears):
	t=2
	completedSet=[]
	while t<=maxyears:
		run=0
		while run<3:
			print "t "+ str(t)
			nonViableSet = increaseCurrentDemand(nonViableSet,t)
			print " demand for this t "+ str(nonViableSet[0].getCurrentDemand())
			#print "viableSet "+ str(viableSet)
			print "completedSet "+ str(len(completedSet))
			if viableSet==[]:
				viableSet=calculateViableSet(nonViableSet,preExistingGridLines)
				nonViableSet=decrementremainingSet(nonViableSet,viableSet)
				print "viableSet"+ str(len(viableSet))
				while viableSet!=[]:
					viableSet = increaseCurrentDemand(viableSet,t)
					index=getIndex_LeastMV_hh(viableSet)
					proposed,current_node,preExistingGridLines=addLine(index,t,proposed,preExistingGridLines)
					completedSet.append(current_node)
					viableSet.remove(index)
					calculateViableSet(viableSet,preExistingGridLines)
			#print "viableSet "+ str(viableSet)
			#print "remainingSet "+ str(nonViableSet)
			run+=1
		print "----------------------"
		t+=1
	return proposed,completedSet

def createShapefile():
	proposed = shapefile.Writer(shapefile.POLYLINE)
	proposed.field('time','N','40')
	return proposed

def closeShapefile(proposed,outputfilepath):
	proposed.save(outputfilepath+'/line_file')


def initialize(latitudeList,longitudeList,hhList,inputfilepath,outputfilepath):
	#initialized a list of objects with each object representing a node
	NodeList = [node(count,longitudeList[count],latitudeList[count],hhList[count]) for count in xrange(len(longitudeList))]

	#convert shapefile to linestrings 
	preExistingGridLines=PreExistingGrid(inputfilepath)

	# Initialize Viable and Non Viable Sets
	viableSet,nonViableSet=createSets(NodeList)

	#create shapefile
	proposed=createShapefile()

	# Run Boruvka's
	proposed,completedSet=runBorvuka(viableSet,nonViableSet,preExistingGridLines,proposed,16)

	#close Shapefile
	closeShapefile(proposed,outputfilepath)

	#create Plots
	NodeList = [node(count,longitudeList[count],latitudeList[count],hhList[count]) for count in xrange(len(longitudeList))]
	createPlots.households_perc_time(NodeList,completedSet,inputfilepath,outputfilepath,16)
	createPlots.NPV_time(NodeList,completedSet,inputfilepath,outputfilepath,16)
	createPlots.lengthWire_time(NodeList,completedSet,inputfilepath,outputfilepath,16)
	createPlots.plotRevenue(NodeList,completedSet,outputfilepath,16)
	createPlots.plotValue(NodeList,completedSet,outputfilepath,16)

	# Save Nodelist as csv file
	saveData.toCsv(NodeList,completedSet,outputfilepath)