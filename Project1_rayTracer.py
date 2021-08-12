import sys
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
import math

MAX = sys.maxsize

class Color:
    def __init__(self, R, G, B):
        self.color = np.array([R, G, B]).astype(np.float)

    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma
        self.color = np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0, 1) * 255).astype(np.uint8)


class Shader:
    def __init__(self, type):
        self.type = type


class ShaderPhong(Shader):
    def __init__(self, diffuse, specular, exponent):
        self.d = diffuse
        self.s = specular
        self.exponent = exponent
    
    @staticmethod
    def shadePhong(v, lightIntensity, normalVector, i):
        global x,y,z,collisionFlag
        normalV = v / np.sqrt(np.sum(v**2))
        h = normalV + lightIntensity
        h = normalize(h)
        x = x + list[collisionFlag].s.d[0]*max(0,np.dot(normalVector,lightIntensity))*i.intensity[0] + list[collisionFlag].s.s[0] * i.intensity[0] * pow(max(0, np.dot(normalVector, h)),list[collisionFlag].s.exponent[0])
        y = y + list[collisionFlag].s.d[1]*max(0,np.dot(normalVector,lightIntensity))*i.intensity[1] + list[collisionFlag].s.s[1] * i.intensity[1] * pow(max(0, np.dot(normalVector, h)),list[collisionFlag].s.exponent[0])
        z = z + list[collisionFlag].s.d[2]*max(0,np.dot(normalVector,lightIntensity))*i.intensity[2] + list[collisionFlag].s.s[2] * i.intensity[2] * pow(max(0, np.dot(normalVector, h)),list[collisionFlag].s.exponent[0])


class ShaderLambertian(Shader):
    def __init__(self, diffuse):
        self.d = diffuse

    @staticmethod
    def shadeLam(lightIntensity, i,normalVector):
        global x,y,z,collisionFlag
        x = x + list[collisionFlag].s.d[0] * i.intensity[0] * max(0, np.dot(lightIntensity, normalVector))
        y = y + list[collisionFlag].s.d[1] * i.intensity[1] * max(0, np.dot(lightIntensity, normalVector))
        z = z + list[collisionFlag].s.d[2] * i.intensity[2] * max(0, np.dot(lightIntensity, normalVector))
        

class Sphere:
    def __init__(self, center, radius, shader):
        self.c = center
        self.r = radius
        self.s = shader
    
    @staticmethod
    def raySphere(a, b, c, count):
        global m, collisionFlag
        #근의 공식.
        if b ** 2 - a * c >= 0:
                if -b + np.sqrt(b ** 2 - a * c) >= 0:
                    if m >= (-b + np.sqrt(b ** 2 - a * c)) / a:
                        m = (-b + np.sqrt(b ** 2 - a * c)) / a
                        collisionFlag = count
                if -b - np.sqrt(b ** 2 - a * c) >= 0:
                    if m >= (-b - np.sqrt(b ** 2 - a * c)) / a:
                        m = (-b - np.sqrt(b ** 2 - a * c)) / a
                        collisionFlag = count
    
class Box:
    def __init__(self, minPt, maxPt, shader, normals):
        self.minPt = minPt
        self.maxPt = maxPt
        self.s = shader
        self.n = normals
    
    @staticmethod
    def rayBox(i,viewPoint, ray, count):
        global m, collisionFlag
        result = 1
        txmin = (i.minPt[0]-viewPoint[0])/ray[0]
        txmax = (i.maxPt[0]-viewPoint[0])/ray[0]
        if txmin > txmax: txmin, txmax = txmax, txmin

        tymin = (i.minPt[1]-viewPoint[1])/ray[1]
        tymax = (i.maxPt[1]-viewPoint[1])/ray[1]
        if tymin > tymax: tymin, tymax = tymax, tymin


        if txmin > tymax or tymin > txmax:
            result = 0

        if tymin > txmin:
            txmin = tymin
        if tymax < txmax:
            txmax = tymax

        tzmin = (i.minPt[2]-viewPoint[2])/ray[2]
        tzmax = (i.maxPt[2]-viewPoint[2])/ray[2]
        if tzmin > tzmax: tzmin, tzmax = tzmax, tzmin

        if txmin > tzmax or tzmin > txmax:
            result = 0

        if tzmin >= txmin:
            txmin = tzmin
        if tzmax < txmax:
            txmax = tzmax

        if result == 1 and m >= txmin:
                m = txmin
                collisionFlag = count

