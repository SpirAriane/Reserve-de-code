# -*- coding: utf-8 -*-

from tkinter import Tk, Canvas, Button, PhotoImage, TOP, RIGHT
from math import sqrt
import pickle
import time

line_width = 2
point_rad = 4
size_x = 800
size_y = 600

class KdNode :
    def __init__(self, point, dim, left_child, right_child):
        self.point = point;
        self.dim = dim;
        self.left_child = left_child;
        self.right_child = right_child;

# Exemple : display points

def circle(can, center, col, rad = point_rad):
    x, y = center
    can.create_oval(x - rad, y - rad, x + rad, y + rad,
                    outline='black', fill=col)
def colorStr(rgb):
    return "#%0.2X%0.2X%0.2X" % (rgb[0],rgb[1],rgb[2])

def drawPoints(can, points, colors) :
    for p in points :
        circle(can, p, colorStr(colors[p]))


''' Exercice 1 '''

def drawKdTree(can, size, kdnode, colors) :
    # la signature de cette fonction devra être modifié !
    if kdnode == None :
        return
    else:
        [size_x_left, size_x_right, size_y_up, size_y_down] = size
        [x,y] = kdnode.point
        if kdnode.dim == 0:
            #séparation verticale
            drawKdTree(can, [size_x_left, x, size_y_up, size_y_down], kdnode.left_child, colors)
            drawKdTree(can, [x, size_x_right, size_y_up, size_y_down], kdnode.right_child, colors)
            circle(can, kdnode.point, colorStr(colors[kdnode.point]))
            can.create_line(x, size_y_up, x, size_y_down)
        
        else :
            #séparation horizontale
            drawKdTree(can, [size_x_left, size_x_right, size_y_up, y], kdnode.left_child, colors)
            drawKdTree(can, [size_x_left, size_x_right, y, size_y_down], kdnode.right_child, colors)
            circle(can, kdnode.point, colorStr(colors[kdnode.point]))
            can.create_line(size_x_left, y, size_x_right, y)


''' Exercice 2 '''

def Findpoints(kdnode, point):
    if kdnode == None:
        return False
    
    (x0,y0) = point
    [x,y] = kdnode.point
    if x0==x and y0==y :
        return True
    elif kdnode.left_child == None and kdnode.right_child == None:
        return False
    
    else:
        if kdnode.dim == 0:
            if x0 <= x :
                return Findpoints(kdnode.left_child, point)
            elif x0 >= x :
                return Findpoints(kdnode.right_child, point)
        elif kdnode.dim == 1:
            if y0 <= y :
                return Findpoints(kdnode.left_child, point)
            elif y0 >= y :
                return Findpoints(kdnode.right_child, point)


''' Exercice 3 '''

def FindVoisin(kdnode, voisin, point): #voisin = kdnode.point
    
    if kdnode == None:
        return voisin
              
    else:
        (x0,y0) = point
        
        voisin2 = voisin
        rayon = distance(point, voisin)
        
        [x_now,y_now] = kdnode.point
        rayon_now = distance(point, kdnode.point)
        if rayon_now < rayon:
            voisin = [x_now,y_now]
            rayon = rayon_now
        
        [x,y] = voisin
        [x_min, x_max, y_min, y_max] = [x0-rayon, x0+rayon, y0-rayon, y0+rayon]
        
        if kdnode.dim == 0:
            if x0 <= x :
                voisin1 = FindVoisin(kdnode.left_child, voisin, point)
                rayon1 = distance(voisin1, point)
                if x0+rayon1 > x :
                    voisin2 = FindVoisin(kdnode.right_child, voisin, point)
            
            elif x0 > x :
                voisin1 = FindVoisin(kdnode.right_child, voisin, point)
                rayon1 = distance(voisin1, point)
                if x0-rayon1 < x :
                    voisin2 = FindVoisin(kdnode.left_child, voisin, point)
                
        elif kdnode.dim == 1:
            if y0 <= y :
                voisin1 = FindVoisin(kdnode.left_child, voisin, point)
                rayon1 = distance(voisin1, point)
                if y0+rayon1 > y :
                    voisin2 = FindVoisin(kdnode.right_child, voisin, point)
                
            elif y0 > y :
                voisin1 = FindVoisin(kdnode.right_child, voisin, point)
                rayon1 = distance(voisin1, point)
                if y0-rayon1 < y :
                    voisin2 = FindVoisin(kdnode.left_child, voisin, point)
        
        rayon2 = distance(voisin2, point)
        
        if rayon2 < rayon1:
            voisin1 = voisin2
            rayon1 = rayon2
        
        if rayon1 < rayon:
            voisin = voisin1
            rayon = rayon1
        
        return voisin
        

