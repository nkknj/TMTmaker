import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont
inf=np.inf
pi=np.pi

filename=sys.argv[1]

def length_AB(A, B):
    return pow(pow(A[0]-B[0], 2)+pow(A[1]-B[1], 2), 1/2)

def check_circles_cross(A, ra, B, rb):
    length=length_AB(A, B)
    if length<=ra+rb:
        cross=True
    else:
        cross=False
    return cross

#直線A, Bの傾き
def gradient_2_dots(A, B):
    if A[0]==B[0]:
        k=inf
    else:
        k=(B[1]-A[1])/(B[0]-A[0])
    return k

#入力の点A, B, C, Dについて、直線ABと直線CDの交点XをpOA+(1-p)OB、qOC+(1-q)ODで表す時のp, q
#なお直線ABの傾きは無限大ではないこと、二直線は平行でないこと、の2点は満たしていることを前提とする
def calc_pq(A, B, C, D):
    q=((D[1]-B[1])*(A[0]-B[0])-(D[0]-B[0])*(A[1]-B[1]))/((C[0]-D[0])*(A[1]-B[1])-(C[1]-D[1])*(A[0]-B[0]))
    p=(q*(C[0]-D[0])+D[0]-B[0])/(A[0]-B[0])
    return p, q

#点A, B, C, Dが与えられたとき、線分ABと線分CDが交差するか判定する関数
def check_AB_CD_cross(A, B, C, D):
    k1=gradient_2_dots(A, B)
    k2=gradient_2_dots(C, D)
    
    if k1==inf and k2==inf:
        cross=False
    elif k1==k2:
        cross=False
    else:
        if k1!=inf:
            p, q=calc_pq(A, B, C, D)
        else:
            p, q=calc_pq(C, D, A, B)
            
        if p*(1-p)>=0 and q*(1-q)>=0:
            cross=True
        else:
            cross=False
    return cross

def get_nodes(n_nodes, space, white, diameter):
    cross=True
    while cross==True:
        nodes=np.c_[np.random.rand(n_nodes)*(space[0]-2*white[0])+white[0], np.random.rand(n_nodes)*(space[1]-2*white[1])+white[1]]
        cross=check_all_circles_cross(nodes, diameter/2)
    return nodes

def check_all_circles_cross(nodes, r):
    cross=False
    for x in range(nodes.shape[0]-1):
        for y in range(x+1, nodes.shape[0]):
            if check_circles_cross(nodes[x], r, nodes[y], r):
                cross=True
    return cross

def uncrosser(nodes, space, white, diameter):
    cross=True
    while cross==True:
        nodes, cross=line_uncrosser(nodes)
    
    return nodes

def line_uncrosser(nodes):
    cross=False
    for x in range(nodes.shape[0]-3):
        for y in range(x+2, nodes.shape[0]-1):
            if check_AB_CD_cross(nodes[x], nodes[x+1], nodes[y], nodes[y+1]):
                cross=True
                nodes=AB_CD_2_AC_BD(nodes, x, y)
                break
        
        if cross==True:
            break
    return nodes, cross

def AB_CD_2_AC_BD(nodes, x, y):
    nodes=np.r_[nodes[:x+1], nodes[y:x:-1], nodes[(y+1):]]
    return nodes

n_nodes=25
space_w=1050
space_h=1485
white_w=50
white_h=50
diameter=50

space=np.array([space_w, space_h])
white=np.array([white_w, white_h])


nodes=get_nodes(n_nodes, space, white, diameter)
nodes=uncrosser(nodes, space, white, diameter)

im=Image.new('RGB', (space[0], space[1]), (200, 200, 200))
draw=ImageDraw.Draw(im)
font = ImageFont.truetype("arial.ttf", 32)
characters_num=[' 1', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8', ' 9', '10', '11', '12', '13']
characters_jpn=[' A', ' B', ' C', ' D', ' E', ' F', ' G', ' H', ' I', ' J', ' K', ' L']
characters=[None]*25
characters[::2]=characters_num
characters[1::2]=characters_jpn

for i in range(nodes.shape[0]):
    temp=nodes[i]
    draw.ellipse((temp[0]-diameter/2, temp[1]-diameter/2, temp[0]+diameter/2, temp[1]+diameter/2), fill=(255, 255, 255), outline=(0, 0, 0))
    draw.text((temp[0]-diameter*2/5, temp[1]-diameter*2/5), characters[i], (0, 0, 0), font)

im.save(filename, quality=95)