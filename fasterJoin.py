def fasterJoin(fc,fcField,joinFC,joinFCField,fields,fieldsNewNames=None):
    """This function joins fields permanently much faster than JoinField. Optional
    parameter 'fieldsNewNames', entered as list of new names in same order as
    'fields', joins the fields with these names instead of the originals."""
    # Create joinList, which is a list of [name, type] for input fields
    listfields = arcpy.ListFields(joinFC)
    joinList = [[k.name,k.type] for k in listfields if k.name in fields]

    if fieldsNewNames:
        # Create list to collect old names
        oldNames = []
        # Replace original names with new names in joinList and append old ones to list
        for name, typ in joinList:
            oldNames.append(name)
            i = fields.index(name)
            joinList[joinList.index([name, typ])][0] = fieldsNewNames[i]\

    # As Field object types and AddField types have different names (shrug),
    # map object types to AddField types
    for name, typ in joinList:
        i = joinList.index([name, typ])
        if name in ['OBJECTID','Shape','Shape_Length','Shape_Area']:
            joinList = [k for k in joinList if k <> join]
        if typ == 'Integer':
            joinList[i] = [name,'LONG']
        elif typ == 'SmallInteger':
            joinList[i] = [name,'SHORT']
        elif typ == 'String':
            joinList[i] = [name,'TEXT']
        elif typ == 'Single':
            joinList[i] = [name,'FLOAT']

    # Add fields with associated names
    for name, typ in joinList:
        arcpy.AddField_management(fc,name,typ)
    # Get names of fc and joinFC to reference fields after join
    fcName = arcpy.Describe(fc).name
    joinFCName = arcpy.Describe(joinFC).name
    # Join tables
    arcpy.MakeFeatureLayer_management(fc,'fasterJoinLyr')
    arcpy.AddJoin_management('fasterJoinLyr',fcField,joinFC,joinFCField)

    # Calculate new fields as equal to joined fields
    # If fieldsNewNames, use oldNames instead of originals
    for join in joinList:
        newName = fcName+'.'+join[0]
        if fieldsNewNames:
            oldName = joinFCName+'.'+oldNames[joinList.index(join)]
            arcpy.CalculateField_management('fasterJoinLyr',newName,'['+oldName+']','VB')
        else:
            oldName = joinFCName+'.'+join[0]
            arcpy.CalculateField_management('fasterJoinLyr',newName,'['+oldName+']','VB')

    arcpy.Delete_management("fasterJoinLyr")