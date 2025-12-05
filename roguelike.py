# type: ignore
# -*- coding: utf-8 -*-
import random
from pygame import Rect

WIDTH, HEIGHT, TILE = 900, 600, 32
TITLE = "PixelRunner"


STATE_MENU, STATE_GAME1, STATE_GAME2, STATE_GAME3, STATE_GAME4, STATE_GAME5, STATE_WIN = \
    "menu", "game1", "game2", "game3", "game4", "game5", "win"

game_state = STATE_MENU
music_on, sfx_on = True, True


RAW_MAP1 = [
    "############################",
    "#....##......#......##.....#",
    "#............#.............#",
    "#....#####...#...#####.....#",
    "#..........................#",
    "#.........#####............#",
    "#....##...........#####....#",
    "#..........................#",
    "############################",
]


RAW_MAP2 = [
    "############################",
    "#..........##..............#",
    "#....####.........######...#",
    "#............#.............#",
    "#....#####...#....#####....#",
    "#..........................#",
    "#....###.....#.............#",
    "#............#...#####.....#",
    "############################",
]


RAW_MAP3 = [
    "############################",
    "#.............#............#",
    "#....#####........#####....#",
    "#...........##.............#",
    "#...####....#......####....#",
    "#...........#..............#",
    "#....#####.......#####.....#",
    "#..##.........#............#",
    "#.............#............#",
    "############################",
]


RAW_MAP4 = [
    "############################",
    "#...........####...........#",
    "#..#####...........#####...#",
    "#...........##.............#",
    "#..####.....#.....####.....#",
    "#...........#..............#",
    "#..#####.........#####.....#",
    "#....##..........##........#",
    "#.............#............#",
    "############################",
]


RAW_MAP5 = [
    "#############################",
    "#....###.............###....#",
    "#........####..####.........#",
    "#..#####.............#####..#",
    "#...........................#",
    "#..#####...###..###...#####.#",
    "#..........#......#.........#",
    "#....###.............###....#",
    "#.............#.............#",
    "#############################",
]

def load_map(raw):
    ROWS, COLS = len(raw), len(raw[0])
    MAP_WIDTH, MAP_HEIGHT = COLS*TILE, ROWS*TILE
    OFFSET_X, OFFSET_Y = (WIDTH-MAP_WIDTH)//2, (HEIGHT-MAP_HEIGHT)//2
    return ROWS, COLS, OFFSET_X, OFFSET_Y


CURRENT_MAP = RAW_MAP1
ROWS, COLS, OFFSET_X, OFFSET_Y = load_map(CURRENT_MAP)
DOOR_CX, DOOR_CY = COLS-2, 4

def is_wall(c):
    x,y=c
    return CURRENT_MAP[y][x] == "#"

def to_px(cx,cy):
    return OFFSET_X+cx*TILE+TILE//2, OFFSET_Y+cy*TILE+TILE//2

def play_sound(name):
    if not sfx_on: return
    try:
        getattr(sounds, name).play()
    except:
        pass

class AnimatedSprite:
    def __init__(self, name, pos, frames):
        self.name,self.x,self.y=name,*pos
        self.state,self.dir,self.frame,self.t="idle","right",0,0
        self.frames=frames

    def update(self, dt):
        self.t+=dt
        f=self.frames[(self.state,self.dir)]
        if f>0 and self.t>=0.1:
            self.t=0
            self.frame=(self.frame+1)%f

    def draw(self):
        img=f"{self.name}_{self.state}_{self.dir}_{self.frame}"
        try:
            screen.blit(img,(self.x-16,self.y-16))
        except:
            screen.draw.filled_circle((self.x,self.y),14,"red")

    @property
    def rect(self):
        return Rect(self.x-16,self.y-16,32,32)


class Hero:
    def __init__(self):
        self.cx,self.cy=2,2
        self.x,self.y=to_px(self.cx,self.cy)
        self.sprite=AnimatedSprite("hero",(self.x,self.y),{
            ("idle","right"):2,("idle","left"):2,
            ("walk","right"):2,("walk","left"):2,
            ("hurt","left"):2,("hurt","right"):2
        })
        self.moving=False
        self.src=(0,0)
        self.dst=(0,0)
        self.t=0

    def want_move(self,dx,dy):
        if self.moving: return
        nx,ny=self.cx+dx,self.cy+dy
        if is_wall((nx,ny)): return
        self.cx,self.cy=nx,ny
        self.src,self.dst=(self.x,self.y),to_px(nx,ny)
        self.moving=True
        self.t=0
        self.sprite.state="walk"
        self.sprite.dir="left" if dx<0 else "right"
        play_sound("step")

    def update(self,dt):
        if self.moving:
            self.t+=dt/0.2
            if self.t>=1:
                self.t=1
                self.moving=False
                self.sprite.state="idle"
            self.x = self.src[0]*(1-self.t)+self.dst[0]*self.t
            self.y = self.src[1]*(1-self.t)+self.dst[1]*self.t
        self.sprite.x,self.sprite.y=self.x,self.y
        self.sprite.update(dt)

    def draw(self):
        self.sprite.draw()

    def reset(self):
        self.__init__()