class Camera:
    def __init__(self):
        self.viewPoint = np.array([0, 0, 0]).astype(np.float)
        self.viewDir = np.array([0, 0, -1]).astype(np.float)
        self.viewUp = np.array([0, 1, 0]).astype(np.float)
        self.viewProjNormal = -1 * self.viewDir
        self.viewWidth = 1.0
        self.viewHeight = 1.0
        self.projDistance = 1.0
        self.intensity = np.array([1, 1, 1]).astype(np.float)  # how bright the light is.

class Light:
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

collisionFlag = -1
m = MAX
x = 0 
y = 0 
z = 0
list = []
light = []
imgSize = None
camera = Camera()

#법선 벡터 만들어줌.
def makeNormal(x, y, z):
    dir = np.cross((y-x), (z-x))
    d = np.sum(dir*z)
    return np.array([dir[0], dir[1], dir[2], d])

def rayTrace(ray, viewPoint):
    global list, light, MAX, m, collisionFlag
    m = MAX
    collisionFlag = -1
    count = 0

    for i in list:
        if i.__class__.__name__ == 'Sphere':
            a = np.sum(ray * ray)
            b = np.sum((viewPoint - i.c) * ray)
            c = np.sum((viewPoint - i.c) ** 2) - i.r ** 2
            Sphere.raySphere(a,b,c,count)

        elif i.__class__.__name__ == 'Box':
            Box.rayBox(i,viewPoint, ray, count)

        count = count + 1
    return [m, collisionFlag]

def normalize(vector):
    return vector/math.sqrt(np.dot(vector, vector))


def shade( ray, collisionFlag):
    global list, light, camera, x, y, z, m
    if collisionFlag == -1:
        return np.array([0, 0, 0])

    else: #intersection 있을때.
        x = 0
        y = 0
        z = 0        
        normalVector = np.array([0, 0, 0])
        v = -m*ray

        if list[collisionFlag].__class__.__name__ == 'Sphere':
            normalVector = camera.viewPoint + m*ray - list[collisionFlag].c

            normalVector = normalize(normalVector)

        elif list[collisionFlag].__class__.__name__ == 'Box':
            sub = MAX
            point_i = camera.viewPoint + m * ray
            
            i = -1
            count = 0

            for normal in list[collisionFlag].n:
                if abs(np.sum(normal[0:3] * point_i)-normal[3]) < sub:
                    sub = abs(np.sum(normal[0:3] * point_i)-normal[3])
                    i = count
                count = count + 1
            normalVector = list[collisionFlag].n[i][0:3]
            normalVector = normalize(normalVector)

        for index in light:
            
            #Light의 합.
            lightIntensity = v + index.position - camera.viewPoint
            lightIntensity = normalize(lightIntensity)
            temp = rayTrace(-lightIntensity, index.position)

            if temp[1] == collisionFlag:
                if list[collisionFlag].s.__class__.__name__ == 'ShaderPhong':
                    ShaderPhong.shadePhong(v, lightIntensity, normalVector, index)
                    
                elif list[collisionFlag].s.__class__.__name__ == "ShaderLambertian":
                    ShaderLambertian.shadeLam(lightIntensity, index, normalVector)
                    
        res = Color(x, y, z)
        res.gammaCorrect(2.2)
        return res.toUINT8()



def main():
    global list, light, imgSize, camera
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    parse(root)
    
    # Create an empty image
    channels = 3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:, :] = 0

    
    dx = camera.viewWidth / imgSize[0]
    dy = camera.viewHeight / imgSize[1]

    #카메라 위치.
    w = camera.viewDir
    normalW = normalize(w)

    u = np.cross(w, camera.viewUp)
    normalU = normalize(u)

    v = np.cross(w, u)
    normalV = normalize(v)

    start = normalW * camera.projDistance - normalU * dx * ((imgSize[0]/2) + 1/2) - normalV * dy * ((imgSize[1]/2) + 1/2)
    
    for x in np.arange(imgSize[0]):
        for y in np.arange(imgSize[1]):
            ray = start + normalU * x * dx + dy * y * normalV
            rayAndCollision = rayTrace(ray, camera.viewPoint)
            img[y][x] = shade(ray, rayAndCollision[1])

    rawimg = Image.fromarray(img, 'RGB')
    rawimg.save(sys.argv[1] + '.png')


