#
# Contact between four mushrooms and rough surface
#
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from regionToolset import *
from visualization import *
from connectorBehavior import *
import boundaryUtils

#
# Create a model
#
tmpModel = mdb.Model(name='tmp')
if mdb.models.has_key('Model-1'):
  del mdb.models['Model-1']
if mdb.models.has_key('AdhesionSingleSurf'):
  del mdb.models['AdhesionSingleSurf']
if mdb.models.has_key('AdhesionTest5'):
  del mdb.models['AdhesionTest5']
if mdb.models.has_key('AdhesionTest6'):
  del mdb.models['AdhesionTest6']

# myModel = mdb.ModelFromInputFile(inputFileName=
#     '/tmp/banerjee/Adhesion/AdhesionSingleSurf.inp', name='AdhesionTest5')
myModel = mdb.Model(name='AdhesionTest6')
myAssem = myModel.rootAssembly
del mdb.models['tmp']

#
# Input dimensions (mm)
#
rStem = 0.5         # Stem radius
lStem = 1.0         # Stem length
lPlate = 2.5        # Distance between stems (plate length)
tPlate = 1.0        # Plate thickness
tCup = 0.296        # Cup thickness
rCupOut = 1.5       # Cup outer radius
rCupIn = 1.35       # Cup inner radius
rFillet = 0.021     # Fillet radius
meshSize = 0.068    # Element size
blockSize = 8       # Size of the rough surface block
#
# Derived parameters
#
theta = asin(rStem/rCupOut)
xc = 0.0
yc = -(rCupOut*cos(theta) - tCup)
x1 = 0.0
y1 = 0.0
x2 = 0.0
y2 = tCup
x3 = 0.0
y3 = y2+lStem
x4 = 0.0
y4 = y3+tPlate
x5 = -0.5*lPlate
y5 = y4
x6 = x5
y6 = y3
x7 = -rStem
y7 = y6
x8 = x7
y8 = y2
x9 = -sqrt(rCupOut*rCupOut-yc*yc)
y9 = 0.0
x10 = -sqrt(rCupIn*rCupIn-yc*yc)
y10 = 0.0
x11 = 0.0
y11 = rCupIn + yc
x12 = x7
y12 = y4
#
# Create a sketch of the part
#
# Sketch of top plate
#
skPlate = myModel.ConstrainedSketch(name='Plate', sheetSize=10.0)
skPlate.ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
skPlate.Line(point1=(x3, y3), point2=(x4, y4))
skPlate.Line(point1=(x4,y4), point2=(x5, y5))
skPlate.Line(point1=(x5, y5), point2=(x6, y6))
skPlate.Line(point1=(x6, y6), point2=(x3, y3))
prtPlate = myModel.Part(dimensionality=THREE_D, name='Plate', type=DEFORMABLE_BODY)
prtPlate.BaseSolidExtrude(depth=0.5*lPlate, sketch=skPlate)
del skPlate
#
# Sketch of stem + cup
#
skStemCup = myModel.ConstrainedSketch(name='Stem', sheetSize=10.0)
skStemCup.ConstructionLine(point1=(0.0, -5.0), point2=(0.0, 5.0))
skStemCup.Line(point1=(x11, y11), point2=(x2, y2))
skStemCup.Line(point1=(x2, y2), point2=(x3, y3))
skStemCup.Line(point1=(x3, y3), point2=(x4, y4))
skStemCup.Line(point1=(x4, y4), point2=(x12, y12))
skStemCup.Line(point1=(x12, y12), point2=(x7, y7))
line1 = skStemCup.Line(point1=(x7, y7), point2=(x8, y8))
arc1 = skStemCup.ArcByCenterEnds(center=(xc, yc), direction=COUNTERCLOCKWISE, point1=(x8, y8), point2=(x9, y9))
line2 = skStemCup.Line(point1=(x9, y9), point2=(x10, y10))
arc2 = skStemCup.ArcByCenterEnds(center=(xc, yc), direction=CLOCKWISE, point1=(x10, y10), point2=(x11, y11))
skStemCup.FilletByRadius(radius=rFillet, curve1=line1, curve2=arc1, nearPoint1=(x8,y8+rFillet), 
  nearPoint2=(x8-rFillet,y8-rFillet))
