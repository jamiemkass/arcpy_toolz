def adjacentLinesDict(line, idField):
    """Returns a dict relating each line ID with
    all line IDs of adjacent lines, separated by
    those adjacent at the end and start."""
    ptsGeom = {'startPts': {}, 'endPts': {}}
    with arcpy.da.SearchCursor(line, (idField, "SHAPE@")) as cursor:
        for row in cursor:
            x1 = row[1].firstPoint.X
            y1 = row[1].firstPoint.Y
            x2 = row[1].lastPoint.X
            y2 = row[1].lastPoint.Y

            if ptsGeom["startPts"].get((x1, y1)):
                ptsGeom["startPts"][(x1, y1)].append(row[0])
            else:
                ptsGeom["startPts"][(x1, y1)] = [row[0]]

            if ptsGeom["endPts"].get((x2, y2)):
                ptsGeom["endPts"][(x2, y2)].append(row[0])
            else:
                ptsGeom["endPts"][(x2, y2)] = [row[0]]

    return ptsGeom