def parse(root):
    global imgSize, light, list, camera
    imgSize = np.array(root.findtext('image').split()).astype(np.int)

    for c in root.findall('camera'):
        camera.viewPoint = np.array(c.findtext('viewPoint').split()).astype(np.float)
        camera.viewDir = np.array(c.findtext('viewDir').split()).astype(np.float)
        if (c.findtext('projNormal')):
            camera.viewProjNormal = np.array(c.findtext('projNormal').split()).astype(np.float)
        camera.viewUp = np.array(c.findtext('viewUp').split()).astype(np.float)
        if (c.findtext('projDistance')):
            camera.projDistance = np.array(c.findtext('projDistance').split()).astype(np.float)
        camera.viewWidth = np.array(c.findtext('viewWidth').split()).astype(np.float)
        camera.viewHeight = np.array(c.findtext('viewHeight').split()).astype(np.float)
    

    for c in root.findall('surface'):
        shape = c.get('type')
        if shape == 'Sphere':
            sphereCenter = np.array(c.findtext('center').split()).astype(np.float)
            sphereRadius = np.array(c.findtext('radius')).astype(np.float)
            refColor = ''
            for child in c:
                if child.tag == 'shader':
                    refColor = child.get('ref')
            
            #shader 확인
            for d in root.findall('shader'):
                if d.get('name') == refColor:
                    diffuseColor = np.array(d.findtext('diffuseColor').split()).astype(np.float)
                    typeShading = d.get('type')
                    if typeShading == 'Lambertian':
                        shader = ShaderLambertian(diffuseColor)
                        list.append(Sphere(sphereCenter, sphereRadius, shader))

                    elif typeShading == 'Phong':
                        exponent = np.array(d.findtext('exponent').split()).astype(np.float)
                        specular = np.array(d.findtext('specularColor').split()).astype(np.float)
                        shader = ShaderPhong(diffuseColor, specular, exponent)
                        list.append(Sphere(sphereCenter, sphereRadius, shader))

        elif shape == 'Box':
            minPt_c = np.array(c.findtext('minPt').split()).astype(np.float)
            maxPt_c = np.array(c.findtext('maxPt').split()).astype(np.float)

            point1 = np.array([minPt_c[0], minPt_c[1], maxPt_c[2]])
            point2 = np.array([minPt_c[0], maxPt_c[1], minPt_c[2]])
            point3 = np.array([maxPt_c[0], minPt_c[1], minPt_c[2]])
            point4 = np.array([minPt_c[0], maxPt_c[1], maxPt_c[2]])
            point5 = np.array([maxPt_c[0], minPt_c[1], maxPt_c[2]])
            point6 = np.array([maxPt_c[0], maxPt_c[1], minPt_c[2]])

            normals = []
            #normal 벡터 넣어줌.
            normals.append(makeNormal(point1, point3, point5))
            normals.append(makeNormal(point2, point3, point6))
            normals.append(makeNormal(point1, point2, point4))
            normals.append(makeNormal(point1, point5, point4))
            normals.append(makeNormal(point5, point3, point6))
            normals.append(makeNormal(point4, point6, point2))

            refColor = '' # blue, red, green ...
            for child in c:
                if child.tag == 'shader':
                    refColor = child.get('ref')
            for d in root.findall('shader'):
                if d.get('name') == refColor:
                    diffuseColor = np.array(d.findtext('diffuseColor').split()).astype(np.float)
                    typeShading = d.get('type')
                    if typeShading == 'Lambertian':
                        shader = ShaderLambertian(diffuseColor)
                        list.append(Box(minPt_c, maxPt_c, shader, normals))
                    elif typeShading == 'Phong':
                        exponent = np.array(d.findtext('exponent').split()).astype(np.float)
                        specular = np.array(d.findtext('specularColor').split()).astype(np.float)
                        shader = ShaderPhong(diffuseColor, specular, exponent)
                        list.append(Box(minPt_c, maxPt_c, shader, normals))

    for c in root.findall('light'):
        position = np.array(c.findtext('position').split()).astype(np.float)
        intensity = np.array(c.findtext('intensity').split()).astype(np.float)
        light.append(Light(position, intensity))




if __name__ == "__main__":
    main()
