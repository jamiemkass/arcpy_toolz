def makeExplodeDict(fc, overlapDict, returnID = None):
    """Returns dict relating each feature to an 'explode value',
    which separates all features into non-overlapping groups. Calls
    makeOverlapDict."""
    if not overlapDict:
        return
    if not returnID:
        returnID = arcpy.Describe(fc).oidFieldName
    # set initial explode value to 1
    expl = 1
    # create dictionary to hold explode values of oids
    explDict = {}
    overlapDict2 = overlapDict.copy()
    # while there are still keys in overlapDict2 not also in explDict
    while len([k for k in overlapDict2.iterkeys() if not explDict.get(k)]) > 0:
        # create list to hold overlapping oids
        ovSet = set()
        # loop over overlapDict2
        for oid, ovlps in overlapDict2.iteritems():
            if not explDict.get(oid) and oid not in ovSet:
                explDict[oid] = expl
                for o in ovlps:
                    ovSet.add(o)
        for oid in explDict.iterkeys():
            if overlapDict2.get(oid):
                del overlapDict2[oid]
        expl += 1

    # Add remaining non-overlapping oids into explDict and give them a random expl value
    explVals = list(set(explDict.itervalues()))
    query = str(tuple(explDict.keys()))
    fillVals = []
    with arcpy.da.SearchCursor(fc, (returnID), '"{0}" NOT IN '.format(returnID) + query) as cursor:
        for row in cursor:
            fillVals.append(row[0])
    for val in fillVals:
        explDict[val] = random.choice(explVals)

    return explDict