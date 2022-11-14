
import pygame
import random
import os
from int_page import *


# 常數
WIDTH = 500
HEIGHT = 800
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CADMIUM_YELLOW = (253, 218, 13)
RED = (255, 0, 0)
DROP_RATE = 100

# 初始化內容
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(20)
all_sprites = pygame.sprite.Group()  # 所有物件集合
all_player_bullets = pygame.sprite.Group()  # 所有玩家子彈集合
all_enemies = pygame.sprite.Group()  # 所有敵方物件集合
all_enemies_bullets = pygame.sprite.Group()  # 所有敵方子彈集合

win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("遊戲名稱")

running = True
show_init = True


# 圖片載入
background_img = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "background.png")).convert(), (WIDTH, HEIGHT))
player_img = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "player.png")).convert(), (50, 38))
life_img = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "life.png")).convert(), (30, 30))
life_img.set_colorkey((0, 0, 0))
bullet1_img = pygame.image.load(
    os.path.join("img", "bullet1.png")).convert()

# 音樂載入
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.8)
laser_sound = pygame.mixer.Sound(os.path.join("sound", "laser.ogg"))
enemy1_sound = pygame.mixer.Sound(os.path.join("sound", "enemy1.ogg"))
powerup_sound = pygame.mixer.Sound(os.path.join("sound", "powerup.ogg"))
buffdrop_sound = pygame.mixer.Sound(os.path.join("sound", "buffdrop.ogg"))
enemydestruction_sound = pygame.mixer.Sound(
    os.path.join("sound", "enemydestruction.ogg"))
playerexplode_sound = pygame.mixer.Sound(
    os.path.join("sound", "playerexplode.ogg"))
magicshield_sound = pygame.mixer.Sound(
    os.path.join("sound", "magicshield.ogg"))
playershoot_sound = pygame.mixer.Sound(
    os.path.join("sound", "playershoot.wav"))
spikeball_bomb_sound = pygame.mixer.Sound(
    os.path.join("sound", "spikeball_bomb.ogg"))
tracebullet_sound = pygame.mixer.Sound(
    os.path.join("sound", "tracebullet.wav"))
getshot_sound = []
for i in range(5):
    getshot_sound.append(pygame.mixer.Sound(os.path.join(
        "sound", f"getshot{i}.ogg")))

# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓測試用(你所要載入的所有東西(圖片檔等)，或是其他你想要增加的全域變數)↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
all_enemies_lasers = pygame.sprite.Group()  # 所有敵方雷射集合
all_awards = pygame.sprite.Group()  # 所有獎勵集合
all_blackholes = pygame.sprite.Group()  # 所有黑洞集合

ufo_img = shield_img = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "ufo1.png")).convert(), (60, 40))
ufo_img.set_colorkey(BLACK)

enemy1_img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
    os.path.join("img", "enemy1.png")).convert(), (30, 30)), 180)
enemy1_img.set_colorkey(BLACK)

shield_img = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "shield.png")).convert(), (60, 60))
shield_img.set_colorkey(BLACK)

shield2_img = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "shield2.png")).convert(), (30, 30))
shield2_img.set_colorkey(BLACK)

magicdefense_img = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "magicdefense1.png")).convert(), (100, 100))
magicdefense_img.set_colorkey(BLACK)

cactus_img = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "cactus.png")).convert(), (60, 90))
cactus_img.set_colorkey(BLACK)

spikeball_img = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "spikeball.png")).convert(), (55, 55))
spikeball_img.set_colorkey(BLACK)

spikes_img = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "spikes.png")).convert(), (20, 20))
spikes_img.set_colorkey(BLACK)
spikes_img_array = []
for i in range(8):
    spikes_img_array.append(pygame.transform.rotate(spikes_img, -45*i))

gun_img = []
for i in range(8):
    img = pygame.image.load(os.path.join(
        "img", f"gun{i}.png")).convert()
    img.set_colorkey(BLACK)
    gun_img.append(pygame.transform.scale(img, (20, 30)))

clock_img = []
for i in range(12):
    img = pygame.image.load(os.path.join(
        "img", f"clock{i}.png")).convert()
    img.set_colorkey(BLACK)
    clock_img.append(pygame.transform.scale(img, (25, 25)))

life_img_array = []
for i in range(8):
    img = pygame.image.load(os.path.join(
        "img", f"life{i}.png")).convert()
    img.set_colorkey(BLACK)
    life_img_array.append(pygame.transform.scale(img, (25, 25)))

