# -*- coding: mbcs -*-
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
from visualization import *
from connectorBehavior import *
mdb.ModelFromInputFile(inputFileName=
    '/tmp/banerjee/Adhesion/AdhesionSingleSurf.inp', name='AdhesionSingleSurf')
mdb.openStep('/tmp/banerjee/Adhesion/BanerjeeTestPart.step', scaleFromFile=OFF)
mdb.models['AdhesionSingleSurf'].PartFromGeometryFile(combine=False, 
    dimensionality=THREE_D, geometryFile=mdb.acis, name='BanerjeeTestPart', 
    scale=0.1, stitchAfterCombine=False, type=DEFORMABLE_BODY)
mdb.models['AdhesionSingleSurf'].rootAssembly.Instance(dependent=ON, name=
    'BanerjeeTestPart-1', part=
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'])
mdb.models['AdhesionSingleSurf'].rootAssembly.rotate(angle=180.0, 
    axisDirection=(0.0, 3.0, 0.0), axisPoint=(0.0, -1.5, -1.7), instanceList=(
    'BanerjeeTestPart-1', ))
mdb.models['AdhesionSingleSurf'].rootAssembly.translate(instanceList=(
    'BanerjeeTestPart-1', ), vector=(19.205997, 16.799999, 9.929255))
mdb.models['AdhesionSingleSurf'].rootAssembly.translate(instanceList=(
    'BanerjeeTestPart-1', ), vector=(-0.000226, 0.0, 0.299869))
mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].createVirtualTopology(
    applyBlendControls=True, blendRadiusTolerance=0.27, 
    blendSubtendedAngleTolerance=60.0, cornerAngleTolerance=30.0, 
    faceAspectRatioThreshold=10.0, ignoreRedundantEntities=True, 
    mergeShortEdges=True, mergeSliverFaces=True, mergeSmallAngleFaces=True, 
    mergeSmallFaces=True, mergeThinStairFaces=True, shortEdgeThreshold=0.054, 
    smallFaceAreaThreshold=0.015, smallFaceCornerAngleThreshold=10.0, 
    thinStairFaceThreshold=0.011)
mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].createVirtualTopology(
    applyBlendControls=True, blendRadiusTolerance=0.27, 
    blendSubtendedAngleTolerance=60.0, cornerAngleTolerance=30.0, 
    faceAspectRatioThreshold=10.0, ignoreRedundantEntities=True, 
    mergeShortEdges=True, mergeSliverFaces=True, mergeSmallAngleFaces=True, 
    mergeSmallFaces=True, mergeThinStairFaces=True, shortEdgeThreshold=0.054, 
    smallFaceAreaThreshold=0.015, smallFaceCornerAngleThreshold=10.0, 
    thinStairFaceThreshold=0.011)
mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].PartitionCellByPlaneThreePoints(
    cells=
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].cells.getSequenceFromMask(
    ('[#1 ]', ), ), point1=
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].vertices[1], 
    point2=
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].InterestingPoint(
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].edges[2], 
    CENTER), point3=
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].InterestingPoint(
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].edges[3], 
    CENTER))
mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].PartitionCellByPlaneThreePoints(
    cells=
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].cells.getSequenceFromMask(
    ('[#1 ]', ), ), point1=
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].vertices[6], 
    point2=
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].InterestingPoint(
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].edges[4], 
    CENTER), point3=
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].InterestingPoint(
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].edges[4], 
    MIDDLE))
mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].PartitionCellByPlaneThreePoints(
    cells=
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].cells.getSequenceFromMask(
    ('[#4 ]', ), ), point1=
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].vertices[2], 
    point2=
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].InterestingPoint(
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].edges[1], 
    CENTER), point3=
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].InterestingPoint(
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].edges[8], 
    MIDDLE))
mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].PartitionCellByPlaneThreePoints(
    cells=
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].cells.getSequenceFromMask(
    ('[#c ]', ), ), point1=
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].InterestingPoint(
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].edges[12], 
    MIDDLE), point2=
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].InterestingPoint(
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].edges[10], 
    CENTER), point3=
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].vertices[5])
mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].seedPart(
    deviationFactor=0.1, size=0.54)
mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].setElementType(
    elemTypes=(ElemType(elemCode=C3D8H, elemLibrary=STANDARD), ElemType(
    elemCode=C3D6, elemLibrary=STANDARD), ElemType(elemCode=C3D4, 
    elemLibrary=STANDARD)), regions=(
    mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].cells.getSequenceFromMask(
    ('[#3f ]', ), ), ))
mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].generateMesh()
mdb.models['AdhesionSingleSurf'].HomogeneousSolidSection(material='ELASTOMER', 
    name='Section-Cup', thickness=None)
mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].SectionAssignment(
    offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdb.models['AdhesionSingleSurf'].parts['BanerjeeTestPart'].cells.getSequenceFromMask(
    mask=('[#3f ]', ), )), sectionName='Section-Cup')
mdb.models['AdhesionSingleSurf'].rootAssembly.Surface(name='TopContactSurface', 
    side1Faces=
    mdb.models['AdhesionSingleSurf'].rootAssembly.instances['BanerjeeTestPart-1'].faces.getSequenceFromMask(
    ('[#8260 ]', ), ))
