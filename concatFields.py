def concatFields(overlay):
    """This function takes all field values from correlate fields (e.g.: fieldname_1) 
    produced from an overlay operation and writes their values in the original fields 
    (e.g. fieldname), then deletes the correlate fields. This only works if no correlate 
    field's suffix number exceeds 9."""
    overlayName = arcpy.Describe(overlay).name
    # Gather lists of fields and correlate fields
    overlayFields = arcpy.ListFields(overlay)
    origFields = [k.name for k in overlayFields]
    # Make list of uneditable fields
    reqFields = [k.name for k in overlayFields if k.required == True]

    # Build dict to relate correlates to originals
    corFieldsDict = {}
    for orig in origFields:
        if orig[:-2] in origFields:
            corFieldsDict[orig] = orig[:-2]

    # Use this dict of only editable fields to edit values
    corFieldsDictEditable = dict((key,val) for (key,val) in corFieldsDict.items() if val not in reqFields)

    # Select all rows with no input1 FID: these are the ones we will move values to
    uLyr = arcpy.MakeFeatureLayer_management(overlayName+'Overlay')
    arcpy.SelectLayerByAttribute_management(uLyr,"NEW_SELECTION",'"{0}" = -1'.format(FIDfieldName))

    # Get a semicolon-delimited list of all fields and their correlates
    fields = ';'.join(corFieldsDictEditable.keys() + corFieldsDictEditable.values())

    # Update all the original fields with the correlate values
    with arcpy.UpdateCursor(uLyr,(fields)) as cursor:
        for row in cursor:
            for c in corFieldsDictEditable:
                row.setValue(corFieldsDictEditable[c],row.getValue(c))
            cursor.updateRow(row)

    # Delete all correlate fields, whether their parents are editable or not
    delFields = corFieldsDict.keys() + [k.name for k in overlayFields if k.name[:4] == 'FID_']
    arcpy.DeleteField_management(overlay,delFields)
    arcpy.Delete_management(uLyr)

    return overlay