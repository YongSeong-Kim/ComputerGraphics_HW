import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

check = np.array([False, False, False, False, True, False, False, False, False, False, False, False])

def key_callback(window, key, scancode, action, mods):
    i = 0
    while i < 12:
        check[i] = False
        i = i + 1
    if key==glfw.KEY_1 :
        check[1] = True
    elif key==glfw.KEY_2 :
        check[2] = True
    elif key==glfw.KEY_3 :
        check[3] = True
    elif key==glfw.KEY_4 :
        check[4] = True
    elif key==glfw.KEY_5 :
        check[5] = True
    elif key==glfw.KEY_6 :
        check[6] = True
    elif key==glfw.KEY_7 :
        check[7] = True
    elif key==glfw.KEY_8 :
        check[8] = True
    elif key==glfw.KEY_9 :
        check[9] = True
    elif key==glfw.KEY_0 :
        check[0] = True

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # # draw cooridnate
    # glBegin(GL_LINES)
    # glColor3ub(255, 0, 0)
    # glVertex2fv(np.array([-1.,0.]))
    # glVertex2fv(np.array([1.,0.]))
    # glColor3ub(0, 255, 0)
    # glVertex2fv(np.array([0.,-1.]))
    # glVertex2fv(np.array([0.,1.]))
    # glEnd()
    # glPointSize(10.0)
    
    if check[1] == True:
        glBegin(GL_POINTS)
        count = 0
        th = np.radians(30)
        arr = np.linspace(0,11,12)
        while count < 12 :
            glVertex2f(1. * np.cos(arr[count] * th), 1. * np.sin(arr[count]* th))
            count = count + 1
        glEnd()
    elif check[2] == True:
        glBegin(GL_LINES)
        count = 0
        th = np.radians(30)
        arr = np.linspace(0,11,12)
        while count < 12 :
            glVertex2f(1. * np.cos(arr[count] * th), 1. * np.sin(arr[count]* th))
            count = count + 1
        glEnd()
    elif check[3] == True:
        glBegin(GL_LINE_STRIP)
        count = 0
        th = np.radians(30)
        arr = np.linspace(0,11,12)
        while count < 12 :
            glVertex2f(1. * np.cos(arr[count] * th), 1. * np.sin(arr[count]* th))
            count = count + 1
        glEnd()
    elif check[4] == True:
        glBegin(GL_LINE_LOOP)
        count = 0
        th = np.radians(30)
        arr = np.linspace(0,11,12)
        while count < 12 :
            glVertex2f(1. * np.cos(arr[count] * th), 1. * np.sin(arr[count]* th))
            count = count + 1
        glEnd()
    elif check[5] == True:
        glBegin(GL_TRIANGLES)
        count = 0
        th = np.radians(30)
        arr = np.linspace(0,11,12)
        while count < 12 :
            glVertex2f(1. * np.cos(arr[count] * th), 1. * np.sin(arr[count]* th))
            count = count + 1
        glEnd()
    elif check[6] == True:
        glBegin(GL_TRIANGLE_STRIP)
        count = 0
        th = np.radians(30)
        arr = np.linspace(0,11,12)
        while count < 12 :
            glVertex2f(1. * np.cos(arr[count] * th), 1. * np.sin(arr[count]* th))
            count = count + 1
        glEnd()
    elif check[7] == True:
        glBegin(GL_TRIANGLE_FAN)
        count = 0
        th = np.radians(30)
        arr = np.linspace(0,11,12)
        while count < 12 :
            glVertex2f(1. * np.cos(arr[count] * th), 1. * np.sin(arr[count]* th))
            count = count + 1
        glEnd()
    elif check[8] == True:
        glBegin(GL_QUADS)
        count = 0
        th = np.radians(30)
        arr = np.linspace(0,11,12)
        while count < 12 :
            glVertex2f(1. * np.cos(arr[count] * th), 1. * np.sin(arr[count]* th))
            count = count + 1
        glEnd()
    elif check[9] == True:
        glBegin(GL_QUAD_STRIP)
        count = 0
        th = np.radians(30)
        arr = np.linspace(0,11,12)
        while count < 12 :
            glVertex2f(1. * np.cos(arr[count] * th), 1. * np.sin(arr[count]* th))
            count = count + 1
        glEnd()
    elif check[0] == True:
        glBegin(GL_POLYGON)
        count = 0
        th = np.radians(30)
        arr = np.linspace(0,11,12)
        while count < 12 :
            glVertex2f(1. * np.cos(arr[count] * th), 1. * np.sin(arr[count]* th))
            count = count + 1
        glEnd()


def main():
    #initialize the library
    if not glfw.init(): 
        return

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2017029452-3-1", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.set_key_callback(window, key_callback)

    # Make the window's context current
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        
        glfw.poll_events()
        render()
        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__": 
    main()
    