magicshield_img_array = []
for i in range(8):
    img = pygame.image.load(os.path.join(
        "img", f"shield{i}.png")).convert()
    img.set_colorkey(BLACK)
    magicshield_img_array.append(pygame.transform.scale(img, (25, 25)))

explosion_img = []
for i in range(9):
    img = pygame.image.load(os.path.join(
        "img", f"expl{i}.png")).convert()
    img.set_colorkey(BLACK)
    explosion_img.append(pygame.transform.scale(img, (60, 60)))

player_explosion_img = []
for i in range(9):
    img = pygame.image.load(os.path.join(
        "img", f"player_expl{i}.png")).convert()
    img.set_colorkey(BLACK)
    player_explosion_img.append(pygame.transform.scale(img, (80, 80)))

satellite_img = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "satellite.png")).convert(), (60, 60))

blackhole_img = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "blackhole1.png")).convert(), (150, 150))
blackhole_img.set_colorkey(BLACK)

laser_img = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "raser.png")).convert(), (600, 30))
laser_img.set_colorkey(BLACK)

trace_bullet_img = []
for i in range(1, 17):
    img = pygame.image.load(os.path.join(
        "img", f"enemy_tracebullet_{i}.png")).convert()
    img.set_colorkey(BLACK)
    trace_bullet_img.append(pygame.transform.scale(img, (30, 30)))

state = [1, 1, 1, 1]
stage = 0

awards = ["gun", "clock", "life", "magicshield"]
awards_img = [gun_img, clock_img, life_img_array, magicshield_img_array]

# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑測試用(你所要載入的所有東西(圖片檔等)，或是其他你想要增加的全域變數)↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


# 音樂載入

# 遊戲中的界面(血量、道具等)


def draw_game_interface(win, player):
    draw_text(win, "血量："+str(player.hp), 25, 70, 30, WHITE)
    for i in range(player.life):
        win.blit(life_img, (WIDTH-50-50*i, 20))
    for i in range(player.num_magicdefense):
        win.blit(shield2_img, (WIDTH-50-50*i, HEIGHT-50))