class Enemy:
    def __init__(self,cx,cy,rect,speed_factor=1.0):
        self.cx,self.cy=cx,cy
        self.x,self.y=to_px(cx,cy)
        self.territory=rect
        self.speed = speed_factor
        self.sprite=AnimatedSprite("slime",(self.x,self.y),{
            ("idle","right"):2,("idle","left"):2,
            ("walk","right"):2,("walk","left"):2
        })
        self.moving=False
        self.src=(0,0)
        self.dst=(0,0)
        self.t=0
        self.cool=0

    def step(self):
        for _ in range(5):
            dx,dy=random.choice([(1,0),(-1,0),(0,1),(0,-1)])
            nx,ny=self.cx+dx,self.cy+dy
            if is_wall((nx,ny)) or not self.territory.collidepoint(nx,ny):
                continue
            self.cx,self.cy=nx,ny
            self.src,self.dst=(self.x,self.y),to_px(nx,ny)
            self.moving=True
            self.t=0
            self.sprite.state="walk"
            self.sprite.dir="left" if dx<0 else "right"
            return
        self.sprite.state="idle"

    def update(self,dt):
        self.cool-=dt
        if self.moving:
            self.t+=dt/(0.25/self.speed)
            if self.t>=1:
                self.t=1
                self.moving=False
                self.cool=0.5/self.speed
                self.sprite.state="idle"
            self.x = self.src[0]*(1-self.t)+self.dst[0]*self.t
            self.y = self.src[1]*(1-self.t)+self.dst[1]*self.t
        elif self.cool<=0:
            self.step()

        self.sprite.x,self.sprite.y=self.x,self.y
        self.sprite.update(dt)

    def draw(self):
        self.sprite.draw()


mouse_pos = (0, 0)

