import time, math

#helper functions for math operations and such

#returns the greatest common divisor between 2 numbers
def gcd(a, b):
  if b == 0:
    return a
  return gcm(b, a%b)

#returns the lowest common multiple between 2 numbers
def lcm(a, b):
  return abs(a*b) // gcd(a,b)

class Point:
  def __init__(self, x=0, y=0, z=0):
    self.x = x
    self.y = y
    self.z = z
  
  def outputMatrix(self):
    return [self.x, self.y, self.z]

class Vector: 
  #create a new vector from vector direction magnitudes and a given point
  def __init__(self, magX=0, magY=0, magZ=0, p=Point(0,0,0)):
    self.magX=magX
    self.magY=magY
    self.magZ=magZ
    self.point=p
    
  #create a new vector from 2 points
  @classmethod
  def fromPoints(cls, p1=Point(0,0,0), p2=Point(0,0,0)):
    #setup vector magnitude
    magX=p2.x-p1.x
    magY=p2.y-p1.y
    magZ=p2.z-p1.z
    return cls(magX, magY, magZ, p1)      
  
  #returns a matrix for the magnitudes of x, y and z respectively
  def magnitudeMatrix(self):
    return [self.magX, self.magY, self.magZ]
  
  #returns the length of the vector
  def length(self):
    return sqrt((self.magX) ** 2 + (self.magY) ** 2 + (self.magZ) ** 2)
  
  #returns the cross product of the vector and a given vector
  def cross(self, vec):
    return Vector(self.magY*vec.magZ - self.magZ*vec.magY, self.magZ*vec.magX - self.magX*vec.magZ, self.magX*vec.magY - self.magY*vec.magX) 
  
  #returns the dot product of the vector and a given vector
  def dot(self, vec):
    return self.magX * vec.magX + self.magY * vec.magY + self.magZ * vec.magZ
  
  #checks if a given point is on the vector
  def checkIfPointOnLine(self, p):
    cross=self.cross(Vector(p.x - self.magX, p.y - self.magY, p.z - self.magZ)) 
    if cross.length() != 0:
      return false
    return true
  
    
  #checks if a given vector is colinear to the vector
  def checkIfColinear(self, vec):
    if self.cross(vec).length() != 0:
      return false
    return true
    
  #returns the point of intersection between a given vector and the vector
  def vectorToVectorIntersection(self, vec):
   #if vectors are colinear
   if self.checkIfColinear(vec):
     return self.point
   #use lcm to eliminate t2
   et2 = lcm(vec.magX, vec.magY)
   #solve for t1
   t1=((et2/vec.magX * vec.point.x - et2/vec.magY * vec.point.y) - (et2/vec.magX * self.point.x - et2/vec.magY * self.point.y))/(et2/vec.magX * self.magX - et2/vec.magY * self.magY)
   t2=((self.point.x+self.magX * t1 - vec.point.x)/self.magX)
   #calculate point of intersection
   ix = self.point.x + self.magX*t1
   iy = self.point.y + self.magY*t1
   iz= self.point.z + self.magZ*t1
   return Point(ix, iy, iz)
   
'''
v1=Vector(1, -2, -3, Point(5,2,-1))
v2=Vector(1, 2, -1, Point(2,0,4))
print Vector.vectorToVectorIntersection(v1, v2).outputMatrix()


a=Vector(0, 0, 1)
b=Vector(-3,4,1)
p=Point(0, 0, 10)
pl=Plane(a, Point(0, 0, 0))

print Vector.magnitudeMatrix(a.cross(b))
print Vector.checkIfPointOnLine(a, p)
print pl.checkIfPointOnPlane(p)  
'''
        
