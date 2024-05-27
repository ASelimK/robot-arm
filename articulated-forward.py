from numpy import matlib 
from numpy import matrix
from numpy import linalg
import numpy as np
import math
from vpython import *

#region INITIAL PROGRAM PARAMETERS

step_degree = 5
debugValues = False #It makes program much more slower when it is True. Prints certain important values to the console.

theta_0_degree = 0 
theta_1_degree = 0 
theta_2_degree = 0 
theta_3_degree = 0

length_01 = 8
length_12 = 8
length_23 = 8

frame0  = [ [4,0,0,0],
            [0,4,0,0],
            [0,0,4,0],
            [0,0,0,1] ]
frame1  = [ [4,0,0,0],
            [0,4,0,0],
            [0,0,4,4],
            [0,0,0,1] ]
frame2  = [ [4,0,0,4],
            [0,4,0,0],
            [0,0,4,4],
            [0,0,0,1] ]
frame3  = [ [4,0,0,8],
            [0,4,0,0],
            [0,0,4,4],
            [0,0,0,1] ]

rotation_01 = [ [1  ,0  ,0  ],
                [0  ,0  ,-1 ],
                [0  ,1  ,0  ] ]
rotation_12 = [ [1  ,0  ,0  ],
                [0  ,1  ,0  ],
                [0  ,0  ,1  ] ]
rotation_23 = [ [1  ,0  ,0  ],
                [0  ,1  ,0  ],
                [0  ,0  ,1  ] ]

#region Derivations
rotation_02 = np.dot(rotation_01,rotation_12)
rotation_03 = np.dot(rotation_02,rotation_23)
theta_0_radian = 0
theta_1_radian = 0
theta_2_radian = 0
theta_3_radian = 0
#endregion

#endregion

#region Functions
def to_radian(theta_degree):
    return (theta_degree/180.0)*np.pi

def recalculate_r0_1(theta_radian, rotation_matrix):
    rx_y =  [   [np.cos(theta_radian)      ,- np.sin(theta_radian)          ,0], 
                [np.sin(theta_radian)      ,np.cos(theta_radian)            ,0],
                [0                         ,0                               ,1]]
    return_value = np.dot(rx_y ,rotation_matrix)
    return return_value

def recalculate_d0_1(length):
    d0_1 = [[0], [0],[length]]
    return d0_1

def recalculate_dx_y(length, radian):
    dx_y =  [[np.cos(radian) * length ], 
            [np.sin(radian) * length ],
            [0                       ]]
    return dx_y

def update_frame_positions_and_orientations():
    global frame0, frame1, frame2, frame3
    #region Frame0
    frame0x.axis = vector(frame0[0][0], frame0[1][0], frame0[2][0])
    frame0y.axis = vector(frame0[0][1], frame0[1][1], frame0[2][1])
    frame0z.axis = vector(frame0[0][2], frame0[1][2], frame0[2][2])

    frame0x.pos = vector(frame0[0][3], frame0[1][3], frame0[2][3])
    frame0y.pos = vector(frame0[0][3], frame0[1][3], frame0[2][3])
    frame0z.pos = vector(frame0[0][3], frame0[1][3], frame0[2][3])
    #endregion

    #region Frame1
    frame1x.axis = vector(frame1[0][0], frame1[1][0], frame1[2][0])
    frame1y.axis = vector(frame1[0][1], frame1[1][1], frame1[2][1])
    frame1z.axis = vector(frame1[0][2], frame1[1][2], frame1[2][2])

    frame1x.pos  = vector(frame1[0][3], frame1[1][3], frame1[2][3])
    frame1y.pos  = vector(frame1[0][3], frame1[1][3], frame1[2][3])
    frame1z.pos  = vector(frame1[0][3], frame1[1][3], frame1[2][3])
    #endregion

    #region Frame2
    frame2x.axis = vector(frame2[0][0], frame2[1][0], frame2[2][0])
    frame2y.axis = vector(frame2[0][1], frame2[1][1], frame2[2][1])
    frame2z.axis = vector(frame2[0][2], frame2[1][2], frame2[2][2])

    frame2x.pos = vector(frame2[0][3], frame2[1][3], frame2[2][3])
    frame2y.pos = vector(frame2[0][3], frame2[1][3], frame2[2][3])
    frame2z.pos = vector(frame2[0][3], frame2[1][3], frame2[2][3])
    #endregion

    #region Frame3
    frame3x.axis = vector(frame3[0][0], frame3[1][0], frame3[2][0])
    frame3y.axis = vector(frame3[0][1], frame3[1][1], frame3[2][1])
    frame3z.axis = vector(frame3[0][2], frame3[1][2], frame3[2][2])

    frame3x.pos = vector(frame3[0][3], frame3[1][3], frame3[2][3])
    frame3y.pos = vector(frame3[0][3], frame3[1][3], frame3[2][3])
    frame3z.pos = vector(frame3[0][3], frame3[1][3], frame3[2][3])
    #endregion

    #region Frame1->Frame2
    arrow_01.pos = frame0x.pos
    arrow_01.axis = frame1x.pos- frame0x.pos
    #endregion
    
    #region Frame1->Frame2
    arrow_12.pos = frame1x.pos
    arrow_12.axis = frame2x.pos- frame1x.pos
    #endregion

    #region Frame1->Frame2
    arrow_23.pos = frame2x.pos
    arrow_23.axis = frame3x.pos- frame2x.pos
    #endregion