# Player物件


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT-50)
        self.shield = Shield(shield_img, - 300, - 300)
        self.magicdefense = Magicdefense(magicdefense_img, -300, -300)
        self.magicdefense_lasttime = 10000
        self.magicdefense_clock = -self.magicdefense_lasttime
        self.bullet_clock = pygame.time.get_ticks()
        self.bullet_num = 1
        self.shoot_time = 600
        self.hidden = False
        self.hidden_time = 0
        self.invincible = False
        self.is_magic_defense = False
        self.laser_shot_sound_clock = 0

        # 玩家相關數據
        self.speedx = 7
        self.speedy = 7
        self.life = 3
        self.hp = 1000
        self.num_magicdefense = 3

        # 自動加入群組
        all_sprites.add(self)

    def shoot(self):
        if self.bullet_num == 1:
            Bullet(self.rect.centerx, self.rect.top,
                   bullet1_img, 0, -10, 10, self)
        elif self.bullet_num == 2:
            Bullet(self.rect.left, self.rect.top,
                   bullet1_img, 0, -10, 10, self)
            Bullet(self.rect.right, self.rect.top,
                   bullet1_img, 0, -10, 10, self)
        elif self.bullet_num == 3:
            Bullet(self.rect.left, self.rect.top,
                   bullet1_img, -3, -8, 10, self)
            Bullet(self.rect.centerx, self.rect.top,
                   bullet1_img, 0, -10, 10, self)
            Bullet(self.rect.right, self.rect.top,
                   bullet1_img, 3, -8, 10, self)
        elif self.bullet_num == 4:
            Bullet(self.rect.left, self.rect.top,
                   bullet1_img, 0, -10, 10, self)
            Bullet(self.rect.right, self.rect.top,
                   bullet1_img, 0, -10, 10, self)
            Bullet(self.rect.left-8, self.rect.top,
                   bullet1_img, -3, -8, 10, self)
            Bullet(self.rect.right+8, self.rect.top,
                   bullet1_img, 3, -8, 10, self)
        elif self.bullet_num == 5:
            Bullet(self.rect.left, self.rect.top,
                   bullet1_img, -3, -8, 10, self)
            Bullet(self.rect.centerx, self.rect.top,
                   bullet1_img, 0, -10, 10, self)
            Bullet(self.rect.right, self.rect.top,
                   bullet1_img, 3, -8, 10, self)
            Bullet(self.rect.left-8, self.rect.top,
                   bullet1_img, -6, -6, 10, self)
            Bullet(self.rect.right+8, self.rect.top,
                   bullet1_img, 6, -6, 10, self)

        playershoot_sound.play()

    # 玩家碰到獎賞時，要幹嘛
    def player_collide_with_award(self, award):
        if award.type == "gun" and self.bullet_num < 5:
            self.bullet_num += 1
        elif award.type == "clock" and self.shoot_time > 150:
            self.shoot_time -= 150
        elif award.type == "life" and self.life < 5:
            self.life += 1
        elif award.type == "life" and self.life == 5:
            self.hp = 1000
        elif award.type == "magicshield" and self.num_magicdefense < 3:
            self.num_magicdefense += 1
    # 玩家碰到敵方戰艦時，要被扣血

    def player_collide_with_enemy(self, enemy):
        if not (self.invincible or self.is_magic_defense):
            now = pygame.time.get_ticks()
            if now-enemy.time_get_hit > 500:
                self.hp -= 50
                enemy.time_get_hit = now

    # 玩家碰到敵方子彈射中時，要被扣血

    def player_collide_with_enemy_bullets(self, bullet):
        if not (self.invincible or self.is_magic_defense):
            self.hp -= bullet.attack
            num = random.randint(0, 1)
            getshot_sound[num].play()

    # 玩家碰到雷射，要被扣血
    def player_collide_with_lasers(self):
        if not (self.invincible or self.is_magic_defense):
            self.hp -= 2
            now = pygame.time.get_ticks()
            if now - self.laser_shot_sound_clock > 200:
                getshot_sound[4].play()
                self.laser_shot_sound_clock = now

    def hide(self):
        self.hidden = True
        self.hidden_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)
        self.invincible = True

    # 使用魔法防護罩
    def useMagicDefense(self):
        if self.num_magicdefense > 0:
            self.num_magicdefense -= 1
            self.is_magic_defense = True
            self.magicdefense.rect.center = (
                self.rect.centerx, self.rect.centery - 5)
            magicshield_sound.play()
            self.magicdefense_clock = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()

        if self.hidden:
            if now - self.hidden_time > 1000:
                self.hidden = False
                self.rect.center = (WIDTH/2, HEIGHT-50)
        else:
            # WASD操控
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_d]:
                self.rect.x += self.speedx
            if key_pressed[pygame.K_a]:
                self.rect.x -= self.speedx
            if key_pressed[pygame.K_w]:
                self.rect.y -= self.speedy
            if key_pressed[pygame.K_s]:
                self.rect.y += self.speedy
            if key_pressed[pygame.K_z]:
                if now - self.magicdefense_clock > self.magicdefense_lasttime:
                    self.useMagicDefense()

            # 判斷是否出界
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT

            # 判斷空白鍵射擊(有限定兩個子彈間的秒數)
            if key_pressed[pygame.K_SPACE]:
                now = pygame.time.get_ticks()
                if now - self.bullet_clock >= self.shoot_time:
                    self.shoot()
                    self.bullet_clock = now

        # 玩家是否剛復活無敵
        if self.invincible:
            if now - self.hidden_time > 3000:
                self.invincible = False
                self.shield.rect.center = (-300, -300)
            else:
                self.shield.rect.center = (
                    self.rect.centerx, self.rect.centery - 5)

        if self.is_magic_defense:
            self.magicdefense.rect.center = (
                self.rect.centerx, self.rect.centery - 5)

        # 判斷玩家魔法護盾秒數
        if self.is_magic_defense:
            if now - self.magicdefense_clock > self.magicdefense_lasttime:
                self.is_magic_defense = False
                self.magicdefense.rect.center = (-300, -300)

        # 判斷玩家是否已經死亡
        if self.hp <= 0 and self.life >= 0:
            self.hp = 1000
            self.life -= 1
            Animation(player_explosion_img,
                      self.rect.centerx, self.rect.centery)
            playerexplode_sound.play()
            getshot_sound[2].play()
            self.hide()

        if self.life < 0:
            playerexplode_sound.play()
            getshot_sound[3].play()
            global show_init, stage, state
            state = [1, 1, 1, 1]
            stage = 0
            show_init = True


# 敵方單位物件