class Plane: 
  #creates a plane from a normal vector and a point that lies on the plane
  def __init__(self, scalX, scalY, scalZ, scalD):
    self.scalX=scalX
    self.scalY=scalY
    self.scalZ=scalZ
    self.scalD=scalD
  
  @classmethod
  def fromNormalAndPoint(cls, normal, p):
    #setup scalar equation
    scalX=normal.magX
    scalY=normal.magY
    scalZ=normal.magZ
    scalD=0-scalX*p.x-scalY*p.y-scalZ*p.z
    
    return cls(scalX, scalY, scalZ, scalD)
  
  #checks if a given point lies on the plane
  def checkIfPointOnPlane(self, p):
    eq=self.scalX*p.x+self.scalY*p.y+self.scalZ*p.z
    if eq + self.scalD != 0:
      return false
    return true
    
  #find the intersection between a line and the plane
  def lineToPlaneIntersection(self, line):
    try:
      t=(self.scalD-self.scalX*line.point.x - self.scalY*line.point.y - self.scalY*line.point.y)/(self.scalX*line.magX+self.scalY*line.magY+self.scalY*line.magY)
      #calculate point of intersection
      ix=line.point.x+line.magX
      iy=line.point.y+line.magY
      iz=line.point.z+line.magZ
      return Point(ix, iy, iz)
    except:
      return Point(0, 0, 0)    

#v=Vector.fromPoints(Point(0,0,0), Point(0, 0, 0))
p2=Plane.fromNormalAndPoint(Vector(0, 1, 3), Point(0, 0, 0))
'''
pl=Plane(1, -1,2,-9)
v1=Vector(-1, 1, 5, Point(3, 2, 0))
print pl.lineToPlaneIntersection(v1).outputMatrix()
'''

class Scene:
  def __init__(self, viewportWidth, viewportHeight):
    self.viewportWidth = viewportWidth
    self.viewportHeight = viewportHeight
    self.cameras=[]
    self.points=[]
    
  def addPoint(self, point): 
    self.points.append(point)
    
  def addCamera(self, origin, fov):
    camera = Camera(origin, fov, self)
    self.cameras.append(camera)
    return camera

class Camera: 
  def __init__(self, origin, fov, scene):
    self.origin = origin
    #field of view
    self.fov = fov
    self.attachToScene(scene)
    
  def attachToScene(self, scene):
     self.scene = scene
     #self.plane = Plane.fromNormalAndPoint(self.direction, self.clipping)
     #print self.plane
     self.canvas=[]
     self.picture=makeEmptyPicture(scene.viewportWidth, scene.viewportHeight, black)
     
  def renderScenePoints(self, color=blue):
    while (True):
      i=len(self.scene.points)
      while (i > 0):     
        #goto next point    
        i-=1
        #print "clearing!"
        p=self.scene.points[i]
        p.z-=1
      
        try:
          scale=int(math.ceil(float(self.fov/(p.z+self.fov))))
        except:
          scale=1
        bx=(p.x * scale) + self.scene.viewportWidth/2
        by=(p.y * scale) + self.scene.viewportHeight/2
     # print str(bx) + " " + str(by)
        if not (bx < 0 or bx >= self.scene.viewportWidth or by < 0 or by >= self.scene.viewportHeight): 
        #print "Painting to picture"
          setColor(getPixelAt(self.picture, bx, by), color)
          
        
      #reset pixel
        
        if (p.z < -self.fov):
          p.z += self.fov*2
        
    #show(self.picture)
      repaint(self.picture)
      time.sleep(0.1)
      #
      #repaint(self.picture)
    return self.canvas
      
    
def main():
  scene=Scene(700, 500)
  
  #lay points on floor
  for x in range(-250, 250, 5):
    for z in range(-250, 250, 5):
      scene.addPoint(Point(x, 10, z))
  
  camera=scene.addCamera(Point(0, 0, 0), 250)
  #setColor(getPixelAt(camera.picture, cx + camera.scene.viewportWidth/2, cy + camera.scene.viewportHeight/2), red)
  #show(camera.picture)
  camera.renderScenePoints(cyan)
  #time.sleep(0.01)
  #clear canvas
  #addRectFilled(camera.picture, 0, 0, camera.scene.viewportWidth, camera.scene.viewportHeight, white)
 
  
  
#main()