def do_matrix_operations():
    global frame0, frame1, frame2, frame3
    global theta_0_radian, theta_0_degree, theta_1_degree, theta_1_radian, theta_2_degree, theta_2_radian
    global rotation_01, rotation_12, rotation_23, rotation_02, rotation_03

    #region Recalculations
    r0_1 =  recalculate_r0_1(theta_0_radian, rotation_01)
    r1_2 =  recalculate_r0_1(theta_1_radian, rotation_12)
    r2_3 =  recalculate_r0_1(theta_2_radian, rotation_23) 

    d0_1 =  recalculate_d0_1(length_01)
    d1_2 =  recalculate_dx_y(length_12, theta_1_radian)
    d2_3 =  recalculate_dx_y(length_23, theta_2_radian)
    #endregion

    #region Concat to homogeneus matrices
    h0_1 = np.concatenate((r0_1, d0_1), 1)
    h0_1 = np.concatenate((h0_1, [[0,0,0,1]]), 0)

    h1_2 = np.concatenate((r1_2, d1_2), 1)
    h1_2 = np.concatenate((h1_2, [[0,0,0,1]]), 0)

    h2_3 = np.concatenate((r2_3, d2_3), 1)
    h2_3 = np.concatenate((h2_3, [[0,0,0,1]]), 0)

    h0_2 = np.dot(h0_1, h1_2)
    h0_3 = np.dot(h0_2, h2_3)
    #endregion

    #region Frame Assignments
    frame1 = np.dot(h0_1, frame0)
    frame2 = np.dot(h0_2, frame0)
    frame3 = np.dot(h0_3, frame0)
    #endregion
    
    update_frame_positions_and_orientations()

    #region print thetas - frames - homogeneus matrices
    if debugValues == True:
        print("-----------------------------------")
        print("h0_1")
        print(h0_1)
        print("h1_2")
        print(h1_2)
        print("h2_3")
        print(h2_3)
        print("h0_2")
        print(h0_2)
        print("h0_3")
        print(h0_3)
        print("-----------------------------------")
        print("theta 0", theta_0_degree)
        print("-----------------------------------")
        print("  frame0")
        print(frame0)
        print("-----------------------------------")
        print("theta 1", theta_1_degree)
        print("-----------------------------------")
        print("  frame1")
        print(frame1)
        print("-----------------------------------")
        print("theta 2", theta_2_degree)
        print("-----------------------------------")
        print("  frame2")
        print(frame2)
        print("-----------------------------------")
        print("theta 3", theta_3_degree)
        print("-----------------------------------")
        print("  frame3")
        print(frame3)
        print("############################################")
    #endregion
#endregion

#region Draw Frames

#region FRAME 0 ______________________________________________
frame0x = arrow(pos = vector(frame0[0][3], frame0[1][3], frame0[2][3]),
                axis = vector(frame0[0][0], frame0[1][0], frame0[2][0]),
                headwidth = 0.8,
                color = color.blue,
                round = True
)

frame0y = arrow(pos = vector(frame0[0][3], frame0[1][3], frame0[2][3]),
                axis = vector(frame0[0][1],frame0[1][1],frame0[2][1]),
                headwidth = 0.8,
                color = color.green,
                round = True
)

frame0z = arrow(pos = vector(frame0[0][3], frame0[1][3], frame0[2][3]),
                axis = vector(frame0[0][2],frame0[1][2],frame0[2][2]),
                headwidth = 0.8,
                color = color.red,
                round = True
)
#endregion