def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos
def draw_rounded_rect(rect: Rect, color, radius=14):
    radius = max(1, min(radius, min(rect.width//2, rect.height//2)))
    inner = rect.inflate(-2*radius, -2*radius)
    if inner.width > 0 and inner.height > 0:
        screen.draw.filled_rect(inner, color)
    left = Rect(rect.left, rect.top + radius, radius, rect.height - 2*radius)
    right = Rect(rect.right - radius, rect.top + radius, radius, rect.height - 2*radius)
    top = Rect(rect.left + radius, rect.top, rect.width - 2*radius, radius)
    bottom = Rect(rect.left + radius, rect.bottom - radius, rect.width - 2*radius, radius)
    if left.width>0 and left.height>0: screen.draw.filled_rect(left, color)
    if right.width>0 and right.height>0: screen.draw.filled_rect(right, color)
    if top.width>0 and top.height>0: screen.draw.filled_rect(top, color)
    if bottom.width>0 and bottom.height>0: screen.draw.filled_rect(bottom, color)
    screen.draw.filled_circle((rect.left+radius, rect.top+radius), radius, color)
    screen.draw.filled_circle((rect.right-radius, rect.top+radius), radius, color)
    screen.draw.filled_circle((rect.left+radius, rect.bottom-radius), radius, color)
    screen.draw.filled_circle((rect.right-radius, rect.bottom-radius), radius, color)

class Button:
    def __init__(self,text,y):
        self.text=text
        self.r=Rect(WIDTH//2-140,y,280,64)
    def draw(self):
        hover = self.r.collidepoint(mouse_pos)
        sombra = self.r.move(4,4)
        draw_rounded_rect(sombra, (10,10,10), radius=14)
        base = (200,200,255)
        hover_color = (235,235,255)
        color = hover_color if hover else base
        draw_rounded_rect(self.r, color, radius=14)
        borde = self.r.inflate(-4,-4)
        screen.draw.rect(borde, (90,90,140))
        screen.draw.text(self.text, center=self.r.center, fontsize=36, color="black")
    def hit(self,pos): return self.r.collidepoint(pos)

class SmallButton:
    def __init__(self,text,x,y,w=120,h=36):
        self.text=text
        self.r=Rect(x,y,w,h)
    def draw(self):
        hover = self.r.collidepoint(mouse_pos)
        sombra = self.r.move(2,2)
        draw_rounded_rect(sombra, (10,10,10), radius=10)
        base = (210,210,230)
        hover_color = (240,240,245)
        color = hover_color if hover else base
        draw_rounded_rect(self.r, color, radius=10)
        screen.draw.rect(self.r.inflate(-2,-2), (30,30,60))
        screen.draw.text(self.text, center=self.r.center, fontsize=22, color="black")
    def hit(self,pos): return self.r.collidepoint(pos)

btns=[Button("Iniciar",250),Button("Audio ON/OFF",340),Button("Sair do jogo",430)]

def make_game_buttons():
    x=12
    return [
        SmallButton(f"Musica {'ON' if music_on else 'OFF'}",x,12),
        SmallButton(f"Sons {'ON' if sfx_on else 'OFF'}",x,56),
        SmallButton("Voltar ao inicio",x,100),
    ]

game_btns=make_game_buttons()

hero=None
enemies=[]


def draw_map():
    for y,row in enumerate(CURRENT_MAP):
        for x,c in enumerate(row):
            if game_state == STATE_GAME1:
                col = (30,70,30) if c=="#" else (120,180,120)
            elif game_state == STATE_GAME2:
                col = (120, 180, 255) if c=="#" else (200, 230, 255)    
            elif game_state == STATE_GAME3:
                col = (180,140,60) if c=="#" else (240,210,120)
            elif game_state == STATE_GAME4:
                col = (60,60,120) if c=="#" else (140,140,200)
            elif game_state == STATE_GAME5:
                col = (90,10,10) if c=="#" else (180,50,30)
            else:
                col = (200,200,220)

            r = Rect(OFFSET_X + x*TILE, OFFSET_Y + y*TILE, TILE, TILE)
            screen.draw.filled_rect(r, col)

            if (x,y)==(DOOR_CX,DOOR_CY):
                screen.draw.filled_rect(r.inflate(-8,-4),(40,160,40))
                screen.draw.filled_circle((r.right-12,r.centery),3,(230,230,120))

def draw():
    screen.clear()

    if game_state==STATE_MENU:
        for i in range(0, HEIGHT, 6):
            shade = int(20 + (i / HEIGHT) * 40)
            screen.draw.filled_rect(Rect(0, i, WIDTH, 6), (15, shade, 45))

        screen.draw.text("Pixel Runner", center=(WIDTH//2 + 4, 120 + 4), fontsize=54, color=(10,20,30))
        screen.draw.text("Pixel Runner", center=(WIDTH//2, 120), fontsize=54, color=(200,230,255))
        screen.draw.text("Uma pequena aventura", center=(WIDTH//2, 170), fontsize=28, color=(200,220,240))
        screen.draw.text("Use W,A,S,D/SETAS para mover", topleft=(12, HEIGHT-36), fontsize=18, color=(190,190,210))

        for b in btns: b.draw()

    elif game_state in (STATE_GAME1,STATE_GAME2,STATE_GAME3,STATE_GAME4,STATE_GAME5):
        draw_map()
        for e in enemies: e.draw()
        hero.draw()
        for b in game_btns: b.draw()

    else:
        screen.fill((30,30,40))
        screen.draw.text("Issoooo!",center=(WIDTH//2,180),fontsize=72,color="white")
        screen.draw.text("Venceu!",center=(WIDTH//2,260),fontsize=48,color="white")
        screen.draw.text("ENTER ou clique para voltar ao menu",center=(WIDTH//2,360),fontsize=28,color="white")


def update(dt):
    global game_state

    if game_state not in (STATE_GAME1,STATE_GAME2,STATE_GAME3,STATE_GAME4,STATE_GAME5):
        return

    hero.update(dt)


    if not hero.moving:
        if keyboard.left or keyboard.a:
            hero.want_move(-1,0)
        elif keyboard.right or keyboard.d:
            hero.want_move(1,0)
        elif keyboard.up or keyboard.w:
            hero.want_move(0,-1)
        elif keyboard.down or keyboard.s:
            hero.want_move(0,1)


    for e in enemies:
        e.update(dt)
        if hero.sprite.rect.colliderect(e.sprite.rect):
            play_sound("hit")
            hero.sprite.state="hurt"
            hero.sprite.dir="left"
            clock.schedule(hero.reset,0.5)

    if (hero.cx,hero.cy)==(DOOR_CX,DOOR_CY):
        try: sounds.win.play()
        except: pass

        if game_state == STATE_GAME1:
            set_game2()
        elif game_state == STATE_GAME2:
            set_game3()
        elif game_state == STATE_GAME3:
            set_game4()
        elif game_state == STATE_GAME4:
            set_game5()
        else:
            set_win()


def on_key_down(key):
    global music_on,sfx_on,game_state

    if game_state in (STATE_GAME1,STATE_GAME2,STATE_GAME3,STATE_GAME4,STATE_GAME5):
        if key==keys.ESCAPE: set_menu()
        elif key==keys.M:
            music_on=not music_on
            toggle_music()
            game_btns[0].text=f"Musica {'ON' if music_on else 'OFF'}"
        elif key==keys.N:
            sfx_on=not sfx_on
            game_btns[1].text=f"Sons {'ON' if sfx_on else 'OFF'}"

    elif game_state==STATE_WIN and key in (keys.RETURN,keys.SPACE):
        set_menu()

def on_mouse_down(pos):
    global music_on,sfx_on

    if game_state==STATE_MENU:
        if btns[0].hit(pos): set_game1()
        elif btns[1].hit(pos):
            music_on=not music_on
            sfx_on=not sfx_on
            toggle_music()
            btns[1].text=f"Audio {'ON' if music_on else 'OFF'}"
        elif btns[2].hit(pos): exit()

    elif game_state in (STATE_GAME1,STATE_GAME2,STATE_GAME3,STATE_GAME4,STATE_GAME5):
        if game_btns[0].hit(pos):
            music_on=not music_on
            toggle_music()
            game_btns[0].text=f"Musica {'ON' if music_on else 'OFF'}"
        elif game_btns[1].hit(pos):
            sfx_on=not sfx_on
            game_btns[1].text=f"Sons {'ON' if sfx_on else 'OFF'}"
        elif game_btns[2].hit(pos): set_menu()

    elif game_state==STATE_WIN:
        set_menu()


def set_game1():
    global game_state,hero,enemies,CURRENT_MAP,ROWS,COLS,OFFSET_X,OFFSET_Y
    CURRENT_MAP = RAW_MAP1
    ROWS,COLS,OFFSET_X,OFFSET_Y = load_map(CURRENT_MAP)
    hero=Hero()

    enemies=[
        Enemy(10,2,Rect(8,1,10,4)),
        Enemy(20,3,Rect(18,1,6,5)),
        Enemy(15,2,Rect(10,1,15,4)),
        Enemy(7,3,Rect(5,1,10,4)),
        Enemy(12,4,Rect(9,2,14,4)),
        Enemy(18,3,Rect(12,1,12,4)),
    ]

    game_state=STATE_GAME1
    toggle_music()

def set_game2():
    global game_state,hero,enemies,CURRENT_MAP,ROWS,COLS,OFFSET_X,OFFSET_Y
    CURRENT_MAP = RAW_MAP2
    ROWS,COLS,OFFSET_X,OFFSET_Y = load_map(CURRENT_MAP)
    hero=Hero()

    enemies=[]
    for i in range(8):
        ex = random.randint(3, COLS-3)
        ey = random.randint(1, ROWS-3)
        enemies.append( Enemy(ex,ey, Rect(2,1,COLS-4,ROWS-3), speed_factor=1.8 ) )

    game_state=STATE_GAME2
    toggle_music()

def set_game3():
    global game_state,hero,enemies,CURRENT_MAP,ROWS,COLS,OFFSET_X,OFFSET_Y
    CURRENT_MAP = RAW_MAP3
    ROWS,COLS,OFFSET_X,OFFSET_Y = load_map(CURRENT_MAP)
    hero=Hero()

    enemies=[]
    for i in range(12):
        ex = random.randint(3, COLS-3)
        ey = random.randint(1, ROWS-3)
        enemies.append( Enemy(ex,ey, Rect(2,1,COLS-4,ROWS-3), speed_factor=2.6 ) )

    game_state=STATE_GAME3
    toggle_music()

def set_game4():
    global game_state, hero, enemies, CURRENT_MAP, ROWS, COLS, OFFSET_X, OFFSET_Y
    CURRENT_MAP = RAW_MAP4
    ROWS, COLS, OFFSET_X, OFFSET_Y = load_map(CURRENT_MAP)
    hero = Hero()

    enemies = []
    for i in range(14):  # 14 inimigos
        ex = random.randint(3, COLS - 3)
        ey = random.randint(1, ROWS - 3)
        enemies.append( Enemy(ex, ey, Rect(2,1,COLS-4,ROWS-3), speed_factor=3.4 ) )

    game_state = STATE_GAME4
    toggle_music()

def set_game5():
    global game_state, hero, enemies, CURRENT_MAP, ROWS, COLS, OFFSET_X, OFFSET_Y
    CURRENT_MAP = RAW_MAP5
    ROWS, COLS, OFFSET_X, OFFSET_Y = load_map(CURRENT_MAP)
    hero = Hero()

    enemies = []
    for i in range(16):  
        ex = random.randint(3, COLS - 3)
        ey = random.randint(1, ROWS - 3)
        enemies.append( Enemy(ex, ey, Rect(2,1,COLS-4,ROWS-3), speed_factor=4.2 ) )

    game_state = STATE_GAME5
    toggle_music()

def set_menu():
    global game_state
    game_state=STATE_MENU

def set_win():
    global game_state
    game_state=STATE_WIN

def toggle_music():
    if music_on:
        try:
            music.play("bgm")
            music.set_volume(0.6)
        except:
            pass
    else:
        try:
            music.stop()
        except:
            pass
