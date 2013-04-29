def fasterJoinAll(inFC,inField,joinFC,joinField,outName):
    """This function joins all fields permanently much faster than JoinField."""
    env.qualifiedFieldNames = False
    # Get list of field objects
    listfields = arcpy.ListFields(joinFC)
    # Make list of field names that are not required (i.e. OBJECTID, Shape, Length/Area)
    reqFields = [k.name for k in listfields if k.required==True]
    # Get names of inFC
    desc = arcpy.Describe(inFC)
    # Make layer of inFC
    inLyr = arcpy.MakeFeatureLayer_management(inFC,'inFC')
    # Add join and save to new fc
    arcpy.AddJoin_management(inLyr,inField,joinFC,joinField)
    joined = arcpy.CopyFeatures_management(inLyr,outName)
    # Delete original inFC and rename product to match it
    arcpy.Delete_management(inLyr)
    listFieldsOut = arcpy.ListFields(joined)
    # Delete repeat fields
    delFields = []
    for f in [k.name for k in listFieldsOut if k.name[-2:] == '_1']:
        delFields.append(f)
    arcpy.DeleteField_management(joined,delFields)
    env.qualifiedFieldNames = True
    return joined