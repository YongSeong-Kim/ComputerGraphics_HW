import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# R=np.identity(3)
# P=np.identity(3)

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0) 
    glVertex3fv(np.array([0.,0.,0.])) 
    glVertex3fv(np.array([1.,0.,0.])) 
    glColor3ub(0, 255, 0) 
    glVertex3fv(np.array([0.,0.,0.])) 
    glVertex3fv(np.array([0.,1.,0.])) 
    glColor3ub(0, 0, 255) 
    glVertex3fv(np.array([0.,0.,0])) 
    glVertex3fv(np.array([0.,0.,1.])) 
    glEnd()

def drawCubeArray(): 
    for i in range(5):
        for j in range(5):
            for k in range(5): 
                glPushMatrix()
                glTranslatef(i,j,-k-1) 
                glScalef(.5,.5,.5) 
                drawUnitCube() 
                glPopMatrix()

def drawUnitCube():
    glBegin(GL_QUADS) 
    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f(-0.5, 0.5,-0.5) 
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f( 0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5,-0.5) 
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5, 0.5) 
    glVertex3f( 0.5,-0.5, 0.5) 
    glVertex3f( 0.5,-0.5,-0.5) 
    glEnd()
def myOrtho(left, right, bottom, top, near, far):
    a = 2.0 / (right - left)
    b = 2.0 / (top - bottom)
    c = -2.0 / (far - near)
    tx = - (right + left)/(right - left)
    ty = - (top + bottom)/(top - bottom)
    tz = - (far + near)/(far - near)
    viewingMatrix = np.identity(4)
    viewingMatrix[0][0] = a
    viewingMatrix[1][1] = b
    viewingMatrix[2][2] = c
    viewingMatrix[0][3] = tx
    viewingMatrix[1][3] = ty
    viewingMatrix[2][3] = tz
    glMultMatrixf(viewingMatrix.T)


# implement here
def myLookAt(eye, at, up):
    viewingMatrix = np.identity(4)
    w =  at - eye
    normalW = w / np.sqrt(np.dot(w , w))
    
    u = np.cross(normalW,up)
    normalU = u / np.sqrt(np.dot(u , u))
    
    v = np.cross( normalU, normalW)
    viewingMatrix[:1,:3] = normalU.T
    viewingMatrix[1:2,:3] = v.T
    viewingMatrix[2:3,:3] = -normalW.T
    glMultMatrixf(viewingMatrix.T)
    glTranslatef(-eye[0], -eye[1], -eye[2])
    

# implement here
def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()
    
    myOrtho(-5,5, -5,5, -8,8)
    myLookAt(np.array([5,3,5]), np.array([1,1,-1]), np.array([0,1,0]))
    # Above two lines must behaves exactly same as the below two lines

    
    drawFrame()
    glColor3ub(255, 255, 255)
    drawCubeArray()





def main():
    #initialize the library
    if not glfw.init(): 
        return

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2017029452-5-1", None, None)
    if not window:
        glfw.terminate()
        return
    

    # Make the window's context current
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        
        glfw.poll_events()
        render()
        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__": 
    main()
    