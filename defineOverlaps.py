def defineOverlaps(fc):
    """This function creates three fields: 'overlaps', which lists the OBJECTIDs
    of all other polygons overlapping each polygon, and 'ovlpCount', which counts
    the number of overlaps per feature, and 'expl', which separates all features
    into unique non-overlapping groups by value."""
    # If there are intersecting features, add overlap fields and expl values
    # If not, function ends

    # Build dicts used to relate each feature to all identical, overlapping shapes
    # Use fc OID as alternate OID instead of intersected fc OID
    overlapDict = makeOverlapDict(fc)

    if overlapDict:
        # Loop through overlapDict and give each oid an expl value that separates all oids into
        # non-overlapping groups
        explDict = makeExplodeDict(fc, overlapDict)

        # Add overlaps, ovlpCount, and expl fields
        arcpy.AddField_management(fc,'overlaps',"TEXT",'','',1000)
        arcpy.AddField_management(fc,'ovlpCount',"SHORT")
        arcpy.AddField_management(fc,'expl',"SHORT")

        # For each row with an overlapping poly (i.e. with an entry in idDict)
        # give overlaps value of all overlapping ids, ovlpCount value of how
        # many overlaps occur, and expl value that separates all features into
        # unique non-overlapping groups (explode value)

        t = time.clock()
        with arcpy.da.UpdateCursor(fc,("OID@","overlaps","ovlpCount","expl")) as cursor:
            for row in cursor:
                # If oid in overlapDict, write overlapping oids and their count
                # to the appropriate fields
                if overlapDict.get(row[0]):
                    row[1] = str(overlapDict[row[0]]).strip('[]')
                    row[2] = len(overlapDict[row[0]])
                # Write expl value to expl field
                row[3] = explDict[row[0]]
                cursor.updateRow(row)