"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
download: https://github.com/horstjens/catapults3d
idea: python3/pygame 3d vector rts game

"""
import pygame
import random
import os

def mouseVector():
    return pygame.math.Vector2(pygame.mouse.get_pos()[0],
                               - pygame.mouse.get_pos()[1])
def randomize_color(color, delta=50):
    d=random.randint(-delta, delta)
    color = color + d
    color = min(255,color)
    color = max(0, color)
    return color

def make_text(msg="pygame is cool", fontcolor=(255, 0, 255), fontsize=42, font=None):
    """returns pygame surface with text. You still need to blit the surface."""
    myfont = pygame.font.SysFont(font, fontsize)
    mytext = myfont.render(msg, True, fontcolor)
    mytext = mytext.convert_alpha()
    return mytext

def write(background, text="bla", pos=None, color=(0,0,0),
          fontsize=None, center=False, x=None, y=None):
        """write text on pygame surface. pos is a 2d Vector """
        if pos is None and (x is None or y is None):
            print("Error with write function: no pos argument given and also no x and y:", pos, x, y)
            return
        if pos is not None:
            # pos has higher priority than x or y
            x = pos.x
            y = -pos.y
        if fontsize is None:
            fontsize = 24
        font = pygame.font.SysFont('mono', fontsize, bold=True)
        fw, fh = font.size(text)
        surface = font.render(text, True, color)
        if center: # center text around x,y
            background.blit(surface, (x-fw//2, y-fh//2))
        else:      # topleft corner is x,y
            background.blit(surface, (x,y))

def get_height_color(number):
    """ takes a number (height-value) from 0 to 255 and returns a color value. white for top (snow), green for lowlands etc. ..."""
    if number < 10:    # 0-10
        color = (178, 240, 245-number)
    elif number < 30:    # 10-30
        color = (179 + (number-10),241 ,204 )
    elif number < 40:    # 30-40
        color = (195,247 ,173+ (number-30)) 
    elif number < 50:    # 40-50
        color = (231, 253-(number-40), 178) 
    elif number < 60:    # 50-60
        color = (195, 227-(number-50), 126) 
    elif number < 70:   # 60-70
        color = (94,189 - (number-60) ,63 ) 
    elif number < 80:   # 70-80
        color = (21,147 - (number-70) ,47 )
    elif number < 90:   # 80-90
        color = (49 + (number-80),136 ,58 )
    elif number < 100:  # 90-100
        color = (122,155 + (number-90) ,50 )
    elif number < 110:  # 100-110
        color = (192,173 ,34 - (number-100) )
    elif number < 120:  # 110-120
        color = (230,173 - (number-110) ,4 )
    elif number < 130:  # 120-130
        color = (245,161 + (number-120) ,1 )
    elif number < 140:  # 130-140
        color = (255,194 - (number-130) ,5 )
    elif number < 150:  # 140-150
        color = (255,147 - (number-140),74 )
    elif number < 160:  # 150-160
        color = (225 - (number-150),122 ,71 )
    elif number < 170:  # 160-170
        color = (202 - (number-160),89 ,75 )
    elif number < 180:  # 170-180
        color = (193,60 + (number-170) ,1 )
    elif number < 190:  # 180-190
        color = (117 + (number-180),66 ,21 )
    elif number < 200:  # 190-200
        color = (137 + (number-190),99 ,76 )
    elif number < 210:  #200-210
        color = (164 + (number-200),142 ,121)
    elif number < 220:  #210-220
        color = (176 + number-210,176+ number-210 ,176+ number-210 )
    elif number < 230: #220-230
        color = (226 + number-220,226+number-220 ,226+number-220 )
    elif number < 240: #230-240
        color = (236+number-230,236+number-230 ,236+number-230 ) 
    else:              #240-255
        color = (236+number-240,236+number-240 ,236+number-240 ) 
    return color

def elastic_collision(sprite1, sprite2):
        """elasitc collision between 2 VectorSprites (calculated as disc's).
           The function alters the dx and dy movement vectors of both sprites.
           The sprites need the property .mass, .radius, pos.x pos.y, move.x, move.y
           by Leonard Michlmayr"""
        if sprite1.static and sprite2.static:
            return 
        dirx = sprite1.pos.x - sprite2.pos.x
        diry = sprite1.pos.y - sprite2.pos.y
        sumofmasses = sprite1.mass + sprite2.mass
        sx = (sprite1.move.x * sprite1.mass + sprite2.move.x * sprite2.mass) / sumofmasses
        sy = (sprite1.move.y * sprite1.mass + sprite2.move.y * sprite2.mass) / sumofmasses
        bdxs = sprite2.move.x - sx
        bdys = sprite2.move.y - sy
        cbdxs = sprite1.move.x - sx
        cbdys = sprite1.move.y - sy
        distancesquare = dirx * dirx + diry * diry
        if distancesquare == 0:
            dirx = random.randint(0,11) - 5.5
            diry = random.randint(0,11) - 5.5
            distancesquare = dirx * dirx + diry * diry
        dp = (bdxs * dirx + bdys * diry) # scalar product
        dp /= distancesquare # divide by distance * distance.
        cdp = (cbdxs * dirx + cbdys * diry)
        cdp /= distancesquare
        if dp > 0:
            if not sprite2.static:
                sprite2.move.x -= 2 * dirx * dp
                sprite2.move.y -= 2 * diry * dp
            if not sprite1.static:
                sprite1.move.x -= 2 * dirx * cdp
                sprite1.move.y -= 2 * diry * cdp


class VectorSprite(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0
    numbers = {} # { number, Sprite }

    def __init__(self, **kwargs):
        self._default_parameters(**kwargs)
        self._overwrite_parameters()
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        self.number = VectorSprite.number # unique number for each sprite
        VectorSprite.number += 1
        VectorSprite.numbers[self.number] = self
        self.create_image()
        self.distance_traveled = 0 # in pixel
        #self.rect.center = (-300,-300) # avoid blinking image in topleft corner
        if self.angle != 0:
            self.set_angle(self.angle)
        self.tail = [] 

    def _overwrite_parameters(self):
        """change parameters before create_image is called""" 
        pass

    def _default_parameters(self, **kwargs):    
        """get unlimited named arguments and turn them into attributes
           default values for missing keywords"""

        for key, arg in kwargs.items():
            setattr(self, key, arg)
        if "layer" not in kwargs:
            self._layer = 4
        else:
            self._layer = self.layer
        if "zoom" not in kwargs:
            self.zoom = 1
        self.old_zoom = self.zoom # make copy!
        if "name" not in kwargs:
            self.name = None
        if "static" not in kwargs:
            self.static = False
        if "selected" not in kwargs:
            self.selected = False
        if "pos" not in kwargs:
            self.pos = pygame.math.Vector2(random.randint(0, Viewer.width),-50)
        if "move" not in kwargs:
            self.move = pygame.math.Vector2(0,0)
        if "fontsize" not in kwargs:
            self.fontsize = 22
        if "friction" not in kwargs:
            self.friction = 1.0 # no friction
        if "radius" not in kwargs:
            self.radius = 5
        if "width" not in kwargs:
            self.width = self.radius * 2
        if "height" not in kwargs:
            self.height = self.radius * 2
        
        if "hitpoints" not in kwargs:
            self.hitpoints = 100
        self.hitpointsfull = self.hitpoints # makes a copy
        if "mass" not in kwargs:
            self.mass = 10
        if "damage" not in kwargs:
            self.damage = 10
        if "bounce_on_edge" not in kwargs:
            self.bounce_on_edge = False
        if "kill_on_edge" not in kwargs:
            self.kill_on_edge = False
        if "angle" not in kwargs:
            self.angle = 0 # facing right?
        if "max_age" not in kwargs:
            self.max_age = None
        if "max_distance" not in kwargs:
            self.max_distance = None
        if "picture" not in kwargs:
            self.picture = None
        if "bossnumber" not in kwargs:
            self.bossnumber = None
        if "kill_with_boss" not in kwargs:
            self.kill_with_boss = False
        if "sticky_with_boss" not in kwargs:
            self.sticky_with_boss = False
        if "mass" not in kwargs:
            self.mass = 15
        if "upkey" not in kwargs:
            self.upkey = None
        if "downkey" not in kwargs:
            self.downkey = None
        if "rightkey" not in kwargs:
            self.rightkey = None
        if "leftkey" not in kwargs:
            self.leftkey = None
        if "speed" not in kwargs:
            self.speed = None
        if "age" not in kwargs:
            self.age = 0 # age in seconds
        if "warp_on_edge" not in kwargs:
            self.warp_on_edge = False
        if "gravity" not in kwargs:
            self.gravity = None
        if "survive_north" not in kwargs:
            self.survive_north = False
        if "survive_south" not in kwargs:
            self.survive_south = False
        if "survive_west" not in kwargs:
            self.survive_west = False
        if "survive_east" not in kwargs:
            self.survive_east = False
        if "speed" not in kwargs:
            self.speed = 0
        if "color" not in kwargs:
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

    def kill(self):
        if self.number in self.numbers:
           del VectorSprite.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)
    
   
    
    def create_image(self):
        if self.picture is not None:
            self.image = self.picture.copy()
        elif self.name is not None:
            self.image = Viewer.zoom_images[self.name][self.zoom]
            self.image0 = self.image.copy()
        else:
            self.image = pygame.Surface((self.width,self.height))
            self.image.fill((self.color))
            self.image = self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect= self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
    

    
    def rotate_to(self, final_degree):
        if final_degree < self.angle:
            self.rotate(- self.turnspeed)
        elif final_degree > self.angle:
            self.rotate(self.turnspeed)
        else:
            return
        
        
    def rotate(self, by_degree):
        """rotates a sprite and changes it's angle by by_degree"""
        self.angle += by_degree
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def set_angle(self, degree):
        """rotates a sprite and changes it's angle to degree"""
        self.angle = degree
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        #self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        # ----- kill because... ------
        if self.hitpoints <= 0:
            self.kill()
        if self.max_age is not None and self.age > self.max_age:
            self.kill()
        if self.max_distance is not None and self.distance_traveled > self.max_distance:
            self.kill()
        # ---- movement with/without boss ----
        if self.bossnumber is not None:
            if self.kill_with_boss:
                if self.bossnumber not in VectorSprite.numbers:
                    self.kill()
            if self.sticky_with_boss and self.bossnumber in VectorSprite.numbers:
                boss = VectorSprite.numbers[self.bossnumber]
                self.pos = pygame.math.Vector2(boss.pos.x, boss.pos.y)
                self.set_angle(boss.angle)
        self.pos += self.move * seconds
        self.move *= self.friction 
        self.distance_traveled += self.move.length() * seconds
        self.age += seconds
        self.wallbounce()
        self.rect.center = ( round(self.pos.x, 0), -round(self.pos.y, 0) )
        
    def worldrect(self, offset_x, offset_y, zoom):
        x = self.pos.x + offset_x
        y = self.pos.y - offset_y
        self.rect.center = ( round(x,0), -round(y,0))



    def wallbounce(self):
        # ---- bounce / kill on screen edge ----
        # ------- left edge ----
        if self.pos.x < 0:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = 0
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = Viewer.width 
        # -------- upper edge -----
        if self.pos.y  > 0:
            if self.kill_on_edge and not self.survive_north:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = 0
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = -Viewer.height
        # -------- right edge -----                
        if self.pos.x  > Viewer.width:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = Viewer.width
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = 0
        # --------- lower edge ------------
        if self.pos.y   < -Viewer.height:
            if self.kill_on_edge:
                self.hitpoints = 0
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = -Viewer.height
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = 0

class Wall(VectorSprite):
    
    def _overwrite_parameters(self):
        self.name = "wall"
        self._layer = 3
        #self.z = int(self.z)
        
    def update(self, seconds):
        if self.old_zoom != self.zoom:
            self.create_image()
        self.old_zoom = self.zoom
    
class Turret(VectorSprite):
    
    def _overwrite_parameters(self):
        self.name = "tower"
        self._layer = 3
        #self.z = int(self.z)
       

        
    def update(self, seconds):
        if self.old_zoom != self.zoom:
            self.create_image()
        self.old_zoom = self.zoom
        #if random.random() < 0.01:
        #    self.rotate(random.choice((-3,-2,-1,-1,0,1,1,2,3)))
        #VectorSprite.update(self, seconds)
        #if random.random() < 0.01:
        #    m = pygame.math.Vector2(100,0)
        #    m.rotate_ip(self.angle)
        #    Rock(pos=pygame.math.Vector2(self.pos.x, self.pos.y), move=m, max_distance=1000, angle=self.angle, start_z=self.z+20, bossnumber=self.number)
      


class Javelin(VectorSprite):
    
    def _overwrite_parameters(self):
        self.speed = 150
        self.start_z = int(self.start_z)
        self.name = "javelin"

    def update(self, seconds):
        if self.old_zoom != self.zoom:
            self.create_image()
        self.old_zoom = self.zoom
        VectorSprite.update(self, seconds)


class Rock(VectorSprite):
    
    def _overwrite_parameters(self):
        self.speed = 150
        self.start_z = int(self.start_z)
        self.name = "rock"
        self_layer = 6
 
 
    def update(self, seconds):
        if self.old_zoom != self.zoom:
            self.create_image()
        self.old_zoom = self.zoom
        VectorSprite.update(self, seconds)

                

class Cannonball(VectorSprite):
    """3d sprite"""
    
    def _overwrite_parameters(self):
        self.speed = 3
        self.pos3 = pygame.math.Vector3(self.pos.x, self.pos.y, 0)
        self.move3 = pygame.math.Vector3(self.move.x, self.move.y, 300)
        
    
    def create_image(self):
        self.image = pygame.surface.Surface((20,20))    
        z = min(255, self.pos3.z)
        z= max(0, self.pos3.z)
        pygame.draw.circle(self.image, (0,0,z), (10,10),10)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        self.pos3 += self.move3 * seconds
        # gravity
        self.move3 += pygame.math.Vector3(0,0,-5)
        # hit earth?
        if self.pos3.z < 0:
            self.kill()
        self.pos = pygame.math.Vector2(self.pos3.x, self.pos3.y)
        self.move = pygame.math.Vector2(self.move3.x, self.move3.y)
        oldcenter = self.rect.center
        self.create_image()
        self.rect.center = oldcenter
        #print(self.pos3, self.move3)

class TileCursor(VectorSprite):
    
    def _overwrite_parameters(self):
        pass
        
    def create_image(self):
        self.image = pygame.surface.Surface((Viewer.tilesize, Viewer.tilesize))
        color = random.randint(128,255)
        pygame.draw.rect(self.image, (color,color,color), (0,0,Viewer.tilesize, Viewer.tilesize), 2)
        self.image.set_colorkey((0,0,0))
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
    def update(self, seconds):
        VectorSprite.update(self,seconds)
        oldcenter = self.rect.center
        self.create_image()
        self.rect.center = oldcenter
        
        

class Ballista(VectorSprite):
    
    def _overwrite_parameters(self):
        self.speed = 3
    
    def create_image(self):
        self.image=Viewer.images["ballista1"]
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
    def update(self,seconds):
        VectorSprite.update(self,seconds)
        # - - - - - - go to mouse cursor ------ #
        target = mouseVector()
        dist =target - self.pos
        try:
            dist.normalize_ip() #schrupmft ihn zur länge 1
        except:
            print("i could not normalize", dist)
            return
        dist *= self.speed  
        rightvector = pygame.math.Vector2(1,0)
        angle = -dist.angle_to(rightvector)
        #print(angle)
        #if self.angle == round(angle, 0):
        if self.selected:
            self.move = dist
            self.set_angle(angle)
            pygame.draw.rect(self.image, (0,200,0), (0,0,self.rect.width, self.rect.height),1)
        # ------ fire sometimes ----
        if random.random() < 0.01:
            p = pygame.math.Vector2(self.pos.x, self.pos.y)
            m = pygame.math.Vector2(1,0)
            m.rotate_ip(self.angle)
            m *= 150    
            Javelin(pos=p,move=m, angle= self.angle, bossnumber=self.number)

class Tile(VectorSprite):
    
    #def _overwrite_parameters(self):
    #    
    #    if self.colorchar in Viewer.legend:
    #        self.color = Viewer.legend[self.colorchar]
    #    else:
    #        self.color = (255,193,203)
                      
        
    def create_image(self):
        self.image = pygame.surface.Surface((self.tilesize, self.tilesize))
        self.image.fill((self.color))
        self.image.set_colorkey((0,0,0))
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
         

class Catapult(VectorSprite):
    
    def _overwrite_parameters(self):
        self.name = "catapult"
        #self.z = int(self.z)
        self._layer = 4
        print("Catapult created")
       

        
    def update(self, seconds):
        if self.old_zoom != self.zoom:
            self.create_image()
        self.old_zoom = self.zoom
        if random.random() < 0.01:
            self.rotate(random.choice((-3,-2,-1,-1,0,1,1,2,3)))
        VectorSprite.update(self, seconds)
        if random.random() < 0.01:
            m = pygame.math.Vector2(100,0)
            m.rotate_ip(self.angle)
            Rock(pos=pygame.math.Vector2(self.pos.x, self.pos.y), move=m, max_distance=1000, angle=self.angle, start_z=self.z+20, bossnumber=self.number, zoom=self.zoom)
      



class Swordgoblin(VectorSprite):
    

    
    def new_move(self):
        self.angle = random.randint(0,360)
        self.speed = random.randint(40,140)
        self.move = pygame.math.Vector2(self.speed, 0)
        self.move.rotate_ip(self.angle)
        self.set_angle(self.angle)
        
    
    def _overwrite_parameters(self):
        #self.speed = 75
        #self.new_move()
        #self.bounce_on_edge = True
        max_age = 5
        self.name = "swordgoblin"
        self.z = 200
        #self.z = int(self.z)    


        
    def update(self,seconds):
        
        if self.old_zoom != self.zoom:
            self.create_image()
        self.old_zoom = self.zoom

        VectorSprite.update(self,seconds)
        if random.random() < 0.002:
            self.new_move()
        if random.random() < 0.01:
            m = pygame.math.Vector2(100,0)
            m.rotate_ip(self.angle)
            Javelin(pos=pygame.math.Vector2(self.pos.x, self.pos.y), move=m, max_distance=1000, angle=self.angle, start_z=self.z+20, bossnumber=self.number, zoom=self.zoom)
      

            
class Tent(VectorSprite):
    
    def _overwrite_parameters(self):
        self.spawntime = 5.0
        self.spawn = 0
        self.name = "tent"
        
        
    def update(self,seconds):
        
        if self.old_zoom != self.zoom:
            self.create_image()
        self.old_zoom = self.zoom

        VectorSprite.update(self,seconds)
        self.spawn += seconds
        if self.spawn > self.spawntime:
            Swordgoblin(pos=pygame.math.Vector2(self.pos.x, self.pos.y), zoom=self.zoom)
            self.spawn = 0


class Flytext(VectorSprite):
    
    def _overwrite_parameters(self):
        self._layer = 7  # order of sprite layers (before / behind other sprites)
        self.r, self.g, self.b = self.color
        if self.max_age is None:
            self.max_age = 2
        
        
    def create_image(self):
        self.image = make_text(self.text, (self.r, self.g, self.b), self.fontsize)  # font 22
        self.rect = self.image.get_rect()
        

class Spark(VectorSprite):
    
    def _overwrite_parameters(self):
        self._layer = 9
        self.kill_on_edge = True
        
    def create_image(self):
        r,g,b = self.color
        r = randomize_color(r,50)
        g = randomize_color(g,50)
        b = randomize_color(b,50)
        self.image = pygame.Surface((10,10))
        pygame.draw.line(self.image, (r,g,b), 
                         (10,5), (5,5), 3)
        pygame.draw.line(self.image, (r,g,b),
                          (5,5), (2,5), 1)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()                          
        

class Explosion():
    """emits a lot of sparks, for Explosion or Player engine"""
    def __init__(self, posvector, minangle=0, maxangle=360, maxlifetime=3,
                 minspeed=5, maxspeed=150, red=255, red_delta=0, 
                 green=225, green_delta=25, blue=0, blue_delta=0,
                 minsparks=5, maxsparks=20):
        for s in range(random.randint(minsparks,maxsparks)):
            v = pygame.math.Vector2(1,0) # vector aiming right (0°)
            a = random.randint(minangle,maxangle)
            v.rotate_ip(a)
            speed = random.randint(minspeed, maxspeed)
            duration = random.random() * maxlifetime # in seconds
            red   = randomize_color(red, red_delta)
            green = randomize_color(green, green_delta)
            blue  = randomize_color(blue, blue_delta)
            Spark(pos=pygame.math.Vector2(posvector.x, posvector.y),
                  angle= a, move=v*speed, max_age = duration, 
                  color=(red,green,blue), kill_on_edge = True)


            

        
    
    

class Viewer(object):
    width = 0
    height = 0
    world_width = 0
    world_height = 0
    tilesize = 32
    images = {}
    zoom_images = {}
    sounds = {}
    menu = {#main
            "main":               ["resume", "map", "settings", "credits", "quit" ],
            
            #map
            "map":                ["back", "load a map", "set water height", "set tile size", "convert png to map"],
            "load a map":         ["back"],
            "convert png to map": ["back"], 
            "set water height":   ["back", "no water"],
            "set tile size":      ["back", "increase tile size", "decrease tile size", "tile size is now: "],
            
            "settings":           ["back", "video", "difficulty", "reset all values"],
            
            #settings
            "video":              ["back", "resolution", "fullscreen"],
            

            
            #video
            "resolution":         ["back"],
            "fullscreen":         ["back", "true", "false"]
            }
    
    
    #legend = {".": ( 0,0,255),
    #          "a": (173,216,230),
    #          "b": (229,229,229),
    #          "c": (191,191,191),
    #          "d": (144,238,144),
    #          "e": (0,128,0)
    #              }
    
    #Viewer.menu["resolution"] = pygame.display.list_modes()
    history = ["main"]
    cursor = 0
    name = "main"
    fullscreen = False

    def __init__(self, width=640, height=400, fps=60):
        """Initialize pygame, window, background, font,...
           default arguments """
        pygame.mixer.pre_init(44100,-16, 2, 2048)   
        pygame.init()
        Viewer.width = width    # make global readable
        Viewer.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((255,255,255)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.world = None
        self.playtime = 0.0
        self.rawmap = []
        self.waterheight = 0
        #Viewer.tilesize = 32
        self.grid = False
        Viewer.menu["set tile size"][-1] = "(The current tile size is: {}x{} pixel)".format(self.tilesize, self.tilesize)
        self.world_offset_x = 0
        self.world_offset_y = 0
        self.world_zoom = 1
        self.radarmap_size = 256
        self.radarmap_zoom = 1.0
        self.radarmap = pygame.surface.Surface((self.radarmap_size, self.radarmap_size))
        # -- menu --
        # --- create screen resolution list ---
        li = ["back"]
        for i in pygame.display.list_modes():
            # li is something like "(800, 600)"
            pair = str(i)
            comma = pair.find(",")
            x = pair[1:comma]
            y = pair[comma+2:-1]
            li.append(str(x)+"x"+str(y))
        Viewer.menu["resolution"] = li
        self.set_resolution()
        # ----- get png files -----
        
        
        
        # ------ background images ------
        #self.backgroundfilenames = [] # every .jpg file in folder 'data'
        #try:
        #    for root, dirs, files in os.walk("data"):
        #        for file in files:
        #            if file[-4:] == ".jpg" or file[-5:] == ".jpeg":
        #                self.backgroundfilenames.append(file)
        #    random.shuffle(self.backgroundfilenames) # remix sort order
        #except:
        #    print("no folder 'data' or no jpg files in it")

        self.age = 0
        # ------ joysticks ----
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init()
        
        self.prepare_sprites()
        self.loadbackground()
        self.load_sounds()
        ##self.world = World()
        #print(self.world)
        
        
    def load_sounds(self):
        #Viewer.sounds["click"]=  pygame.mixer.Sound(
        #         os.path.join("data", "panzersound1.wav"))
        return
    
    
    def set_resolution(self):
        if Viewer.fullscreen:
             self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF|pygame.FULLSCREEN)
        else:
             self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.loadbackground()
    
    
    def loadbackground(self):
        
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((0,0,128)) # fill background white
            
        self.background = pygame.transform.scale(self.background,
                          (Viewer.width,Viewer.height))
        self.background.convert()
        
    
    #def paint_world(self):
    #    for y, line in enumerate(self.world.terrain):
    #        for x, tile in enumerate(line):
    #            h = self.world.terrain[y][x]
    #            pygame.draw.rect(self.screen,(h,h,h), (x*10, y*10,10,10))
        
    
    def create_selected(self, original_name):
        Viewer.images[original_name + "_selected"] = Viewer.images[original_name].copy()
        # make green rectangle
        img = Viewer.images[original_name + "_selected"]
        pygame.draw.rect(img, (0,255,0),(0,0,img.get_rect().width,
                                             img.get_rect().height),1)
        img.set_colorkey((0,0,0))
        img.convert_alpha()
        Viewer.images[original_name + "_selected"] = img
        
    
    def load_sprites(self):
            """ all sprites that can rotate MUST look to the right. Edit Image files manually if necessary!"""
            print("loading sprites from 'data' folder....")
        
            Viewer.images["catapult"] = pygame.image.load(os.path.join("data", "catapult1.png")).convert_alpha()
            Viewer.images["rock"] = pygame.image.load(os.path.join("data", "rock.png")).convert_alpha()
            Viewer.images["tent"]= pygame.image.load(os.path.join("data", "tent1.png")).convert_alpha()
            Viewer.images["swordgoblin"]= pygame.image.load(os.path.join("data" , "swordgoblin.png")).convert_alpha()
            Viewer.images["javelin"] = pygame.image.load(os.path.join("data", "javelin.png")).convert_alpha()
            Viewer.images["tower"] = pygame.image.load(os.path.join("data", "tower.png")).convert_alpha()
            Viewer.images["wall"] = pygame.image.load(os.path.join("data", "wall.png")).convert_alpha()
            
                       
            
            
    def zoom_sprites(self):
        """create keys of image name in the dict and as values the smaller images (zoom value 4,3,2,1,0,-1,-2,-3)"""
        # --- scalieren ---
        for name, image in Viewer.images.items():
            Viewer.zoom_images[name] = {}
            i = image.copy()
            for z in range(4, -4, -1):
                Viewer.zoom_images[name][z] = i.copy()
                i = pygame.transform.rotozoom(i, 0.0, 0.5)    # half size image
                
    
    def prepare_sprites(self):
        """painting on the surface and create sprites"""
        self.load_sprites()
        self.zoom_sprites()
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.flytextgroup = pygame.sprite.Group()
        #self.mousegroup = pygame.sprite.Group()
        self.worldgroup = pygame.sprite.Group()
        self.bulletgroup = pygame.sprite.Group()
        self.radargroup = pygame.sprite.Group()
        self.tentgroup = pygame.sprite.Group()
        self.swordgoblingroup = pygame.sprite.Group()
        VectorSprite.groups = self.allgroup
        #Tile.groups = self.allgroup
        Javelin.groups = self.allgroup, self.worldgroup, self.bulletgroup
        Flytext.groups = self.allgroup, self.flytextgroup
        Turret.groups = self.allgroup, self.worldgroup, self.radargroup
        Wall.groups = self.allgroup, self.worldgroup, self.radargroup
        Catapult.groups = self.allgroup, self.worldgroup
        Rock.groups = self.allgroup, self.worldgroup, self.bulletgroup
        Javelin.groups = self.allgroup, self.worldgroup, self.bulletgroup
        Tent.groups = self.allgroup , self.worldgroup
        Swordgoblin.groups = self.allgroup, self.worldgroup, self.swordgoblingroup
        #Catapult.groups = self.allgroup,
        
        # --- tile cursor (number 0) ---
        TileCursor() 
        
        #self.player1 =  Player(imagename="player1", warp_on_edge=True, pos=pygame.math.Vector2(Viewer.width/2-100,-Viewer.height/2))
        #self.player2 =  Player(imagename="player2", angle=180,warp_on_edge=True, pos=pygame.math.Vector2(Viewer.width/2+100,-Viewer.height/2))
        #self.b1 = Ballista()
        #self.c1 = Catapult()
        
        
    def create_sprites(self):
         
        for (x,y) in ((1800,2800), (300,320)):
            Tent(pos=pygame.math.Vector2(x,-y))
        for (x,y) in ((250,300), (300,300), (350,300), (400,300), (450,300)):
            tz = self.get_z(x,y)
            Wall(pos=pygame.math.Vector2(x,-y), z=tz, zoom=1)
        for (x,y) in ((200,300), (800,300), (800, 800), (200,800), (500,550)):
            tz = self.get_z(x,y)
            Turret(pos=pygame.math.Vector2(x,-y), z=tz, zoom = 1)
            Catapult(pos=pygame.math.Vector2(x,-y), z=tz+25, zoom = 1)
            #print("turret z", tz)
        #print("sprites created")
        #for s in self.allgroup:
        #    print(s, s.number) 
    
    
       
    def menu_run(self):
        running = True
        pygame.mouse.set_visible(False)
        while running:
            
            #pygame.mixer.music.pause()
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1 # running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return -1 # running = False
                    if event.key == pygame.K_UP:
                        Viewer.cursor -= 1
                        Viewer.cursor = max(0, Viewer.cursor) # not < 0
                        #Viewer.menusound.play()
                    if event.key == pygame.K_DOWN:
                        Viewer.cursor += 1
                        Viewer.cursor = min(len(Viewer.menu[Viewer.name])-1,Viewer.cursor) # not > menu entries
                        #Viewer.menusound.play()
                    if event.key == pygame.K_RETURN:
                        text = Viewer.menu[Viewer.name][Viewer.cursor]
                        if text == "quit":
                            return -1
                            Viewer.menucommandsound.play()
                        elif text in Viewer.menu:
                            # changing to another menu
                            Viewer.history.append(text) 
                            Viewer.name = text
                            Viewer.cursor = 0
                            #Viewer.menuselectsound.play()
                        elif text == "resume":
                            if self.world is None:
                                Flytext(text="You need to load a map first!", fontsize = 33, color = (200,0,0))
                            else:
                                return
                            #Viewer.menucommandsound.play()
                            #pygame.mixer.music.unpause()
                        elif text == "back":
                            Viewer.history = Viewer.history[:-1] # remove last entry
                            Viewer.cursor = 0
                            Viewer.name = Viewer.history[-1] # get last entry
                            #Viewer.menucommandsound.play()
                            # direct action
                        elif text == "credits":
                            Flytext(text="by Bigm0 and BakTheBig", fontsize = 100, pos=pygame.math.Vector2(400, -100), move=pygame.math.Vector2(0, 10))  
                        elif text == "increase tile size":
                            Viewer.tilesize += 1
                            Viewer.menu["set tile size"][-1] = "(The current tile size is: {}x{} pixel)".format(self.tilesize, self.tilesize)
                        elif text == "decrease tile size":
                            if self.tilesize > 1:
                                Viewer.tilesize -= 1
                                Viewer.menu["set tile size"][-1] = "(The current tile size is: {}x{} pixel)".format(self.tilesize, self.tilesize)
                           
                    

                        if Viewer.name == "resolution":
                            # text is something like 800x600
                            t = text.find("x")
                            if t != -1:
                                x = int(text[:t])
                                y = int(text[t+1:])
                                Viewer.width = x
                                Viewer.height = y
                                self.set_resolution()
                                #Viewer.menucommandsound.play()
                        
                        if Viewer.name == "map":
                            # --- get maps (map*.txt files) ---
                            # --- get png files (*.png)
                            Flytext(text="scanning all .png and .map files from folder maps", pos=pygame.math.Vector2(400, -100), move=pygame.math.Vector2(0, 10))
                            for root, dirs, files in os.walk("maps"):
                                for f in files:
                                    if f[-4:] == ".map":
                                        if f not in Viewer.menu["load a map"]:
                                             Viewer.menu["load a map"].append(f)
                                    elif f[-4:] == ".png":
                                        if f not in Viewer.menu["convert png to map"]:
                                             Viewer.menu["convert png to map"].append(f)
                                break # only this directory

                                    
                        if Viewer.name == "fullscreen":
                            if text == "true":
                                #Viewer.menucommandsound.play()
                                Viewer.fullscreen = True
                                self.set_resolution()
                            elif text == "false":
                                #Viewer.menucommandsound.play()
                                Viewer.fullscreen = False
                                self.set_resolution()
                        if Viewer.name == "set water height":
                            if text != "back":
                                self.waterheight = text
                        if Viewer.name == "convert png to map":
                            if text != "back" and text[-4:] == ".png":
                                name = text[:-4]+".map"
                                print("i try to open", text)
                                pic = pygame.image.load(os.path.join("maps", text))
                                lines = []
                                for y in range(pic.get_height()):
                                    line = []
                                    for x in range(pic.get_width()):
                                        color = pic.get_at((x,y))
                                        line.append(color)
                                        #print("color at ",x,y,"=",color)
                                        # color is a tuple with r, g, b, and alpha?, all integers 0-255
                                    lines.append(line)
                                
                                with open(os.path.join("maps", name), "w") as f:
                                    for line in lines:
                                        textline = ""
                                        for color in line:
                                            textline += str(color[0]) + ","
                                        f.write(textline+"\n")
                                Flytext(text="png converted into map file", pos=pygame.math.Vector2(400, -400), move=pygame.math.Vector2(0, 10))
                                            
                                    
                        if Viewer.name == "load a map":
                            if text[-4:] == ".map":
                                with open(os.path.join("maps", text), "r") as f:
                                    lines = f.readlines()
                                for line in lines:
                                    row = []
                                    for number in line.split(","):
                                        row.append(number)
                                    self.rawmap.append(row)
                                Flytext(text="map loaded: {}".format(text), pos=pygame.math.Vector2(300, -100), move=pygame.math.Vector2(0,20))
                                self.world = True
                                # ------ create radarmap ------
                                self.radarmap = pygame.surface.Surface((len(self.rawmap), len(row)))
                                for y, line in enumerate(self.rawmap):
                                    for x, number in enumerate(line):
                                        if number == "\n":
                                            continue
                                        #print("number:", number)
                                        pygame.draw.rect(self.radarmap, (int(number), int(number), int(number)), (x,y,1,1))
                                self.radarmap.set_colorkey((128,0,128))
                                        
                                # add exiting chars in rawmap to water high
                                #mynumbers = []
                                #for line in self.rawmap:
                                #    for number in line:
                                #        if not number.i
                                #        if number in mynumbers:
                                #                pass
                                #        else:
                                #                mynumbers.append(number)
                                    
                                #if len(mynumbers) > 0:
                                #    Flytext(text="sorting mynumbers....", move=pygame.math.Vector2(0,20))
                                #    #print(mychars)                
                                #    mynumbers.sort()
                                #    #print(mychars)
                                #    for n in mynumbers:
                                #        Viewer.menu["set water height"].append(n)
                                #print("map sucessfully added")
                                #print(self.rawmap)
                                
                                    
                        
            # ------delete everything on screen-------
            self.screen.blit(self.background, (0, 0))
            
            
         
            # -------------- UPDATE all sprites -------             
            self.flytextgroup.update(seconds)

            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)

            # --- paint menu ----
            # ---- name of active menu and history ---
            write(self.screen, text="you are here:", x=200, y=50, color=(0,255,255))
            
            t = "main"
            for nr, i in enumerate(Viewer.history[1:]):
                #if nr > 0:
                t+=(" > ")
                t+=(i)
                #
            
            #t+=Viewer.name
            write(self.screen, text=t, x=200,y=70,color=(0,255,255))
            # --- menu items ---
            menu = Viewer.menu[Viewer.name]
            for y, item in enumerate(menu):
                write(self.screen, text=item, x=200, y=100+y*20, color=(255,255,255))
            # --- cursor ---
            write(self.screen, text="-->", x=100, y=100+ Viewer.cursor * 20, color=(255,255,255))
                        
                
            # -------- next frame -------------
            pygame.display.flip()
        #----------------------------------------------------- 
    
    def make_worldmap(self):
            print("generating map.....{} x {}".format(len(self.rawmap[1]), len(self.rawmap )))
            self.screen.fill((255,128,128))
            # BUG! size limit 16384 for surface width / height ? 
            #self.world = pygame.surface.Surface((len(self.rawmap[0])*self.tilesize, len(self.rawmap)*self.tilesize))
            self.world = pygame.surface.Surface((self.width, self.height))
            dy = self.world_offset_y / self.tilesize
            dx = self.world_offset_x / self.tilesize
            for y, line in enumerate(self.rawmap):
                for x, number in enumerate(line):
                    if x < -dx or y < -dy:
                        continue
                    if x > self.width / self.tilesize - dx or y > self.height / self.tilesize - dy:
                        continue
                    if number == "\n":
                        continue
                    number = int(number)
                    if number <= self.waterheight:
                        color = (0,0,255) # blue
                    color = get_height_color(number)
                    #print("x,dx, y,dy", x, dx, y, dy)
                    #print("rect start x, rect start y", (x+dx)*self.tilesize, (y+dy) * self.tilesize) 
                    pygame.draw.rect(self.world, color, ((x+dx) * self.tilesize, (y+dy) * self.tilesize, self.tilesize, self.tilesize))
                    if self.grid:
                        pygame.draw.rect(self.world, (255,255,255), ((x+dx) * self.tilesize, (y+dy) * self.tilesize, self.tilesize, self.tilesize), 1)
                    
    
    
    def display_help(self):
        Flytext(text="scroll map with cursor keys", pos = pygame.math.Vector2(400, -100))
        Flytext(text="zoom map with mouse wheel or with + and - key", pos = pygame.math.Vector2(400,-150))
        Flytext(text="set water level with PgUp key and PgDown key",  pos = pygame.math.Vector2(400,-200))
        Flytext(text="toogle grid with key g", pos = pygame.math.Vector2(400,-250))
    
    
    def get_z(self, xpos, ypos):
         # --- tile coursor -----
         x = int(xpos / self.tilesize)
         y = int(ypos / self.tilesize)
         try:
             z = int(self.rawmap[-y][x])
         except:
             return -1
         return z
    
    def worldzoom(self, delta):
        """incrase (delta=1) or decrease (delta=-1) worldzoom"""
        if delta not in [1,0,-1]:
            raise ValueError("delta of worldzoom must be 1 or -1 or 0")
        if self.world_zoom + delta > 4:
            return # out of range
        if self.world_zoom + delta < -3:
            return # out of range
        self.world_zoom += delta
        if delta == 1:
            factor = 2
        elif delta == -1:
            factor = 0.5
        elif delta == 0:
            factor = 1
        Viewer.tilesize *= factor
        for o in self.worldgroup:
            o.pos *= factor
            o.move *= factor
            o.zoom = self.world_zoom
        self.make_worldmap() 
        
        
        
    def run(self):
        """The mainloop"""
        
        running = True
        self.menu_run()
        
        pygame.mouse.set_visible(True)
        oldleft, oldmiddle, oldright  = False, False, False
        # --------- blitting rawmap to world ------------
        if self.rawmap != []:
            self.make_worldmap()
        
        x, y, h = "?","?","?"
        self.worldzoom(0)
        
        self.create_sprites()
        
        while running:
          
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            text = "press h for help. FPS: {:8.3} ".format(self.clock.get_fps())
            text += "Worldzoom: {}    world_offset_x: {}     world_offset_y: {}".format(self.world_zoom, self.world_offset_x, self.world_offset_y)
            text += "tile value (x:{} y:{}): {}".format(x,y,h) 
            pygame.display.set_caption(text)
            
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # ----- mouse wheel -----
                elif event.type == pygame.MOUSEBUTTONDOWN:
                     if event.button == 4:
                         #Viewer.tilesize += 1
                         #self.make_worldmap()
                         self.worldzoom(1)
                     elif event.button == 5:
                         #Viewer.tilesize -= 1
                         #self.make_worldmap()
                         self.worldzoom(-1)
                         
                         
                
                # ------- pressed and released key ------
                
                
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_c:
                        # ---spawns a catapult ---
                        Catapult(selected=True, pos = mouseVector())
                    #if event.key == pygame.K_RIGHT:
                    #    self.b1.set_angle(self.b1.angle + 5)
                    #    self.c1.set_angle(self.c1.angle + 5)
                    #if event.key == pygame.K_s:
                    #    self.b1.selected = not self.b1.selected
                    #    self.c1.selected = not self.c1.selected 
                    if event.key == pygame.K_SPACE:
                        p = pygame.math.Vector2(self.c1.pos.x, self.c1.pos.y)
                        m = pygame.math.Vector2(200,0)
                        m.rotate_ip(self.c1.angle)
                        Cannonball(pos=p, move=m, bossnumber= self.c1.number)
                    if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                        self.worldzoom(1)
                    if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        self.worldzoom(-1)
                    if event.key == pygame.K_h:
                        self.display_help()
                    if event.key == pygame.K_g:
                        self.grid = not self.grid
                        Flytext(x=400,y=400, text="Grid is now: {}".format(self.grid))
                        self.make_worldmap()
                    # --------------- map scrolling ------------
                    if event.key == pygame.K_UP:
                        self.world_offset_y += self.tilesize
                        self.make_worldmap()
                        #for o in self.worldgroup:
                            #o.worldpos.y += self.tilesize
                            #o.pos.y -= self.tilesize
                    if event.key == pygame.K_DOWN: 
                        self.world_offset_y += -self.tilesize
                        self.make_worldmap()
                        #for o in self.worldgroup:
                            #o.worldpos.y -= self.tilesize
                            #o.pos.y += self.tilesize
                    if event.key == pygame.K_LEFT:
                        self.world_offset_x += self.tilesize
                        self.make_worldmap()
                        #for o in self.worldgroup:
                            #o.worldpos.x += self.tilesize
                            #o.pos.x += self.tilesize
                            #print(o.pos)
                    if event.key == pygame.K_RIGHT: 
                        self.world_offset_x += -self.tilesize
                        self.make_worldmap()
                        #for o in self.worldgroup:
                            #o.worldpos.x -= self.tilesize
                            #o.pos.x -= self.tilesize
                    # ----------- water raising / lowering ------
                    if event.key == pygame.K_PAGEUP:
                        self.waterheight += 5
                        self.waterheight = min(255, self.waterheight)
                        self.make_worldmap()
                        
                    if event.key == pygame.K_PAGEDOWN:
                        self.waterheight -= 5
                        self.waterheight = max(0, self.waterheight)
                        self.make_worldmap()
                    
            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            
          
            # ------- movement keys for player1 -------
            
            #if pressed_keys[pygame.K_l]:
            #            self.player2.turn_right()
            
            # ------ mouse handler ------
            left,middle,right = pygame.mouse.get_pressed()
            oldleft, oldmiddle, oldright = left, middle, right

           
            # ------ joystick handler -------
            #for number, j in enumerate(self.joysticks):
            #    if number == 0:
            #        player = self.player1
            #    elif number ==1:
            #        player = self.player2
            #    else:
            #        continue 
             #   x = j.get_axis(0)
             #   y = j.get_axis(1)
                #if y > 0.5:
                #    player.move_backward()
                #if y < -0.5:
                #    player.move_forward()
                #if x > 0.5:
                #    player.turn_right()
                #if x < -0.5:
                #    player.turn_left()
                
              #  buttons = j.get_numbuttons()
              #  for b in range(buttons):
               #        pushed = j.get_button( b )
                #       if b == 0 and pushed:
                #           player.fire()
                #       if b == 4 and pushed:
                #           player.strafe_left()
                #       if b == 5 and pushed:
                #           player.strafe_right()                
                
              
            # =========== delete everything on screen ==============
            self.screen.fill((0,0,0))
            self.screen.blit(self.world, (0,0 ))
            
            # --- tile coursor -----
            x,y = pygame.mouse.get_pos()
            x = int(x / self.tilesize)
            y = int(y / self.tilesize)
            try:
                h = self.rawmap[y][x]
            except:
                x, y = 0, 0
            VectorSprite.numbers[0].pos.x = x * self.tilesize + self.tilesize // 2
            VectorSprite.numbers[0].pos.y = -y * self.tilesize - self.tilesize // 2
            
            
            
            
            
            #self.screen.blit(self.radarmap, (0,0))
            # ---- showing currently visible world map borders in radarmap -----
            radar = self.radarmap.copy()
            #print("ox, oy, ox+width/tileset, oy+height/tileset", self.world_offset_x, self.world_offset_y , self.world_offset_x + int(Viewer.width / self.tilesize), self.world_offset_y + int(Viewer.height / self.tilesize))
            pygame.draw.rect(radar, (80,255,80),  (-self.world_offset_x//self.tilesize, -self.world_offset_y//self.tilesize , int(Viewer.width / self.tilesize), int(Viewer.height / self.tilesize)),1)
            self.screen.blit(radar, (Viewer.width-radar.get_width(),0))
            
            ##self.paint_world()
                       
            # write text below sprites
            write(self.screen,  text="water: {}".format( self.waterheight ), x=Viewer.width-400, y=10, color=(100,0,200))
            
            # ----- collision detection between player and PowerUp---
            #for p in self.playergroup:
            #    crashgroup=pygame.sprite.spritecollide(p,
            #               self.powerupgroup, False, 
            #               pygame.sprite.collide_mask)
            #    for o in crashgroup:
            #            Explosion(o.pos, red=128, green=0, blue=128)
            #            o.kill()
            
            
            
                   
            # ================ UPDATE all sprites =====================
            self.allgroup.update(seconds)
            for s in self.worldgroup:
                s.worldrect(self.world_offset_x, self.world_offset_y, self.worldzoom)
                
            
            # --- is a javelin (from bulletgroup) flown into a mountain ? -----
            for bu in self.bulletgroup:
                try:   # somtimes error that z can't be found or is a "\n" char instead value
                    z = int(self.get_z(bu.pos.x, bu.pos.y))
                except:
                    continue 
                if z > bu.start_z:
                    # bullet is inside a mountain
                    Explosion(posvector=bu.pos)
                    bu.kill() 
                    # Explosion?
                    

            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)

            
           
                
            # -------- next frame -------------
            pygame.display.flip()
        #-----------------------------------------------------
        pygame.mouse.set_visible(True)    
        pygame.quit()

if __name__ == '__main__':
    Viewer(1430,800).run()
