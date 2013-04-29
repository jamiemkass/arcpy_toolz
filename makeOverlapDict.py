def makeOverlapDict(fc, returnID = None):
    """Returns a dict relating each feature to each
    feature that overlaps it, based on the param 'returnID'."""
    fcName = arcpy.Describe(fc).name
    if not returnID:
        returnID = 'FID_' + fcName
        returnID2 = 'FID_' + fcName + '_1'
    else:
        returnID2 = returnID + '_1'

    identity = arcpy.Identity_analysis(fc, fc, fcName + 'ID')

    overlapDict = {}
    with arcpy.da.SearchCursor(identity, (returnID, returnID2)) as cursor:
        for row in cursor:
            if row[0] <> row[1]:
                if not overlapDict.get(row[0]):
                    overlapDict[row[0]] = [row[1]]
                else:
                    overlapDict[row[0]].append(row[1])

    for oid in overlapDict.iterkeys():
        overlapDict[oid] = list(set(overlapDict[oid]))

    arcpy.Delete_management(identity)

    return overlapDict