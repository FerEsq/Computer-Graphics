'''
 * Nombre: renderer.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Iniciado el 20.07.2023 
              Finalizado el 26.07.2023
 '''

from gl import Renderer, V2, color
width = 900
height = 450

rend = Renderer(width, height)

p1 = [  V2(165, 380), 
        V2(185, 360), 
        V2(180, 330), 
        V2(207, 345), 
        V2(233, 330), 
        V2(230, 360), 
        V2(250, 380), 
        V2(220, 385), 
        V2(205, 410), 
        V2(193, 383)  ]

p2 = [  V2(321, 335),
        V2(288, 286), 
        V2(339, 251),
        V2(374, 302)  ]

p3 = [  V2(377, 249), 
        V2(411, 197),
        V2(436, 249)  ]

p4 = [ V2(413, 177),
       V2(448, 159), 
       V2(502, 88), 
       V2(553, 53), 
       V2(535, 36), 
       V2(676, 37), 
       V2(660, 52),
       V2(750, 145), 
       V2(761, 179), 
       V2(672, 192),
       V2(659, 214), 
       V2(615, 214), 
       V2(632, 230), 
       V2(580, 230),
       V2(597, 215), 
       V2(552, 214), 
       V2(517, 144),
       V2(466, 180)  ]

p5 = [  V2(682, 175),
        V2(708, 120), 
        V2(735, 148), 
        V2(739, 170) ]

rend.glPolygon(p1, color(1,0,0))
rend.glPolygon(p2, color(0,1,0))
rend.glPolygon(p3, color(0,0,1))
rend.glPolygon(p4, color(1,1,0))
rend.glPolygon(p5, color(0,0,0))
rend.glFill(p1, color(1,0,0))
rend.glFill(p2, color(0,1,0))
rend.glFill(p3, color(0,0,1))
rend.glFill(p4, color(1,1,0))
rend.glFill(p5, color(0,0,0))


rend.glFinish("output.bmp")