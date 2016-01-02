import ogr,csv,sys
import argparse
import shapefile
import os
import gdal

# converts each input shapefile into a csv file
def convertShptoCsv(shpfile,csvfile):
    count=0
    if not os.path.isfile(csvfile):
        count =count+1
        raise IOError('Could not find file ' + str(filename1))

    source = ogr.Open(shpfile, gdal.GA_Update)
    if source is None:
        count = count +1
        raise IOError('Could open file ' + str(shpfile))
    if count==0:
        csvfile=open(csvfile,'wb')
        ds=ogr.Open(shpfile)
        lyr=ds.GetLayer()
        dfn=lyr.GetLayerDefn()
        nfields=dfn.GetFieldCount()
        #print nfields
        fields=[]
        for i in range(nfields):
            fields.append(dfn.GetFieldDefn(i).GetName())
            #print dfn.GetFieldDefn(i).GetName()
        fields.append('kmlgeometry')
        csvwriter = csv.DictWriter(csvfile, fields)
        csvwriter.writeheader()
        #csvfile.write(','.join(fields)+'\n')
        for feat in lyr:
            #print feat
            attributes=feat.items()
            geom=feat.GetGeometryRef()
            #print geom
            attributes['kmlgeometry']=geom.ExportToKML()
            csvwriter.writerow(attributes)
        del csvwriter,lyr,ds
        csvfile.close()

def convertCsvtoData(filename1,filename2):
    point1a = []
    point1b = []
    point2a = []
    point2b = []
    with open(filename1, 'r') as csvfile:
        csvfile.next()
        c1 = csv.reader(csvfile)
        for hosts_row in c1:
            row = hosts_row[1]
            row = row.replace('<LineString><coordinates>','')
            row = row.replace('</coordinates></LineString>','')
            temp = row.split(' ',1)[0]
            temp1 = round(float(temp.split(',',1)[0]),9)
            temp2 = round(float(temp.split(',',1)[1]),9)
            point1a.append(str(temp1))
            point1b.append(str(temp2))
            temp = row.split(' ',1)[1]
            temp1 = round(float(temp.split(',',1)[0]),9)
            temp2 = round(float(temp.split(',',1)[1]),9)
            point2a.append(str(temp1))
            point2b.append(str(temp2))
    #for i in range(len(point1a)):
    #    print str(point1a[i])+" : "+str(point1b[i])
    latitudeList=[]
    longitudeList=[]
    with open(filename2, 'r') as csvfile:
            csvfile.next()
            c1 = csv.reader(csvfile)
            for hosts_row in c1:
                latitudeList.append(str(round(float(hosts_row[3]),9)))
                longitudeList.append(str(round(float(hosts_row[2]),9)))
    index1=[0]*len(point1a)
    index2=[0]*len(point1b)
    for i in range(0,len(point1a)):
        index1[i]=longitudeList.index(point1a[i])
        index2[i]=longitudeList.index(point2a[i])
        #print str(index1[i]) + " " +str(index2[i])
    return index1,index2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="convert shapefiles into csv files")
    parser.add_argument('shapefile_path_name', type=str, help="type folder/shapefile_name.shp")
    parser.add_argument('outputcsv_path_name', type=str,help="type folder/csvname.csv")
    parser.add_argument('originalcsv_path_name', type=str,help="type folder/csvname.csv")
   

    args = parser.parse_args()
    filename1 = '%s.shp' % args.shapefile_path_name 
    filename2 = '%s.csv' % args.outputcsv_path_name 
    filename3 = '%s.csv' % args.originalcsv_path_name
    shpfile=filename1
    csvfile=filename2
    convertShptoCsv(shpfile,csvfile)
    convertCsvtoData(csvfile,filename3)
    