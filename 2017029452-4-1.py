import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

R=np.identity(3)
P=np.identity(3)

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()

def key_callback(window, key, scancode, action, mods): 
     global R, P
     R=np.identity(3)
     if action==glfw.PRESS or action==glfw.REPEAT:
         
        if key==glfw.KEY_Q:
            R[:2,2:] = [[-0.1],
            [ 0.]]
            P = R@P
        elif key==glfw.KEY_E:
            R[:2,2:] = [[0.1],
            [ 0.]]
            P = R@P
            
        elif key==glfw.KEY_A:
            th = np.radians(10)
            R[:2,:2] = [[np.cos(th), -np.sin(th)],
            [np.sin(th), np.cos(th)]]
            P = P@R
        elif key==glfw.KEY_D:
            th = np.radians(-10)
            R[:2,:2] = [[np.cos(th), -np.sin(th)],
            [np.sin(th), np.cos(th)]]
            P = P@R
        elif key==glfw.KEY_1:
            P = np.identity(3)
        elif key==glfw.KEY_W:
            R[:2,:2] = [[0.9, 0.],
            [0., 1.]]
            P = R@P
        elif key==glfw.KEY_S:
            th = np.radians(10)
            R[:2,:2] = [[np.cos(th), -np.sin(th)],
            [np.sin(th), np.cos(th)]]
            P = R@P

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,'2017029452-4-1', None,None)
    
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(P)
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()