#region FRAME 1 ______________________________________________
frame1x = arrow(pos = vector(frame1[0][3], frame1[1][3], frame1[2][3]),
                axis = vector(frame1[0][0], frame1[1][0], frame1[2][0]),
                headwidth = 0.8,
                color = color.blue,
                round = True
)

frame1y = arrow(pos = vector(frame1[0][3], frame1[1][3], frame1[2][3]),
                axis = vector(frame1[0][1],frame1[1][1],frame1[2][1]),
                headwidth = 0.8,
                color = color.green,
                round = True
)

frame1z = arrow(pos = vector(frame1[0][3], frame1[1][3], frame1[2][3]),
                axis = vector(frame1[0][2],frame1[1][2], frame1[2][2]),
                headwidth = 0.8,
                color = color.red,
                round = True
)

#endregion

#region FRAME 2 ______________________________________________
frame2x = arrow(pos = vector(frame2[0][3], frame2[1][3], frame2[2][3]),
                axis = vector(frame2[0][0], frame2[1][0], frame2[2][0]),
                headwidth = 0.8,
                color = color.blue,
                round = True
)

frame2y = arrow(pos = vector(frame2[0][3], frame2[1][3], frame2[2][3]),
                axis = vector(frame2[0][1], frame2[1][1], frame2[2][1]),
                headwidth = 0.8,
                color = color.green,
                round = True
)

frame2z = arrow(pos = vector(frame2[0][3], frame2[1][3], frame2[2][3]),
                axis = vector(frame2[0][2], frame2[1][2], frame2[2][2]),
                headwidth = 0.8,
                color = color.red,
                round = True
)
#endregion

#region FRAME 3 ______________________________________________
frame3x = arrow(pos = vector(frame3[0][3], frame3[1][3], frame3[2][3]),
                axis = vector(frame2[0][0], frame2[1][0], frame2[2][0]),
                headwidth = 0.8,
                color = color.blue,
                round = True
)

frame3y = arrow(pos = vector(frame3[0][3], frame3[1][3], frame3[2][3]),
                axis = vector(frame2[0][1], frame2[1][1], frame2[2][1]),
                headwidth = 0.8,
                color = color.green,
                round = True
)

frame3z = arrow(pos = vector(frame3[0][3], frame3[1][3], frame3[2][3]),
                axis = vector(frame2[0][2], frame2[1][2], frame2[2][2]),
                headwidth = 0.8,
                color = color.red,
                round = True
)
#endregion

#region Frame0->Frame1______________________________________
arrow_01 = arrow(pos = frame0x.pos,
                axis = frame1x.pos - frame0x.pos,
                headwidth = 0,
                color = color.cyan,
                round = True,
                len = length_01
)
#endregion

#region Frame1->Frame2______________________________________
arrow_12 = arrow(pos = frame1x.pos,
                axis = frame2x.pos - frame1x.pos,
                headwidth = 0,
                color = color.cyan,
                round = True,
                len = length_12
)
#endregion

#region Frame1->Frame2______________________________________
arrow_23 = arrow(pos = frame2x.pos,
                axis = frame3x.pos - frame2x.pos,
                headwidth = 0,
                color = color.cyan,
                round = True,
                len = length_23
)
#endregion

#endregion

#To make simulation initially true also, do_matrix_operations()
do_matrix_operations()

def rotate_x(event):
    global theta_0_radian, theta_0_degree, theta_1_degree, theta_1_radian, theta_2_degree, theta_2_radian

    #region FRAME 1 keyboard_________________________________________________
    if event.key == 'q':
        theta_0_degree -= step_degree
        theta_0_radian = to_radian(theta_0_degree)

    if event.key == 'w':
        theta_0_degree += step_degree
        theta_0_radian = to_radian(theta_0_degree)
    #endregion

    #region FRAME 2 keyboard_________________________________________________
    if event.key == 'a':
        theta_1_degree -= step_degree
        theta_1_radian = to_radian(theta_1_degree)

    if event.key == 's':
        theta_1_degree += step_degree
        theta_1_radian = to_radian(theta_1_degree)
    #endregion

    #region FRAME 3 keyboard_________________________________________________
    if event.key == 'z':
        theta_2_degree -= step_degree
        theta_2_radian = to_radian(theta_2_degree)

    if event.key == 'x':
        theta_2_degree += step_degree
        theta_2_radian = to_radian(theta_2_degree)
    #endregion

    do_matrix_operations()

scene.bind('keydown', rotate_x)

while True:
    rate(60)
