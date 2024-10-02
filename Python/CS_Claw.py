import bpy
import os
import math
import subprocess

output_base_path = '/your/output/folder/here/' # Where your files will be put
montage = '/opt/homebrew/bin/montage' # Change this to be wherever montage is. use which montage if you are on *nix

image_format = 'PNG'
image_extension = '.png'
image_width = 1920
image_height = 1080

sheet_name = 'spritesheet'
sprite_geom_W = 512 # Sprite cell width
sprite_geom_H = 512 # Sprite cell height
filter = 'Catrom' # Image filter type
background = 'transparent' # background for sprite sheet

num_columns = 6 # Number of columns in your sprite sheet

camera_list = [ # Ensure these all match the camera names in your scene
    'Front_Camera', 
    'FrontRight_Camera', 
    'Right_Camera', 
    'Back_Right', 
    'Back_Camera', 
    'Back_Left', 
    'Left_Camera', 
    'FrontLeft_Camera'
]

start_frame = bpy.context.scene.frame_start
end_frame = bpy.context.scene.frame_end

bpy.context.scene.render.image_settings.file_format = image_format
bpy.context.scene.render.resolution_x = image_width  
bpy.context.scene.render.resolution_y = image_height

def render_from_camera(camera_name, output_folder):
    bpy.context.scene.camera = bpy.data.objects[camera_name]
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    bpy.context.scene.render.filepath = os.path.join(output_folder, camera_name + '_')
    bpy.ops.render.render(animation=True, write_still=False)

def calculate_montage_n(folder_path, num_columns):
    num_files = len([f for f in os.listdir(folder_path) if f.endswith(image_extension)])
    n_value = math.ceil(num_files / num_columns)
    return n_value

def run_montage_command(folder_path, n_value, num_columns):
    montage_path = f'{montage}'
    input_files = os.path.join(folder_path, '*.png')
    output_spritesheet = os.path.join(folder_path, f'{sheet_name}.png')
    montage_command = [
        montage_path, input_files,
        '-geometry', f'{sprite_geom_W}x{sprite_geom_H}',
        '-tile', f'{num_columns}x{n_value}',
        '-background', f'{background}',
        '-filter', f'{filter}',
        output_spritesheet
    ]
    subprocess.run(montage_command, cwd=folder_path, check=True)

for camera in camera_list:
    output_folder = os.path.join(output_base_path, camera)
    render_from_camera(camera, output_folder)
    n_value = calculate_montage_n(output_folder, num_columns)
    run_montage_command(output_folder, n_value, num_columns)

print("Rendering and montage processing completed!")