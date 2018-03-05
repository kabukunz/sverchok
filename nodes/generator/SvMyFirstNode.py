# ##### BEGIN GPL LICENSE BLOCK #####
# ---snipped for brevity ------------
# ##### END GPL LICENSE BLOCK #######

import bpy
# import mathutils
# from mathutils import Vector
from bpy.props import FloatProperty, IntProperty
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

class SvMyFirstNode(bpy.types.Node, SverchCustomTreeNode):
    ''' MyFirstNode '''
    bl_idname = 'SvMyFirstNode'
    bl_label = 'MyFirstNode'
    bl_icon = 'GREASEPENCIL'

    Bones = IntProperty(
        name='Bones', description='bone chain',
        default=1, min=1, options={'ANIMATABLE'},
        update=updateNode)
    Size = FloatProperty(
        name='Size', description='Size',
        default=1.0, options={'ANIMATABLE'},
        update=updateNode)

    scene = bpy.context.scene
    ops = bpy.ops.object
    data = bpy.data.objects    
        
    armour = [scene, ops, data, bones, arm]

    def sv_init(self, context):
        self.inputs.new('StringsSocket', "Bones").prop_name = 'Bones'
        self.inputs.new('StringsSocket', "Arm").prop_name = 'Arm'
        self.outputs.new('VerticesSocket', "Vers")

    def draw_buttons(self, context, layout):
        pass

#---------- CreateBones -------------        
        
    def CreateBones(self):
    
        connect = False
        # connect = bpy.context.object.Bconnect 
        obj = bpy.context.active_object
        if obj.type != 'MESH':
            return{'FINISHED'}

        vtdat = []
        egdat = []
        pos = []
        cobj = obj
        
        cloc = cobj.location
        mesh = cobj.data
        vts = mesh.vertices
        eds = mesh.edges

        bpy.ops.object.mode_set(mode='OBJECT')
        for i in vts:
            pos.append(i.co.x)
            pos.append(i.co.y)
            pos.append(i.co.z)
            vtdat.append(pos)
            pos = []

        for i in eds:
#                if i.select:
            pos.append(i.vertices[0])
            pos.append(i.vertices[1])
            egdat.append(pos)
            pos = []

        if len(egdat) < 1:
            return{'FINISHED'}

        self.createArmature(cloc, egdat, vtdat)
        
        if not connect:
            self.connectbones(True)
        
        bpy.ops.object.mode_set(mode='OBJECT')
        return{'FINISHED'}

#---------- ConnectBones -------------

    def connectbones(self,mode):
        cobj = bpy.context.object
        amt = cobj.data
        bones = amt.edit_bones
        
        bpy.ops.object.mode_set(mode='EDIT')
        
        for i in bones:
            if i.select:
                for ii in bones:
                    if i != ii:
                        if i.head == ii.tail:
                            i.parent = ii
                            i.use_connect = mode
    
        return 1

#---------- createArmature -------------

    def createArmature(self, loc, eindex, vpos):

        bpy.ops.object.add(type='ARMATURE', enter_editmode=True, location=loc)
        ob = bpy.context.object
        ob.show_x_ray = True
        amt = ob.data
    
        ct = 0
        for i in eindex:
            bone = amt.edit_bones.new('bone')
            bone.head = vpos[eindex[ct][0]]
            bone.tail = vpos[eindex[ct][1]]
            ct += 1
        bpy.ops.armature.select_all(action='SELECT')
        bpy.ops.object.mode_set(mode='EDIT')
        return ob

#---------- setBones -------------

    def setBones(self, armour):
    
        # set bones as active object
        armour.bones.select = True
        # bones.select = True
        # scene.objects.active = bones
        armour.scene.objects.active = armour.bones
        
#---------- parentArmature -------------        
        
    def parentArmature(self, arm, armobj):
        
        # parent armature with auto weights

        # set object mode
        ops.mode_set(mode='OBJECT')
        
        # set armature as select object
        arm.select = True
        armature.select = True
        
        # set bones as active object
        scene.objects.active = armature
        
        # set relationship
        ops.parent_set(type='ARMATURE_AUTO')

#---------- checkRelations -------------      

    def checkRelations(self, data):        
        
        print ("QUI1")
        bones = data.get(bones_name)
        if bones is None or bones.type != 'MESH':
            print ("QUI2")
            return {'FINISHED'}
    
        arm = data.get(arm_name)    
        if arm is None or arm.type != 'MESH':
            print ("QUI3")
            return {'FINISHED'}
        
        print ("QUI2")
        
        # create a new armature ONCE
        armature = data.get("Armature")
        print (armature)        
        if armature is None or armature.type != 'ARMATURE':
            print ("QUI4")
            print (armature)
            setBones(bones)
            CreateBones()

        print ("QUI3")

        # check again for the sake of correctness    
        armature = data.get("Armature")
        print (armature)        
        if armature is None or armature.type != 'ARMATURE':
            print ("QUI5")
            print (armature)
            return {'FINISHED'}
            
        update = False        
    
        if update == False:
            parentArmature(arm,armature)

    def process(self):
        print("Hello There")

        inputs = self.inputs
        outputs = self.outputs

        # I think this is analoge to preexisting code, please verify.
        # size = inputs['Size'].sv_get()[0]
        bones = int(inputs['Bones'].sv_get()[0][0])
        arm = int(inputs['Arm'].sv_get()[0][0])
        # divz = int(inputs['Divz'].sv_get()[0][0])

        # scene = bpy.context.scene
        # ops = bpy.ops.object
        # data = bpy.data.objects    

        checkRelations()
        Verts = []

        # return in_sockets, out_sockets

        # out = [a for a in (zip(*[self.makecube(s, bones, divy, divz) for s in size]))]

        # outputs, blindly using sv_set produces many print statements.
        outputs['Vers'].sv_set(out[0])
        # outputs['Edgs'].sv_set(out[1])
        # outputs['Pols'].sv_set(out[2])

        self.debug("hello from the box")

def register():
    bpy.utils.register_class(SvMyFirstNode)


def unregister():
    bpy.utils.unregister_class(SvMyFirstNode)