def distance(pt1,pt2):
    [x1,y1] = pt1
    [x2,y2] = pt2
    return sqrt((x1-x2)**2 + (y1-y2)**2)
    


def drawVoisin(can, point, voisin):
    [x0,y0] = point
    [x,y] = voisin
    r = sqrt((x-x0)**2 + (y-y0)**2)
    can.create_oval(x0 - r, y0 - r, x0 + r, y0 + r, fill='blue')
    can.create_oval(x0 - 5, y0 - 5, x0 + 5, y0 + 5, outline='green', fill='green')
    can.create_line(x0, y0, x, y, fill='green')

def Pick(event):
    can.delete("all")
    x = event.x
    y = event.y
    point = (x,y)
    
    start1 = time.perf_counter()
    voisin = FindVoisin(kdtree, kdtree.point, point)
    stop1 = time.perf_counter()
    
    start2 = time.perf_counter()
    voisin2 = RechercheNaive(list_points, point)
    stop2 = time.perf_counter()
    
    print('Avec la recherche naïve, on trouve', voisin2, 'en', stop2-start2, 'secondes.' )
    print('Avec la recherche par KdTree, on trouve', voisin, 'en', stop1-start1, 'secondes.' )
    
    drawVoisin(can, point, voisin)
    drawKdTree(can, size, kdtree, colors)
    

'''Exercice 4'''

def RechercheNaive(liste, point):
    d = distance(point,liste[0])
    voisin = liste[0]
    for pt in liste:
        new_distance = distance(point,pt)
        if new_distance < d:
            d = new_distance
            voisin = pt
    return voisin

#Dans tous les cas, ma recherche naÏve est plus rapide que ma recherche par KdTree, et apparemment plus juste pour l'arbre à 10000 points, ou le KdTree ne trouve pas le plus proche, contrairement à l'autre.  


'''Exercice 5'''  

def CreerKdTree(Liste, dim=0):
    l = sorted(Liste, key=lambda x: x[dim])
    n = len(l)
    KdTree = KdNode(l[n//2], dim)
    fils_gauche = l[0:n//2]
    fils_droit = l[(n//2)+1:n]
    Kdtree.left_child = CreerKdTree(fils_gauche, (dim+1)%2)
    Kdtree.right_child = CreerKdTree(fils_droit, (dim+1)%2)
    return KdTree



if __name__ == '__main__':
    
    fen = Tk()
    can = Canvas(fen, width=size_x, height=size_y, bg='white')
    can.pack(side=TOP, padx=5, pady=5)

    example = "Simple"
#    example = "Grid"
#    example = "Clusters"
#    example = "Random_10"
#    example = "Random_100"
#    example = "Random_1000"
#    example = "Random_10000"
    kdtree = pickle.load(open("KdTree/"+example+".data","rb"))
    colors = pickle.load(open("KdTree/"+example+".color","rb"))
    list_points = pickle.load(open("KdTree/"+example+".points","rb"))

#    drawPoints(can, list_points, colors)
    size = [0, size_x, 0, size_y]
    drawKdTree(can, size, kdtree, colors)
    
    can.bind("<Button-1>", Pick)
    
    fen.mainloop()
    
    '''
    print(Findpoints(kdtree, (350, 350)))
    print(Findpoints(kdtree, (500, 150)))
    print(Findpoints(kdtree, (475, 225)))
    print(Findpoints(kdtree, (705, 500)))
    print(Findpoints(kdtree, (450, 550)))
    print(Findpoints(kdtree, (900, 300)))
    print(Findpoints(kdtree, (400, 500)))
    print(Findpoints(kdtree, (950, 450)))
    print(Findpoints(kdtree, (700, 500)))
    '''
