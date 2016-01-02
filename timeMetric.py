from math import radians, cos, sin, asin, sqrt
import csv
import argparse, glob
import os
import numpy as np
import ogr,sys
import shapefile
import gdal
import pandas as pd
from sympy import *
import mst, offgrid, minigrid, internalGrid, backtrack, network

def main():
	parser = argparse.ArgumentParser(description="convert shapefiles into csv files")
	parser.add_argument('csv1', type=str, help="type folder/csvname minus the csv")
	parser.add_argument('inputfilepath', type=str, help="type folder/csvname minus the csv")
	parser.add_argument('outputfilepath', type=str, help="type folder/csvname minus the csv")
	args = parser.parse_args()
	filename1 = '%s.csv' % args.csv1
	inputfilepath = '%s' % args.inputfilepath
	outputfilepath = '%s' % args.outputfilepath
	if not os.path.isfile(filename1):
		print 'Could not find file ' + str(filename1)
	else:
		row_count = 0
		latitudeList=[]
		longitudeList=[]
		hhList=[]
		demandList=[]
		gridList=[]
		mvmax_NP=[]
		hh_grid_NP=[]
		with open(filename1, 'r') as csvfile:
			csvfile.next()
			c1 = csv.reader(csvfile)
			for hosts_row in c1:
				row_count+=1
				#print hosts_row
				if float(hosts_row[1]>5000):
					hhList.append(float(hosts_row[1])/5.8)
				else:
					hhList.append(float(hosts_row[1])/6.1)
				latitudeList.append(float(hosts_row[3]))
				longitudeList.append(float(hosts_row[2]))
			print sum(hhList)
			network.initialize(latitudeList,longitudeList,hhList,inputfilepath,outputfilepath)
	

if __name__=='__main__':
	main()
