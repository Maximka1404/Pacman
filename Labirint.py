from pygame import*

class GameSprite(sprite.Sprite):
    def __init__ (self,picture,w,h,x,y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(picture),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__ (self,picture,w,h,x,y,x_speed,y_speed):
        GameSprite.__init__(self,picture,w,h,x,y)
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        if player.rect.x <= win_w - 80 and player.x_speed > 0 or player.rect.x >= 0 and player.x_speed < 0:
            self.rect.x += self.x_speed

        platforms_touched = sprite.spritecollide(self, barries, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right,
                                        p.rect.left)
        elif self.x_speed < 0: 
            for p in platforms_touched:
                self.rect.left = max(self.rect.left,
                                        p.rect.right)
        if player.rect.y <= win_h - 80 and player.y_speed > 0 or player.rect.y >= 0 and player.y_speed < 0:
            self.rect.y += self.y_speed

        platforms_touched = sprite.spritecollide(self, barries, False)
        if self.y_speed > 0: 
            for p in platforms_touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: 
            for p in platforms_touched:
                self.y_speed = 0 
                self.rect.top = max(self.rect.top, p.rect.bottom) 
    def fire(self):
        bullet = Bullet('bullet.png', 15, 20, self.rect.right, self.rect.centery, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    x_point = 'left'
    def __init__ (self,picture,w,h,x,y,x_speed):
        GameSprite.__init__(self,picture,w,h,x,y)
        self.x_speed = x_speed
    def update(self):
        if self.rect.x <= 420:
            self.x_point = 'right'
        if self.rect.x >= 615:
            self.x_point = 'left'
        if self.x_point == 'left':
            self.rect.x -= self.x_speed
        else:
            self.rect.x += self.x_speed

class Bullet(GameSprite):
    def __init__ (self,picture,w,h,x,y,x_speed):
        GameSprite.__init__(self,picture,w,h,x,y)
        self.x_speed = x_speed
    def update(self):
        self.rect.x += self.x_speed
        if self.rect.x >= win_w + 10:
            self.kill()
    


win_w = 700
win_h = 500

player = Player('pacman.png', 60, 60, 100, 200, 0, 0) #экземпляр класса
monstr = Enemy('robot.png',80,80,620,150,5)
flag = GameSprite('flag.png',60,60,600,400)

w1 = GameSprite('barries.png', 175, 30, 260, 65)#создание 1 стены  w,h,x,y
w2 = GameSprite('barries.png',30, 126, 100, 375)#создание 2 стены

window = display.set_mode((win_w, win_h))
display.set_caption('Моя первая игра')
pic = transform.scale(image.load('phon.png'),(win_w, win_h))
finish = False
run = True

barries = sprite.Group()
barries.add(w1)
barries.add(w2)

bullets = sprite.Group()

monstres = sprite.Group()
monstres.add(monstr)

while run:
    time.delay(50)
    for i in event.get():
        if i.type == QUIT:
            run = False
        elif i.type == KEYDOWN:
            if i.key == K_w:
                player.y_speed = -5
            elif i.key == K_s:
                player.y_speed = 5
            elif i.key == K_d:
                player.x_speed = 5
            elif i.key == K_a:
                player.x_speed = -5
            elif i.key == K_SPACE:
                player.fire()
        elif i.type == KEYUP:
            if i.key == K_w:
                player.y_speed = 0
            elif i.key == K_s:
                player.y_speed = 0
            elif i.key == K_d:
                player.x_speed = 0
            elif i.key == K_a:
                player.x_speed = 0
    if finish != True:
        window.fill((0,0,0))
        player.reset()
        player.update()
        flag.reset()
        bullets.draw(window)
        bullets.update()
        barries.draw(window)
        sprite.groupcollide(bullets,monstres,True,True)
        monstres.update()
        monstres.draw(window)
        sprite.groupcollide(bullets,barries,True,False)

        if sprite.collide_rect(player,monstr):
            finish = True
            point_1 = transform.scale(image.load('Game over.jpg'),(win_w, win_h))
            window.blit(point_1,(0,0))
        if sprite.collide_rect(player,flag):
            finish = True
            point_2 = transform.scale(image.load('Great.jpg'),(win_w, win_h))
            window.blit(point_2,(0,0))
        
    display.update()
