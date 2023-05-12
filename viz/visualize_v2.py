import matplotlib.pyplot as plt
import numpy as np
import _pickle as cPickle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import cairosvg
from geopatterns import GeoPattern
import random
import uuid
import re
import inspect
import os
# Next polyomino set visulization:
import math 

import os
from PIL import Image

import sys
sys.path.insert(0, "..")
import packing.packing as P

board_dict = {
    0: [
        [1, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 1],
    ],
    1: [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1],
    ],
    2: [
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 1],
    ],
    3: [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 1],
    ],
    4: [
        [1, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 1],
    ],
}

pattern_types = ["bricks", "hexagons", "overlapping_circles", "overlapping_rings", "plaid", "plus_signs", "rings", "squares", "triangles", "xes"]

def create_texture_files(k=20, location=".outputs/"):
    texture_files = []
    for i in range(k):
        file_name = os.path.join(location, f"tmp_{i}.png")
        pattern = GeoPattern(str(uuid.uuid4()) ,random.choice(pattern_types))
        cairosvg.svg2png(bytestring=pattern.svg_string, write_to=file_name, dpi=300, scale=5.0)
        texture_files.append(file_name)
    return texture_files

def draw_edges(polymino, ax, x_offset=0, y_offset=0, color='black'):
    for ind, (x, y) in enumerate(polymino):
        x += x_offset
        y += y_offset
        ax.plot([x, x + 1], [y, y], color=color, linewidth=2)
        ax.plot([x + 1, x + 1], [y, y + 1], color=color, linewidth=2)
        ax.plot([x + 1, x], [y + 1, y + 1], color=color, linewidth=2)
        ax.plot([x, x], [y + 1, y], color=color, linewidth=2)
    ax.set_aspect('equal')
    ax.axis('off')
    
def draw_packing_with_texture(polyminoes, locations, board_width, board_height, texture_files):
    fig, ax = plt.subplots(figsize=(board_width, board_height))
    ax.set_xlim(0, board_width)
    ax.set_ylim(0, board_height)
    ax.axis('off')
    ax.invert_yaxis()
    i = 0
    for polymino, (x_offset, y_offset) in zip(polyminoes, locations):
        draw_edges(polymino, ax, x_offset, y_offset, color='black')
        for x, y in polymino:
            img = texture_files[i]
            img = Image.open(img)
            ax.imshow(img, extent=[x + x_offset, x + x_offset +1, 
                                y + y_offset, y + y_offset +1])
        ax.set_aspect('equal')
        ax.axis('off')
        i += 1
    return fig

def draw_single_polyomino(polymino, ax, texture_file):
    # center the polyomino
    # draw edges:
    
    poly_np = np.array(polymino)
    ax_1_size = poly_np[:, 0].max() - poly_np[:, 0].min() + 1
    ax_2_size = poly_np[:, 1].max() - poly_np[:, 0].min() + 1
    x_offset = (5 - ax_1_size) / 2
    y_offset = (5 - ax_2_size) / 2
    draw_edges(polymino, ax, x_offset, y_offset, color='black')
    for x, y in polymino:
        img = Image.open(texture_file)
        ax.imshow(img, extent=[x + x_offset, x + x_offset + 1, 
                               y + y_offset, y + y_offset + 1])
        
def draw_polyomino_set(blocks, grid_size_W, grid_size_H, texture_files,figsize=5):        
    n_poly = len(blocks)
    # grid_size = math.ceil(math.sqrt(n_poly))
    fig, axs = plt.subplots(grid_size_W, grid_size_H, figsize=(grid_size_H * figsize, grid_size_W * figsize))
    for ax in axs.flat:
        ax.axis('off')
    for ind, poly in enumerate(blocks):
        i, j = ind // grid_size_H, ind % grid_size_H
        if grid_size_W == 1:
            ax = axs[j]
        else:
            ax = axs[i, j]
        ax.set_xlim(0, figsize)  # assume each polymino fits in a 5x5 box
        ax.set_ylim(0, figsize)
        texture_file = texture_files[ind]
        draw_single_polyomino(poly, ax, texture_file)
    return fig

def concatenate_images(image1, image2):
    # Resize the images to have the same height
    height = min(image1.size[1], image2.size[1])
    image1 = image1.resize((int(image1.size[0] * height / image1.size[1]), height))
    image2 = image2.resize((int(image2.size[0] * height / image2.size[1]), height))

    # Create a new blank image with double the width
    width = image1.size[0] + image2.size[0]
    new_image = Image.new('RGB', (width, height))

    # Paste the resized images onto the new image
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1.size[0], 0))

    return new_image

def create_gif_mix(folder_path, output_path, file_reqr_1, file_reqr_2, frame_rate):
    images = []
    file_names = os.listdir(folder_path)
    file_names_1 = [f for f in file_names if file_reqr_1 in f]
    file_names_1.sort(key=lambda f: int(f.split('.')[0].split('_')[-1]))
    
    file_names_2 = [f for f in file_names if file_reqr_2 in f]
    file_names_2.sort(key=lambda f: int(f.split('.')[0].split('_')[-1]))
    
    for ind, file_name in enumerate(file_names_1):
        image_path = os.path.join(folder_path, file_name)
        image_1 = Image.open(image_path)
        file_name = file_names_2[ind]
        image_path = os.path.join(folder_path, file_name)
        image_2 = Image.open(image_path)
        
        concatenated_image = concatenate_images(image_1, image_2)
        images.append(concatenated_image)

    images[0].save(output_path, save_all=True, append_images=images[1:], duration=frame_rate, loop=0)
    
def create_gif(folder_path, output_path, file_reqr_1, frame_rate):
    images = []
    file_names = os.listdir(folder_path)
    file_names_1 = [f for f in file_names if file_reqr_1 in f]
    file_names_1.sort(key=lambda f: int(f.split('.')[0].split('_')[-1]))
    
    
    for ind, file_name in enumerate(file_names_1):
        image_path = os.path.join(folder_path, file_name)
        image_1 = Image.open(image_path)
        
        images.append(image_1)

    images[0].save(output_path, save_all=True, append_images=images[1:], duration=frame_rate, loop=0)