skStemCup.FilletByRadius(radius=rFillet, curve1=arc1, curve2=line2, nearPoint1=(x9+rFillet,y9+rFillet), 
  nearPoint2=(x9+rFillet,y9))
skStemCup.FilletByRadius(radius=2*rFillet, curve1=line2, curve2=arc2, nearPoint1=(x10-rFillet,y10), 
  nearPoint2=(x10+rFillet,y10+rFillet))
prtStemCup = myModel.Part(dimensionality=THREE_D, name='StemCup', type=DEFORMABLE_BODY)
prtStemCup.BaseSolidRevolve(angle=90.0, flipRevolveDirection=OFF, sketch=skStemCup)
del skStemCup
#
# Create instances of plate and stem + cup
#
instPlate = myAssem.Instance(dependent=ON, name='instPlate', part=prtPlate)
instStemCup = myAssem.Instance(dependent=ON, name='instStemCup', part=prtStemCup)
#
# Do boolean merge of the two instances and create a new part
#
instQtrMushroom = myAssem.InstanceFromBooleanMerge(domain=GEOMETRY, instances=(instPlate, instStemCup),
  keepIntersections=ON, name='QtrMushroom', originalInstances=DELETE)
prtQtrMushroom = myModel.parts['QtrMushroom']
#
# Delete the parts and instances that are not needed any more
#
del myModel.parts[prtPlate.name]
del myModel.parts[prtStemCup.name]
#
# Mesh the part
#
prtQtrMushroom.seedPart(deviationFactor=0.1, size=meshSize)
prtQtrMushroom.setMeshControls(regions=prtQtrMushroom.cells.getSequenceFromMask(('[#4 ]', ), ), 
  technique=BOTTOM_UP)
prtQtrMushroom.setElementType(elemTypes=(
    ElemType(elemCode=C3D8H, elemLibrary=STANDARD), ElemType(elemCode=C3D6, 
    elemLibrary=STANDARD), ElemType(elemCode=C3D4, elemLibrary=STANDARD)), 
    regions=(prtQtrMushroom.cells.getSequenceFromMask(('[#7 ]', ), ), ))
prtQtrMushroom.setMeshControls(algorithm=ADVANCING_FRONT, 
  regions=prtQtrMushroom.cells.getSequenceFromMask(('[#3 ]', ), ), technique=SWEEP)
cellPt = (0.5*(x2+x3), 0.5*(y2+y3), 0)
sourceFacePt = (0.5*(x3+x7), 0.5*(y2+y3), 0)
sourceCellSeq = boundaryUtils.getCell(prtQtrMushroom, cellPt)
sourceFaceSeq = boundaryUtils.getFace(prtQtrMushroom, sourceFacePt)
prtQtrMushroom.generateBottomUpRevolvedMesh(angleOfRevolution=90.0, axisOfRevolution=((xc,yc,0),(x1,y1,0)),
  cell=sourceCellSeq[0], geometrySourceSide=Region(faces=sourceFaceSeq), numberOfLayers=10)
assocFacePt = (0.5*(x3+x7), y3, 0)
assocFaceSeq = boundaryUtils.getFace(prtQtrMushroom, assocFacePt)
ee = prtQtrMushroom.elementFaces
pickedElemFaces = ee.getSequenceFromMask(mask=(
    '[#1008 #0:2 #8 #0:4 #10000000 #0:4 #1004', 
    ' #0:23 #100800 #0:2 #800 #0:5 #10 #0:3', 
    ' #100400 #0:23 #10080000 #0:2 #80000 #0:5 #1000', 
    ' #0:3 #10040000 #0:23 #8000000 #10 #0 #8000000', 
    ' #0:5 #100000 #0:3 #4000000 #10 #0:23 #1008', 
    ' #0:2 #8 #0:4 #10000000 #0:4 #1004 #0:23', 
    ' #100800 #0:2 #800 #0:5 #10 #0:3 #100400', 
    ' #0:23 #10080000 #0:2 #80000 #0:5 #1000 #0:3', 
    ' #10040000 #0:23 #8000000 #10 #0 #8000000 #0:5', 
    ' #100000 #0:3 #4000000 #10 #0:23 #1008 #0:2', 
    ' #8 #0:4 #10000000 #0:4 #1004 #0:23 #100800', 
    ' #0:2 #800 #0:5 #10 #0:3 #100400 #0:23', 
    ' #10000 #0:3 #10000 #0:3 #10000 #0:3 #10000', 
    ' #0:3 #10000 #0:3 #10000 #0:3 #10000 #0:3', 
    ' #10000 #0:3 #10000 #0:3 #10000 ]', ), )
