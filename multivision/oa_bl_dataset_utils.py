import math
import os, random
import bpy
import cv2
import numpy as np
import glob
from oa_luxcore_materials import assign_pbr_material
from oa_file_utils import path_to_random_file

def import_random_stl(dir_path, dimensions=(1,1,1)):
    random_stl = random.choice(os.listdir(dir_path))
    full_path_stl = os.path.join(dir_path, random_stl)
    bpy.ops.import_mesh.stl(filepath=full_path_stl, global_scale=1.0)
    bl_obj_name = os.path.splitext(random_stl)[0]
    bl_obj = bpy.data.objects[bl_obj_name]
    bl_obj.scale[0]=1.0/bl_obj.dimensions[0]*dimensions[0]
    bl_obj.scale[1]=1.0/bl_obj.dimensions[1]*dimensions[1]
    bl_obj.scale[2]=1.0/bl_obj.dimensions[2]*dimensions[2]
    return bl_obj

def import_stl(path):
    #print(f'Path: {path}')
    bpy.ops.import_mesh.stl(filepath=path)
    bl_obj_name = os.path.basename(path)
    #print(f"Split: {bl_obj_name}")
    bl_obj_name = os.path.splitext(bl_obj_name)[0]
    bl_obj_name = bl_obj_name.capitalize()
    #print(f"Splitext: {bl_obj_name}")
    bl_obj = bpy.data.objects[bl_obj_name]
    return bl_obj

def set_hdri_luxcore(hdri_path, gain=1.0, z_rot = 0):
    bpy.context.scene.world.luxcore.gain = gain
    bpy.context.scene.world.luxcore.rotation = z_rot


    bpy.context.scene.world.luxcore.light = 'infinite'
    bpy.context.scene.world.luxcore.image = bpy.data.images.load(hdri_path)
    bpy.context.scene.world.luxcore.sampleupperhemisphereonly = True


def set_random_hdri_luxcore(hdri_dir_path, brightness_gain=None):
    hdri_paths = glob.glob(hdri_dir_path + "/*.hdr")
    hdri_path = random.choice(hdri_paths)
    set_hdri_luxcore(hdri_path)
    world_rot = random.uniform(0, 2*math.pi)
    bpy.context.scene.world.luxcore.rotation = world_rot

    if brightness_gain is None:
        bpy.context.scene.world.luxcore.gain = 1.0
    elif brightness_gain == "random":
        brightness_gain_exp = random.uniform(-1.0, 1.0)
        brightness_gain = 2 ** brightness_gain_exp
        bpy.context.scene.world.luxcore.gain = brightness_gain
    else: 
        bpy.context.scene.world.luxcore.gain = brightness_gain


def set_random_pbr(bl_object, pbr_dir_path):
    pbr_path = path_to_random_file(pbr_dir_path)
    assign_pbr_material(bl_object, pbr_path)





def row_wise_mean_index(img):
    try:
        img = np.average(img, axis=2)
    except:
        print("grayscale image")
    ret_img = np.zeros(np.shape(img))
    n_cols = np.shape(img)[1]
    col_inds = np.array(list(range(n_cols)))
    for r in range(len(img)):
        row = img[r]
        max_val = np.max(row)
        if max_val > 100:
            row_sum = np.sum(row)
            weighted_sum = np.dot(col_inds, row)/float(row_sum)
            ind = int(weighted_sum)
            ret_img[r,ind] = 255
    return ret_img

def convert_to_binary(img):
    try:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    except:
        pass
    img[img>50] = 255
    img[img<=50] = 0
    return img














    



if __name__ == "__main__":
    img = cv2.imread("/home/ola/Pictures/img_screenshot_29.01.2021.png")
    img = row_wise_mean_index(img)
    cv2.imshow("fsdds", img)
    cv2.waitKey(0)



