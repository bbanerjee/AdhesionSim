def mask2find(part, cells='', faces='', edges='', verts=''): 
    c, f, e, v = part.cells, part.faces, part.edges, part.vertices
    if cells <> '':
        mycells = c.getSequenceFromMask(mask=(cells, ), )
        c1 = () 
        for mp in mycells.pointsOn: 
            c1 += ((mp[0], ), )
        print 'cells = c.findAt((%s,),' % c1[0]
        for cnt in range(1,len(c1)-1): 
           print '                 (%s,),' %c1[cnt]
        print '                 (%s,))' % c1[len(c1)-1]
    if faces <> '':
        myfaces = f.getSequenceFromMask(mask=(faces, ), )
        f1 = () 
        for mp in myfaces.pointsOn: 
            f1 += ((mp[0], ), )
        print 'faces = f.findAt((%s,),' % f1[0]
        for cnt in range(1,len(f1)-1):
            print '                 (%s,),' %f1[cnt]
        print '                 (%s,))' % f1[len(f1)-1]
    if edges <> '':
        myedges = e.getSequenceFromMask(mask=(edges, ), )
        e1 = ()
        for mp in myedges.pointsOn: 
            e1 += ((mp[0], ), )
        print 'edges = e.findAt((%s,),' % e1[0]
        for cnt in range(1,len(e1)-1):
            print '                 (%s,),' %e1[cnt]
        print '                 (%s,))' % e1[len(e1)-1]
    if verts <> '':
        myverts = v.getSequenceFromMask(mask=(verts, ), )
        v1 = ()
        for mp in myverts.pointsOn: 
            v1 += ((mp[0], ), )
        print 'verts = v.findAt((%s,),' % v1[0]
        for cnt in range(1,len(v1)-1):
            print '                 (%s,),' %v1[cnt]
        print '                 (%s,))' % v1[len(v1)-1]
#   return c1, f1, e1, v1 