class Enemy(pygame.sprite.Sprite):
    def __init__(self, img, hp, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.time_get_hit = pygame.time.get_ticks()
        self.bullet_clock = pygame.time.get_ticks()
        # 敵方相關數據
        self.hp = hp

        # 自動加入所屬群組
        all_sprites.add(self)
        all_enemies.add(self)

    # 被子彈射到時，被扣血的函式(不同的子彈有不同的攻擊力)
    def get_hit(self, bullet):
        self.hp -= bullet.attack


# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓測試用(繼承Enemy之後，寫出你的敵人class)↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
class Shield(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        all_sprites.add(self)


class Magicdefense(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.ori_img = img
        self.img_angle = 0
        self.frame_clock = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        all_sprites.add(self)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.frame_clock > 50:
            self.img_angle -= 2
            center = self.rect.center
            self.image = pygame.transform.rotate(self.ori_img, self.img_angle)
            self.rect = self.image.get_rect()
            self.rect.center = center


# 基本飛機
class BasicEnemy(Enemy):
    def __init__(self, img, hp, x, y, x_move_range, to_y):
        super().__init__(img, hp, x, y)
        self.ori_x = x
        self.to_y = to_y
        self.speedx = 1
        self.x_move_range = x_move_range
        self.bullet_img = pygame.transform.scale(pygame.image.load(
            os.path.join("img", "enemy_bullet1.png")).convert(), (15, 20))

        enemy1_sound.play()

    def shoot(self):
        now = pygame.time.get_ticks()
        if (now - self.bullet_clock > 400):
            self.bullet_clock = now
            Bullet(self.rect.centerx, self.rect.bottom+10,
                   self.bullet_img, 0, 10, 10, self)
            Bullet(self.rect.centerx-10, self.rect.bottom+10,
                   self.bullet_img, -6, 8, 10, self)
            Bullet(self.rect.centerx+10, self.rect.bottom+10,
                   self.bullet_img, 6, 8, 10, self)

    def update(self):
        if self.rect.y < self.to_y:
            self.rect.y += 2
        elif self.rect.y > self.to_y:
            self.rect.y = self.to_y
        elif self.rect.y == self.to_y:
            if self.x_move_range != 0:
                if self.rect.x < (self.ori_x-self.x_move_range):
                    self.speedx = 1
                if self.rect.x > (self.ori_x+self.x_move_range):
                    self.speedx = -1

                self.rect.x += self.speedx
            self.shoot()

        if self.hp <= 0:
            Animation(explosion_img, self.rect.centerx, self.rect.centery)
            if random.randint(1, 100) <= DROP_RATE:
                index = random.randint(0, len(awards)-1)
                Award(awards_img[index], self.rect.centerx,
                      self.rect.centery, awards[index])
                buffdrop_sound.play()
            enemydestruction_sound.play()
            self.kill()

# 仙人掌


class BasicEnemy2(Enemy):
    def __init__(self, img, hp, x, y, to_y, move_range):
        super().__init__(img, hp, x, y)
        self.ori_x = x
        self.speedx = 1
        self.to_y = to_y
        self.move_range = move_range

    def shoot(self):
        now = pygame.time.get_ticks()
        if (now - self.bullet_clock > 700):
            self.bullet_clock = now
            SpikesBall(self.rect.centerx, self.rect.bottom +
                       15, spikeball_img, 0, 3, 50, self)

    def update(self):
        if self.rect.y < self.to_y:
            self.rect.y += 3
        elif self.rect.y > self.to_y:
            self.rect.y = self.to_y
        elif self.rect.y == self.to_y:

            if self.rect.x < (self.ori_x-self.move_range):
                self.speedx = 1
            if self.rect.x > (self.ori_x+self.move_range):
                self.speedx = -1

            self.rect.x += self.speedx
            self.shoot()

        if self.hp <= 0:
            Animation(explosion_img, self.rect.centerx, self.rect.centery)
            if random.randint(1, 100) <= DROP_RATE:
                index = random.randint(0, len(awards)-1)
                Award(awards_img[index], self.rect.centerx,
                      self.rect.centery, awards[index])
                buffdrop_sound.play()
            enemydestruction_sound.play()
            self.kill()

# 幽浮


class BasicEnemy3(Enemy):
    def __init__(self, img, hp, x, y, player, to_y):
        super().__init__(img, hp, x, y)
        self.to_y = to_y
        self.ori_x = x
        self.player = player
        self.isSetting = False

        if 0 == random.randint(0, 1):
            self.speedx = -1
        else:
            self.speedx = 1
        if 0 == random.randint(0, 1):
            self.speedy = -1
        else:
            self.speedy = 1

    def shoot(self):
        now = pygame.time.get_ticks()
        if (now - self.bullet_clock > 1000):
            self.bullet_clock = now
            TraceBullet(self.rect.centerx, self.rect.bottom+10,
                        trace_bullet_img, 10, self, self.player)
            tracebullet_sound.play()

    def update(self):
        if not self.isSetting:
            if self.rect.y < self.to_y:
                self.rect.y += 3
            elif self.rect.y >= self.to_y:
                self.rect.y = self.to_y
                self.isSetting = True
        else:
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.x < (self.ori_x-120):
                self.speedx = 1
            if self.rect.x > (self.ori_x+120):
                self.speedx = -1
            if self.rect.y < (self.to_y-50):
                self.speedy = 1
            if self.rect.y > (self.to_y+50):
                self.speedy = -1

        self.shoot()

        if self.hp <= 0:
            Animation(explosion_img, self.rect.centerx, self.rect.centery)
            if random.randint(1, 100) <= DROP_RATE:
                index = random.randint(0, len(awards)-1)
                Award(awards_img[index], self.rect.centerx,
                      self.rect.centery, awards[index])
                buffdrop_sound.play()
            enemydestruction_sound.play()
            self.kill()


class Satellite(Enemy):
    def __init__(self, img, hp, x, y):  # loc number 拿掉
        super().__init__(img, hp, x, y)
        self.ori_image = img
        self.move_to_x = random.randrange(40, WIDTH-40)
        self.move_to_y = random.randrange(50, HEIGHT-60)
        self.direction = random.randrange(1, 5)  # 1~4 上右下左
        self.rotate_clock = pygame.time.get_ticks()+4000
        self.move_clock = pygame.time.get_ticks()+1000
        self.laser = None
        # print(self.laser)
        if self.direction == 1:
            self.image = pygame.transform.rotate(self.ori_image, 270)
            self.rotate_now_angle = 270
            self.rotate_to_angle = self.rotate_now_angle + 90
        elif self.direction == 2:
            self.image = pygame.transform.rotate(self.ori_image, 180)
            self.rotate_now_angle = 180
            self.rotate_to_angle = self.rotate_now_angle + 90
        elif self.direction == 3:
            self.image = pygame.transform.rotate(self.ori_image, 90)
            self.rotate_now_angle = 90
            self.rotate_to_angle = self.rotate_now_angle + 90
        elif self.direction == 4:
            self.image = self.ori_image
            self.rotate_now_angle = 0
            self.rotate_to_angle = self.rotate_now_angle + 90

        # 相關參數
        self.speedx = 3
        self.speedy = 3
        # self.x1 = 50
        # self.x2 = 400
        # self.y1 = 100
        # self.y2 = 700

        # self.loc_num = loc_num
        # loc_num
        # 0 1 2
        # 3 4 5
        # 6 7 8
        # self.loc = [(self.x1, self.y1), ((self.x1+self.x2)//2, self.y1), (self.x2, self.y1), (self.x1, (self.y1+self.y2)//2), ((self.x1+self.x2) //
        #    2, (self.y1+self.y2)//2), (self.x2, (self.y1+self.y2)//2), (self.x1, self.y2), ((self.x1+self.x2)//2, self.y2), (self.x2, self.y2)]

    # def shoot(self):

    def update(self):
        # if self.rect.x > self.loc[self.loc_num][0]:
        #     self.rect.x -= self.speedx
        # if self.rect.x < self.loc[self.loc_num][0]:
        #     self.rect.x += self.speedx
        # if self.rect.y < self.loc[self.loc_num][1]:
        #     self.rect.y += self.speedy
        # if self.rect.y > self.loc[self.loc_num][1]:
        #     self.rect.y -= self.speedy

        if self.rect.x > self.move_to_x:
            self.rect.x -= self.speedx
        if self.rect.x < self.move_to_x:
            self.rect.x += self.speedx
        if self.rect.y < self.move_to_y:
            self.rect.y += self.speedy
        if self.rect.y > self.move_to_y:
            self.rect.y -= self.speedy

        # 五秒後隨機換位
        # now = pygame.time.get_ticks()
        # if now - self.move_clock > 5000:
        #     self.loc_num = random.randrange(9)
        #     self.move_clock = now

        # 五秒後隨機換位
        now = pygame.time.get_ticks()
        if now - self.move_clock > 6000:
            self.move_to_x = random.randrange(40, WIDTH-40)
            self.move_to_y = random.randrange(50, HEIGHT-60)
            self.need_rotate = True
            self.rotate_to_angle += 90
            self.move_clock = now
            self.rotate_clock = now + 3000

        if now - self.rotate_clock > 500 and self.rotate_to_angle > self.rotate_now_angle:
            self.rotate_now_angle += 2
            center = self.rect.center
            # print(center)
            self.image = pygame.transform.rotate(
                self.ori_image, self.rotate_now_angle % 360)
            self.rect = self.image.get_rect()
            self.rect.center = center
            if self.rotate_to_angle == self.rotate_now_angle:
                self.direction -= 1
                if self.direction == 0:
                    self.direction = 4
                self.laser = Laser(laser_img, self.rect.centerx,
                                   self.rect.centery, self.direction)
                laser_sound.play()
        # print(self.laser)

        # 血量小於0死亡
        if self.hp <= 0:
            Animation(explosion_img, self.rect.centerx, self.rect.centery)
            if random.randint(1, 100) <= DROP_RATE:
                index = random.randint(0, len(awards)-1)
                Award(awards_img[index], self.rect.centerx,
                      self.rect.centery, awards[index])
                buffdrop_sound.play()
            enemydestruction_sound.play()
            self.kill()
            if self.laser != None and self.laser.alive():
                self.laser.kill()


class TraceBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, img, attack, who, trace_who):
        pygame.sprite.Sprite.__init__(self)
        self.img_array = img
        self.image = img[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_clock = self.frame_clock = self.create_clock = pygame.time.get_ticks()
        self.frame = 0

        # 子彈相關數據
        self.speedx = 1
        self.speedy = 1
        self.attack = attack
        self.trace_who = trace_who

        # 自動加入所屬群組
        all_sprites.add(self)
        if isinstance(who, Player):
            all_player_bullets.add(self)
        if isinstance(who, Enemy):
            all_enemies_bullets.add(self)

    def update(self):
        now = pygame.time.get_ticks()

        # 跑動畫
        if now - self.frame_clock > 50:
            self.frame = (self.frame + 1) % len(self.img_array)
            # print(self.frame)
            center = self.rect.center
            self.image = trace_bullet_img[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center

            self.frame_clock = now

        # 速度計算
        if now-self.speed_clock > 80:
            if self.rect.x > self.trace_who.rect.x:
                if self.speedx >= -4:
                    self.speedx -= 1
            if self.rect.x < self.trace_who.rect.x:
                if self.speedx <= 4:
                    self.speedx += 1
            if self.rect.y < self.trace_who.rect.y:
                if self.speedy <= 4:
                    self.speedy += 1
            if self.rect.y > self.trace_who.rect.y:
                if self.speedy >= -4:
                    self.speedy -= 1

            self.speed_clock = now

        # 超過指定秒數消失
        if now-self.create_clock > 5000:
            self.kill()

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > HEIGHT:
            self.kill()
        if self.rect.left > WIDTH:
            self.kill()
        if self.rect.right < 0:
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, img, x, y, direction):  # direction 1~4:上右下左
        pygame.sprite.Sprite.__init__(self)
        self.disappear_clock = pygame.time.get_ticks()
        if direction == 1:
            self.image = pygame.transform.rotate(img, 90)
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
        elif direction == 2:
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.centery = y
        elif direction == 3:
            self.image = pygame.transform.rotate(img, 270)
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.top = y
        elif direction == 4:
            self.image = pygame.transform.rotate(img, 180)
            self.rect = self.image.get_rect()
            self.rect.right = x
            self.rect.centery = y

        all_sprites.add(self)
        all_enemies_lasers.add(self)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.disappear_clock > 1500:
            self.kill()


class SpikesBall(pygame.sprite.Sprite):
    def __init__(self, x, y, img, speedx, speedy, attack, who):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.ori_img = img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame_clock = 0
        self.angle = 0
        self.bomb_clock = pygame.time.get_ticks()
        self.bombtime = random.randint(800, 2300)
        self.who = who

        # 子彈相關數據
        self.speedx = speedx
        self.speedy = speedy
        self.attack = attack

        # 自動加入所屬群組
        all_sprites.add(self)
        all_enemies_bullets.add(self)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.frame_clock > 50:
            center = self.rect.center
            self.angle += 5
            self.image = pygame.transform.rotate(self.ori_img, self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.frame_clock = now

        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if now - self.bomb_clock > self.bombtime:
            Bullet(self.rect.centerx, self.rect.centery,
                   spikes_img_array[0], 0, -10, 10, self.who)
            Bullet(self.rect.centerx, self.rect.centery,
                   spikes_img_array[1], 10/(2**0.5), -10/(2**0.5), 10, self.who)
            Bullet(self.rect.centerx, self.rect.centery,
                   spikes_img_array[2], 10, 0, 10, self.who)
            Bullet(self.rect.centerx, self.rect.centery,
                   spikes_img_array[3], 10/(2**0.5), 10/(2**0.5), 10, self.who)
            Bullet(self.rect.centerx, self.rect.centery,
                   spikes_img_array[4], 0, 10, 10, self.who)
            Bullet(self.rect.centerx, self.rect.centery,
                   spikes_img_array[5], -10/(2**0.5), 10/(2**0.5), 10, self.who)
            Bullet(self.rect.centerx, self.rect.centery,
                   spikes_img_array[6], -10, 0, 10, self.who)
            Bullet(self.rect.centerx, self.rect.centery,
                   spikes_img_array[7], -10/(2**0.5), -10/(2**0.5), 10, self.who)
            spikeball_bomb_sound.play()
            self.kill()

        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > HEIGHT:
            self.kill()
        if self.rect.left > WIDTH:
            self.kill()
        if self.rect.right < 0:
            self.kill()


class Award(pygame.sprite.Sprite):
    def __init__(self, img, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.img_array = img
        self.image = img[0]
        self.frame = 0
        self.frame_clock = pygame.time.get_ticks()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # 加入所屬群組
        all_sprites.add(self)
        all_awards.add(self)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.frame_clock > 50:
            self.frame = (self.frame + 1) % len(self.img_array)
            center = self.rect.center
            self.image = self.img_array[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center

            self.frame_clock = now


class Animation(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img_array = img
        self.image = img[0]
        self.frame = 0
        self.frame_clock = pygame.time.get_ticks()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # 加入所屬群組
        all_sprites.add(self)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.frame_clock > 50:
            self.frame = (self.frame + 1)
            if self.frame == len(self.img_array):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.img_array[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.frame_clock = now


class Blackhole(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.image = blackhole_img
        self.ori_img = blackhole_img
        self.img_angle = 0
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(70, WIDTH-80),
                            random.randint(70, HEIGHT-80))
        self.frame_clock = self.exist_time = pygame.time.get_ticks()

        all_sprites.add(self)
        all_blackholes.add(self)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.frame_clock > 50:
            self.img_angle -= 2
            center = self.rect.center
            self.image = pygame.transform.rotate(self.ori_img, self.img_angle)
            self.rect = self.image.get_rect()
            self.rect.center = center
        if now - self.exist_time > 10000:
            Blackhole(self.player)
            self.kill()

        distance = ((self.player.rect.centerx - self.rect.centerx) **
                    2 + (self.player.rect.centery - self.rect.centery)**2)**0.5
        speed = 0
        if distance > 500:
            speed = 2
        elif distance > 400:
            speed = 3
        elif distance > 300:
            speed = 4
        elif distance > 200:
            speed = 5
        elif distance > 100:
            speed = 6
        else:
            speed = 7

        if distance != 0:
            # print(distance)
            if self.player.rect.centerx > self.rect.centerx:
                self.player.rect.centerx -= abs(
                    self.player.rect.centerx - self.rect.centerx)/distance*speed*0.8
                if self.player.rect.centerx < self.rect.centerx:
                    self.player.rect.centerx = self.rect.centerx
            elif self.player.rect.centerx < self.rect.centerx:
                self.player.rect.centerx += abs(
                    self.player.rect.centerx - self.rect.centerx)/distance*speed*0.8
                if self.player.rect.centerx > self.rect.centerx:
                    self.player.rect.centerx = self.rect.centerx

            if self.player.rect.centery > self.rect.centery:
                self.player.rect.centery -= abs(
                    self.player.rect.centery - self.rect.centery)/distance*speed*0.8
                if self.player.rect.centery < self.rect.centery:
                    self.player.rect.centery = self.rect.centery
            elif self.player.rect.centery < self.rect.centery:
                self.player.rect.centery += abs(
                    self.player.rect.centery - self.rect.centery)/distance*speed*0.8
                if self.player.rect.centery > self.rect.centery:
                    self.player.rect.centery = self.rect.centery
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑測試用(繼承Enemy之後，寫出你的敵人class)↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, img, speedx, speedy, attack, who):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        # 子彈相關數據
        self.speedx = speedx
        self.speedy = speedy
        self.attack = attack

        # 自動加入所屬群組
        all_sprites.add(self)
        if isinstance(who, Player):
            all_player_bullets.add(self)
        if isinstance(who, Enemy):
            all_enemies_bullets.add(self)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > HEIGHT:
            self.kill()
        if self.rect.left > WIDTH:
            self.kill()
        if self.rect.right < 0:
            self.kill()


def main():
    global running
    global show_init
    global stage
    global state
    count = 0
    test_clock = pygame.time.get_ticks()

    while running:

        # 畫面顯示
        win.fill(BLACK)
        win.blit(background_img, (0, 0))

        if show_init == True:
            running = draw_init(clock, win, background_img)
            show_init = False

            # 消除所有sprite，以防前一場遊戲剩下的sprite沒清乾淨
            for sprite in all_sprites:
                sprite.kill()

            # 確認遊戲開始後，初始化物件
            player = Player()

            # 開發測試區(只有一關)
            Satellite(satellite_img, 100, -50, -50)
            Satellite(satellite_img, 100, -50, -50)
            Satellite(satellite_img, 100, -50, -50)
            Satellite(satellite_img, 100, -50, -50)
            BasicEnemy3(ufo_img, 50, 300, -20, player, 250)
            BasicEnemy3(ufo_img, 50, 150, -20, player, 350)
            # Award(gun_img, 100, 100, "gun")
            # Award(clock_img, 200, 200, "clock")
            # Shield(shield_img, 200, 200)
            # Magicdefense(magicdefense_img, 200, 200)
            BasicEnemy2(cactus_img, 50, 220, -20, 50, 200)
            BasicEnemy(enemy1_img, 50, 150, -20, 0, 50)
            BasicEnemy(enemy1_img, 50, 350, -20, 0,80)
            Blackhole(player)

        # 測試動畫是否正常
        # now = pygame.time.get_ticks()
        # if now - test_clock > 50:
        #     count = (count+1)%16
        #     test_clock = now
        # win.blit(trace_bullet_img[count],(100,100))

        # 階段
        # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓測試用(建立你所寫的敵人物件)↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        # if stage == 0 and state[stage] == 1:
        #     BasicEnemy(enemy1_img, 50, 350, -20)
        #     BasicEnemy(enemy1_img, 50, 150, -20)
        #     state[stage] = 0
        # elif stage == 1 and state[stage] == 1:
        #     BasicEnemy2(cactus_img, 50, 220, -20, 50, 200)
        #     state[stage] = 0

        # elif stage == 2 and state[stage] == 1:
        #     BasicEnemy3(ufo_img, 50, 350, -20, player)
        #     BasicEnemy3(ufo_img, 50, 150, -20, player)
        #     state[stage] = 0

        # elif stage == 3 and state[stage] == 1:
        #     Satellite(satellite_img, 30, -50, -50)
        #     Satellite(satellite_img, 30, WIDTH//2, -50)
        #     Satellite(satellite_img, 30, WIDTH+50, -50)
        #     Satellite(satellite_img, 30, -50, HEIGHT//2)
        #     Satellite(satellite_img, 30, -50, HEIGHT//2)
        #     Satellite(satellite_img, 30, WIDTH+50, HEIGHT//2)
        #     Satellite(satellite_img, 30, -50, HEIGHT+50)
        #     Satellite(satellite_img, 30, WIDTH//2, HEIGHT+50)
        #     Satellite(satellite_img, 30, WIDTH+50, HEIGHT+50)
        #     state[stage] = 0

        # if len(all_enemies) == 0:
        #     stage += 1

        # 測試每階段敵人是否正常創造與刪除
        # print(len(all_sprites))

        # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑測試用(建立你所寫的敵人物件)↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

        clock.tick(FPS)

        # 輸入判定
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 演算各種碰撞判斷
        # 玩家與敵方戰艦相撞
        hits = pygame.sprite.spritecollide(
            player, all_enemies, False)  # hits 回傳所有玩家碰撞到的eneny list
        for hit in hits:
            player.player_collide_with_enemy(hit)

        # 敵方與玩家子彈碰撞
        hits = pygame.sprite.groupcollide(
            all_enemies, all_player_bullets, False, True)  # hits 回傳一個字典 被射到的enemy物件：[所有射中該enemy的子彈list]
        for hit in hits:
            length = len(hits[hit])
            for i in range(0, length):
                hit.get_hit(hits[hit][i])

        # 玩家與敵方子彈碰撞
        hits = pygame.sprite.spritecollide(
            player, all_enemies_bullets, True)  # hits 回傳所有玩家碰撞到的敵方子彈 list
        for hit in hits:
            player.player_collide_with_enemy_bullets(hit)

        # 玩家與雷射碰撞
        hits = pygame.sprite.spritecollide(
            player, all_enemies_lasers, False)  # hits 回傳所有玩家碰撞到的雷射 list
        for hit in hits:
            player.player_collide_with_lasers()

        # 玩家與獎勵碰撞
        hits = pygame.sprite.spritecollide(
            player, all_awards, True)  # hits 回傳所有玩家碰撞到的award list
        for hit in hits:
            powerup_sound.play()
            player.player_collide_with_award(hit)

        # 更新遊戲
        all_sprites.update()
        all_sprites.draw(win)
        draw_game_interface(win, player)

        # 測試是否所有sprite都有正常被加入與刪除
        # count_sprite=0
        # for i in all_sprites:
        #     count_sprite+=1
        # print(count_sprite)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
