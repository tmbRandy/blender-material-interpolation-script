import bpy

def set_texture_interpolation():
    for material in bpy.data.materials:
        if material.node_tree:
            for node in material.node_tree.nodes:
                if node.type == 'TEX_IMAGE':
                    node.interpolation = 'Closest'

def set_material_modes():
    for material in bpy.data.materials:
        material.use_nodes = True
        if material.node_tree:
            for node in material.node_tree.nodes:
                if node.type == 'OUTPUT_MATERIAL':
                    node.inputs[0].default_value = 'CLIP'  # Set Blend Mode to 'Alpha Clip'
                if node.type == 'OUTPUT_SHADOW':
                    node.inputs[0].default_value = 'CLIP'  # Set Shadow Mode to 'Alpha Clip'

def connect_alpha_nodes():
    for material in bpy.data.materials:
        if material.node_tree:
            image_nodes = [node for node in material.node_tree.nodes if node.type == 'TEX_IMAGE']
            bsdf_nodes = [node for node in material.node_tree.nodes if node.type == 'BSDF_PRINCIPLED']
            for image_node in image_nodes:
                for bsdf_node in bsdf_nodes:
                    material.node_tree.links.new(image_node.outputs['Alpha'], bsdf_node.inputs['Alpha'])

class SetTextureInterpolationOperator(bpy.types.Operator):
    bl_idname = "object.set_texture_interpolation"
    bl_label = "Set Texture Interpolation"
    
    def execute(self, context):
        set_texture_interpolation()
        return {'FINISHED'}

class SetMaterialModesOperator(bpy.types.Operator):
    bl_idname = "object.set_material_modes"
    bl_label = "Set Material Modes"
    
    def execute(self, context):
        set_material_modes()
        return {'FINISHED'}

class ConnectAlphaNodesOperator(bpy.types.Operator):
    bl_idname = "object.connect_alpha_nodes"
    bl_label = "Connect Alpha Nodes"
    
    def execute(self, context):
        connect_alpha_nodes()
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SetTextureInterpolationOperator.bl_idname)
    self.layout.operator(SetMaterialModesOperator.bl_idname)
    self.layout.operator(ConnectAlphaNodesOperator.bl_idname)

def register():
    bpy.utils.register_class(SetTextureInterpolationOperator)
    bpy.utils.register_class(SetMaterialModesOperator)
    bpy.utils.register_class(ConnectAlphaNodesOperator)
    bpy.types.VIEW3D_MT_object.prepend(menu_func)

def unregister():
    bpy.utils.unregister_class(SetTextureInterpolationOperator)
    bpy.utils.unregister_class(SetMaterialModesOperator)
    bpy.utils.unregister_class(ConnectAlphaNodesOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()
