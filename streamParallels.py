def streamParallels(streams, joinList, bankDistField, outLoc):
    """This function creates stream parallels from stream lines. These
    parallels are a defined distance from the stream based on the value of
    the bank distance field, and are used to buffer out from the estimated stream banks."""
    lyrs=[]
    # Create left and Right standard bank distance buffers, add direction field
    arcpy.Buffer_analysis(streams, "strBufL", bankDistField, "LEFT", "FLAT")
    arcpy.AddField_management("strBufL", "dir", "TEXT")
    arcpy.CalculateField_management("strBufL", "dir", '"L"', "VB")
    arcpy.Buffer_analysis(streams, "strBufR", bankDistField, "RIGHT", "FLAT")
    arcpy.AddField_management("strBufR", "dir", "TEXT")
    arcpy.CalculateField_management("strBufR", "dir", '"R"', "VB")
    # Merge buffers in preparation for spatial join
    arcpy.Merge_management(["strBufL", "strBufR"], "strLRbufs")
    # Convert buffer to polyline
    arcpy.PolygonToLine_management("strLRbufs", "strLRbufsLine", "IGNORE_NEIGHBORS")
    # Create points from each line end point
    arcpy.FeatureVerticesToPoints_management(streams, "strStartEndPts", "BOTH_ENDS")
    # Buffer each end point by 0.1 m
    arcpy.Buffer_analysis("strStartEndPts", "strStartEndPtsBuf", 0.1)
    # Split the polyline at vertices to render each line segment selectable
    strLRbufsLineSplit = arcpy.SplitLine_management("strLRbufsLine", "in_memory\\strLRbufsLineSplit")
    # Make layers of buffer polyline and end points for selection
    lineLyr = arcpy.MakeFeatureLayer_management(strLRbufsLineSplit)
    lyrs.append(lineLyr)
    ptLyr = arcpy.MakeFeatureLayer_management("strStartEndPtsBuf")
    lyrs.append(ptLyr)
    # Select all line segments that intersect with the point buffers and delete them
    arcpy.SelectLayerByLocation_management(lineLyr, "INTERSECT", ptLyr, '', "NEW_SELECTION")
    arcpy.DeleteRows_management(lineLyr)
    # Erase the center line
    parallelsE = arcpy.Erase_analysis(strLRbufsLineSplit, streams, "in_memory\\parallelsE")
    # Dissolve on streamID to maintain unique segment shapes using the updated joinList
    # to preserve attributes
    joinList.append('dir')
    arcpy.Dissolve_management(parallelsE, "parallelsED", joinList, '', "SINGLE_PART")
    # Make unique parallel ID called pID (gets deleted later)
    arcpy.AddField_management('parallelsED', "pID", "LONG")
    oidFieldName = arcpy.Describe('parallelsED').oidFieldName
    arcpy.CalculateField_management('parallelsED', 'pID', '['+oidFieldName+']', 'VB')
    # Planarize the lines
    arcpy.FeatureToLine_management("parallelsED", "parallelsEDPlan", '', 'ATTRIBUTES')
    # Copy features because cleanDangles modifies geometry
    arcpy.CopyFeatures_management("parallelsEDPlan", "parallelsPreD")
    pLyr = arcpy.MakeFeatureLayer_management("parallelsPreD")
    lyrs.append(pLyr)
    arcpy.SelectLayerByLocation_management(pLyr, "INTERSECT", streams, '', "NEW_SELECTION")
    arcpy.DeleteRows_management(pLyr)
    # This removes most overhanging line features
    geom.cleanDangles("parallelsPreD", 'pID', 'Shape_Length')
    joinList.append('pID')
    parallels = arcpy.Dissolve_management("parallelsPreD", outLoc+"\\parallels", joinList, '', 'SINGLE_PART')
    # Select all right parallels and flip, as they will be pointing in the wrong direction
    parLyr = arcpy.MakeFeatureLayer_management(parallels)
    lyrs.append(parLyr)
    arcpy.SelectLayerByAttribute_management(parLyr, "NEW_SELECTION", '"dir"=\'R\'')
    arcpy.FlipLine_edit(parLyr)

    # Delete layers
    for lyr in lyrs:
        arcpy.Delete_management(lyr)
    arcpy.Delete_management("in_memory")

    return parallels