#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Jamie
#
# Created:     20/11/2012
# Copyright:   (c) Jamie 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

newCSV = 'C:/stats.csv'
with open(newCSV,'wb') as csvfile:
    writer = csv.writer(csvfile)
    write = writer.writerow
    lyr = arcpy.MakeFeatureLayer_management(r'G:\4_GISstaff\Jamie\RBWTv2_laurelStuff_results\results.gdb\modeled_ws')
    slyr = arcpy.MakeFeatureLayer_management(r'G:\4_GISstaff\Jamie\RBWTv2_laurelStuff_results\results.gdb\streams_BAARI_NHD')
    for row in arcpy.SearchCursor("modeled_ws"):
        arcpy.SelectLayerByAttribute_management(lyr,"NEW_SELECTION",'"Name"='+str(row.Name))
        arcpy.SelectLayerByLocation_management(slyr,"INTERSECT",lyr,'',"NEW_SELECTION")
        arcpy.SelectLayerByAttribute_management(slyr,"SUBSET_SELECTION",'"WetlandTyp"=\'FSD\'')
        stat = arcpy.Statistics_analysis(slyr,'stat.dbf',['Shape_Length','SUM'])
        writeStat = ''
        for row in arcpy.SearchCursor(stat):
            writeStat = row.SUM_Shape_Length
        line = [str(row.Name),writeStat]
        write(line)
        arcpy.Delete_management(stat)