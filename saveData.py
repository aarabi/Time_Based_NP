import matplotlib.pyplot as plt
import pandas as pd
import network, csv
import numpy as np

def toCsv(NodeList,completedSet,outputfilepath):
	f = open(outputfilepath+'/results.csv', 'wt')
	try:
		writer = csv.writer(f)
		writer.writerow( ('Households','Longitude','Latitude','ViableDemand','Year of Electrification','NPV_grid','NPV_temp') )
		for item in completedSet:
			writer.writerow( (item.getHouseholds(),item.getLongitude(),item.getLatitude(),item.getCurrentDemand(),item.getYears(),item.getNPV_grid(),item.getNPV_temp()))
	finally:
		f.close()