ff = prtQtrMushroom.faces
prtQtrMushroom.associateMeshWithGeometry(geometricEntity=ff.findAt(coordinates=assocFacePt),
  elemFaces=pickedElemFaces)
prtQtrMushroom.generateMesh(regions=
    prtQtrMushroom.cells.getSequenceFromMask(
    ('[#2 ]', ), ))
prtQtrMushroom.generateMesh(regions=
    prtQtrMushroom.cells.getSequenceFromMask(
    ('[#1 ]', ), ))
myAssem.regenerate()
#
# Create duplicate instances
#
instQtrMushroom2 = myAssem.Instance(dependent=ON, name='QtrMushroom-2', part=prtQtrMushroom)
instQtrMushroom2.rotateAboutAxis(angle=90.0, axisDirection=(0.0, 1.0, 0.0), axisPoint=(xc, yc, 0.0)) 
instQtrMushroom3 = myAssem.Instance(dependent=ON, name='QtrMushroom-3', part=prtQtrMushroom)
instQtrMushroom3.rotateAboutAxis(angle=-90.0, axisDirection=(0.0, 1.0, 0.0), axisPoint=(xc, yc, 0.0)) 
instQtrMushroom4 = myAssem.Instance(dependent=ON, name='QtrMushroom-4', part=prtQtrMushroom)
instQtrMushroom4.rotateAboutAxis(angle=180.0, axisDirection=(0.0, 1.0, 0.0), axisPoint=(xc, yc, 0.0)) 
#
# Merge the instances to create full mushroom
#
prtMushroom = myAssem.PartFromBooleanMerge(domain=MESH, 
    instances=(instQtrMushroom, instQtrMushroom2, instQtrMushroom3, instQtrMushroom4),
    mergeNodes=BOUNDARY_ONLY, name='Mushroom', nodeMergingTolerance=1e-06)
instMushroom = myAssem.Instance(dependent=ON, name='Mushroom-1', part=prtMushroom)
#
# Delete the parts and instances that are not needed any more
#
del myAssem.instances[instQtrMushroom.name]
del myAssem.instances[instQtrMushroom2.name]
del myAssem.instances[instQtrMushroom3.name]
del myAssem.instances[instQtrMushroom4.name]
#
# Rotate the instance 90 degrees about the x axis
#
instMushroom.rotateAboutAxis(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0)) 
#
# Create a pattern of four whole mushrooms
#
# instMushroom2 = myAssem.Instance(dependent=ON, name='Mushroom-2', part=prtMushroom)
# instMushroom2.rotateAboutAxis(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0)) 
# instMushroom2.translate((lPlate, 0, 0))
# instMushroom3 = myAssem.Instance(dependent=ON, name='Mushroom-3', part=prtMushroom)
# instMushroom3.rotateAboutAxis(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0)) 
# instMushroom3.translate((0, lPlate, 0))
# instMushroom4 = myAssem.Instance(dependent=ON, name='Mushroom-4', part=prtMushroom)
# instMushroom4.rotateAboutAxis(angle=90.0, axisDirection=(1.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0)) 
# instMushroom4.translate((lPlate, lPlate, 0))
#
# Merge the instances to create four mushrooms
#
# prtFourMushroom = myAssem.PartFromBooleanMerge(domain=MESH, 
#     instances=(instMushroom, instMushroom2, instMushroom3, instMushroom4),
#     mergeNodes=BOUNDARY_ONLY, name='FourMushroom', nodeMergingTolerance=1e-06)
# instFourMushroom = myAssem.Instance(dependent=ON, name='FourMushroom-1', part=prtFourMushroom)
#
# Delete the parts and instances that are not needed any more
#
# del myAssem.instances[instMushroom.name]
# del myAssem.instances[instMushroom2.name]
# del myAssem.instances[instMushroom3.name]
# del myAssem.instances[instMushroom4.name]
#
# Translate the mushrooms to sit over block
#
# instFourMushroom.translate((0.35*blockSize, 0.35*blockSize, 0))
