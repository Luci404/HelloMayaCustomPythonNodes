import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import math, sys

def maya_useNewAPI():
    pass
    
# https://download.autodesk.com/us/maya/2011help/api/class_m_px_node.html
class helloWorldNode(om.MPxNode):
    id = om.MTypeId(0x7f001) #Unique ID https://download.autodesk.com/us/maya/2011help/API/class_m_type_id.html
    input = om.MObject()
    output = om.MObject()

    # Called by Maya, returns an instance of this node.
    @staticmethod
    def creator():
        print("[HelloMayaCustomPythonNodes] Creation is now happening...")
        return helloWorldNode()

    # Called by Maya at initialization.
    @staticmethod
    def initialize():
        print("[HelloMayaCustomPythonNodes] Initialization is now happening...")

        inNumericAttribute = om.MFnNumericAttribute()
        helloWorldNode.input = inNumericAttribute.create('input', 'i', om.MFnNumericData.kFloat, 0.0)
        inNumericAttribute.storable = True
        inNumericAttribute.writable = True

        outNumericAttribute = om.MFnNumericAttribute()
        helloWorldNode.output = outNumericAttribute.create('output', 'o', om.MFnNumericData.kFloat, 0.0)
        outNumericAttribute.storable = True
        outNumericAttribute.writable = True

        # The 'MPxNode.addAttribute(attr: om.MObject)' method adds a new attribute to a user defined node type during the type's initialization.
        helloWorldNode.addAttribute(helloWorldNode.input)
        helloWorldNode.addAttribute(helloWorldNode.output)

        # The 'MPxNode.attributeAffects(whenChanges: om.MObject, isAffected: om.MObject)' method specifies that a particular input attribute affects
        # a specific output attribute. This is required to make evaluation efficient. When an input changes, only the affected outputs will be computed.
        # Output attributes cannot be keyable - if they are keyable, this method will fail.
        helloWorldNode.attributeAffects( helloWorldNode.input, helloWorldNode.output)

    # Constructor
    def __init__(self):
        print("[HelloMayaCustomPythonNodes] Construction is now happening...")
        om.MPxNode.__init__(self)
    
    # Called by Maya, recompute the given output based on the nodes inputs. When an input changes, the compute method is called for each dependent output.
    def compute(self, plug, dataBlock):
        if (plug == helloWorldNode.output):
            print("Hello")
            dataHandle = dataBlock.inputValue(helloWorldNode.input)
            inputFloat = dataHandle.asFloat()
            result = math.sin(inputFloat) * 10.0
            outputHandle = dataBlock.outputValue(helloWorldNode.output)
            outputHandle.setFloat(result)
            dataBlock.setClean(plug)

def initializePlugin(obj):
    print("[HelloMayaCustomPythonNodes] Plugin initialization is now happening...")

    mplugin = om.MFnPlugin(obj)
    try:
        mplugin.registerNode('helloWorldNode', helloWorldNode.id, helloWorldNode.creator, helloWorldNode.initialize, om.MPxNode.kDependNode)
    except:
        sys.stderr.write(f"Failed to register node: {'helloWorldNode'}!")
        raise

def uninitializePlugin(mobject):
    print("[HelloMayaCustomPythonNodes] Plugin uninitialization is now happening...")

    mplugin = om.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(helloWorldNode.id)
    except:
        sys.stderr.write("fFailed to uninitialize node: {'helloWorldNode'}!")
        raise