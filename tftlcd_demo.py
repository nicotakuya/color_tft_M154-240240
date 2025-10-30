# TFT-LCD M154-240240-RGB(ST7789) demo program
# for Raspberry Pi Pico(MicroPython)
# (C)2025 takuya matsubara

import time
import random
import math
from machine import SPI, Pin

VRAM_WIDTH = 240
VRAM_HEIGHT = 240
VRAM_SIZE = VRAM_WIDTH * VRAM_HEIGHT * 2
vram = bytearray(VRAM_SIZE)

GPIO_TFTCS = 17
GPIO_TFTDC = 20
GPIO_TFTSCK = 18
GPIO_TFTTX = 19

def_posx = 0
def_posy = 0
def_tcolor = 0
FONTSIZE = 3

#font data 0x20-0x5F
font = (
 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00 
,0x18,0x18,0x18,0x18,0x18,0x00,0x18,0x00 
,0x6c,0x6c,0x24,0x48,0x00,0x00,0x00,0x00 
,0x28,0x28,0xfe,0x28,0xfe,0x28,0x28,0x00 
,0x10,0x7e,0x90,0x7c,0x12,0xfc,0x10,0x00 
,0x42,0xa4,0x48,0x10,0x24,0x4a,0x84,0x00 
,0x30,0x48,0x48,0x30,0x4a,0x84,0x7a,0x00 
,0x18,0x18,0x08,0x10,0x00,0x00,0x00,0x00 
,0x18,0x20,0x40,0x40,0x40,0x20,0x18,0x00 
,0x30,0x08,0x04,0x04,0x04,0x08,0x30,0x00 
,0x92,0x54,0x38,0xfe,0x38,0x54,0x92,0x00 
,0x10,0x10,0x10,0xfe,0x10,0x10,0x10,0x00 
,0x00,0x00,0x00,0x00,0x30,0x30,0x60,0x00 
,0x00,0x00,0x00,0xfe,0x00,0x00,0x00,0x00 
,0x00,0x00,0x00,0x00,0x00,0x30,0x30,0x00 
,0x00,0x02,0x04,0x08,0x10,0x20,0x40,0x00 
,0x7c,0x82,0x8a,0x92,0xa2,0x82,0x7c,0x00 
,0x10,0x30,0x10,0x10,0x10,0x10,0x38,0x00 
,0xfc,0x02,0x02,0x3c,0x40,0x80,0xfe,0x00 
,0xfc,0x02,0x02,0xfc,0x02,0x02,0xfc,0x00 
,0x18,0x28,0x48,0x88,0xfe,0x08,0x08,0x00 
,0xfe,0x80,0x80,0xfc,0x02,0x02,0xfc,0x00 
,0x7e,0x80,0x80,0xfc,0x82,0x82,0x7c,0x00 
,0xfe,0x02,0x04,0x08,0x10,0x20,0x40,0x00 
,0x7c,0x82,0x82,0x7c,0x82,0x82,0x7c,0x00 
,0x7c,0x82,0x82,0x7e,0x02,0x02,0xfc,0x00 
,0x30,0x30,0x00,0x00,0x30,0x30,0x00,0x00 
,0x30,0x30,0x00,0x00,0x30,0x30,0x60,0x00 
,0x08,0x10,0x20,0x40,0x20,0x10,0x08,0x00 
,0x00,0x00,0x7e,0x00,0x7e,0x00,0x00,0x00 
,0x40,0x20,0x10,0x08,0x10,0x20,0x40,0x00 
,0x7c,0x82,0x82,0x0c,0x10,0x00,0x10,0x00 
,0x7c,0x82,0x02,0x3e,0x42,0x42,0x3c,0x00 
,0x38,0x44,0x82,0x82,0xfe,0x82,0x82,0x00 
,0xf0,0x88,0x88,0xfc,0x82,0x82,0xfc,0x00 
,0x7c,0x82,0x80,0x80,0x80,0x82,0x7c,0x00 
,0xf8,0x84,0x82,0x82,0x82,0x84,0xf8,0x00 
,0xfe,0x80,0x80,0xfe,0x80,0x80,0xfe,0x00 
,0xfe,0x80,0x80,0xfe,0x80,0x80,0x80,0x00 
,0x7c,0x82,0x80,0x8e,0x82,0x82,0x7c,0x00 
,0x82,0x82,0x82,0xfe,0x82,0x82,0x82,0x00 
,0x38,0x10,0x10,0x10,0x10,0x10,0x38,0x00 
,0x38,0x10,0x10,0x10,0x10,0x90,0x60,0x00 
,0x88,0x90,0xa0,0xc0,0xa0,0x90,0x88,0x00 
,0x80,0x80,0x80,0x80,0x80,0x80,0xfe,0x00 
,0x82,0xc6,0xc6,0xaa,0xaa,0x92,0x82,0x00 
,0x82,0xc2,0xa2,0x92,0x8a,0x86,0x82,0x00 
,0x7c,0x82,0x82,0x82,0x82,0x82,0x7c,0x00 
,0xfc,0x82,0x82,0xfc,0x80,0x80,0x80,0x00 
,0x7c,0x82,0x82,0x82,0xba,0x84,0x7a,0x00 
,0xfc,0x82,0x82,0xfc,0x88,0x84,0x82,0x00 
,0x7e,0x80,0x80,0x7c,0x02,0x02,0xfc,0x00 
,0xfe,0x10,0x10,0x10,0x10,0x10,0x10,0x00 
,0x82,0x82,0x82,0x82,0x82,0x82,0x7c,0x00 
,0x82,0x82,0x44,0x44,0x28,0x28,0x10,0x00 
,0x82,0x92,0xaa,0xaa,0xc6,0xc6,0x82,0x00 
,0x82,0x44,0x28,0x10,0x28,0x44,0x82,0x00 
,0x82,0x44,0x28,0x10,0x10,0x10,0x10,0x00 
,0xfe,0x04,0x08,0x10,0x20,0x40,0xfe,0x00 
,0x18,0x10,0x10,0x10,0x10,0x10,0x18,0x00 
,0x44,0x28,0x10,0x7c,0x10,0x7c,0x10,0x00 
,0x30,0x10,0x10,0x10,0x10,0x10,0x30,0x00 
,0x10,0x28,0x44,0x00,0x00,0x00,0x00,0x00 
,0x00,0x00,0x00,0x00,0x00,0x00,0xfe,0x00 
)

# sprite pattern
sp_pattern = (
  0b0010100,
  0b0010100,
  0b0011100,
  0b0011100,
  0b1111111,
  0b1111111,
  0b1011101,

  0b0111110,
  0b1111111,
  0b1000001,
  0b1111111,
  0b1111111,
  0b1100011,
  0b0110110,

  0b0111110,
  0b1111111,
  0b1100011,
  0b1111111,
  0b1111111,
  0b0110110,
  0b1100011,

  0b0110110,
  0b0011100,
  0b0011100,
  0b0011100,
  0b0011100,
  0b0011100,
  0b0001000,

  0b1001001,
  0b0101010,
  0b0000000,
  0b1100011,
  0b0000000,
  0b0101010,
  0b1001001,

  0b0001000,
  0b0011100,
  0b0011100,
  0b0011100,
  0b0011100,
  0b0011100,
  0b0110110,
  
  0b0011100,
  0b0111110,
  0b1110111,
  0b1100011,
  0b1110111,
  0b0111110,
  0b0011100
)

# 16bit color
def color16bit(r,g,b):
    r >>= 3
    g >>= 2
    b >>= 3
    return (r << 11)+(g << 5)+b

# clear vram
def vram_cls():
    for i in range(VRAM_WIDTH*VRAM_HEIGHT*2):
        vram[i] = 0

# コマンド送信
def tft_command(cmd):
    tftdc.low()  # command
    tftcs.low()  # enable
    tftspi.write(cmd.to_bytes(1, "big"))
    tftcs.high() # disable

# データ送信
def tft_data(dat):
    tftdc.high() # data 
    tftcs.low()  # enable
    tftspi.write(dat.to_bytes(1, "big"))
    tftcs.high() # disable
    
# TFT初期化
def tft_init():
    global tftspi,tftcs,tftdc
    
    # polarity=0 phase=0(クロックlow=アイドル、データ立ち上がり=サンプリング)
    # 1Sec / Serial clock cycle 16 ns = 62500000 Hz
    tftspi = SPI(0, baudrate=8000000,sck=Pin(GPIO_TFTSCK), mosi=Pin(GPIO_TFTTX))
    tftcs = Pin(GPIO_TFTCS, mode=Pin.OUT)
    tftdc = Pin(GPIO_TFTDC, mode=Pin.OUT)
    tftcs.high() # disable 
    time.sleep(0.5)
    tft_command(0x01) # SWRESET (01h): Software Reset 
    time.sleep(0.2)
    tft_command(0x11) # SLPOUT (11h): Sleep Out 
    time.sleep(0.1)
    tft_command(0x3A)  # COLMOD (3Ah): Interface Pixel Format
    tft_data(0x55)
    #  b4-6:101=65K-color / 110=262K-color
    #  b0-2:101=16bit / 011=12bit / 110=18bit
    tft_command(0x36) # MADCTL (36h): Memory Data Access Control 
    tft_data(0x00)
    tft_command(0x21) # INVON (21h): Display Inversion On 
    tft_command(0x29) # DISPON (29h): Display On
    time.sleep(0.2)
    tft_command(0x2A)    # CASET (2Ah): Column Address Set
    tft_data(0x00)
    tft_data(0x00)
    tft_data((VRAM_WIDTH-1) >> 8)
    tft_data((VRAM_WIDTH-1) & 0xff)

    tft_command(0x2B)    # RASET (2Bh): Row Address Set
    tft_data(0x00)
    tft_data(0x00)
    tft_data((VRAM_WIDTH-1) >> 8)
    tft_data((VRAM_WIDTH-1) & 0xff)
    time.sleep(0.1)

    vram_locate(0, 0)
    vram_textcolor(color16bit(255,255,255))

# print string
def vram_putstr(textstr):
    textbytes = textstr.encode('utf-8')
    for i in range(len(textbytes)):
        vram_putch( textbytes[i] )

# PRINT DECIMAL
def vram_putdec(num):
    shift=10000
    while shift > 0:
        ch = int(num / shift) % 10
        ch += 0x30
        vram_putch(ch)
        shift = int(shift/10)

# point
def vram_point(x,y):
    if x < 0:return 0
    if y < 0:return 0
    if x >= VRAM_WIDTH:return 0
    if y >= VRAM_HEIGHT:return 0
    ptr = (x + (y*VRAM_WIDTH)) * 2
    return (vram[ptr] << 8)+vram[ptr+1]
    
# pset
def vram_pset(x,y,c):
    if x < 0:return
    if y < 0:return
    if x >= VRAM_WIDTH:return
    if y >= VRAM_HEIGHT:return
    ptr = (x + (y*VRAM_WIDTH)) * 2
    vram[ptr] = c >> 8
    vram[ptr+1] = c & 0xff

# draw line
def vram_line(x1 ,y1 ,x2 ,y2 ,c):
    xs = 1  # X方向の1pixel移動量
    ys = 1  # Y方向の1pixel移動量

    xd = x2 - x1  # X2-X1座標の距離
    if xd < 0:
        xd = -xd  # X2-X1座標の絶対値
        xs = -1    # X方向の1pixel移動量
  
    yd = y2 - y1  # Y2-Y1座標の距離
    if yd < 0:
        yd = -yd  # Y2-Y1座標の絶対値
        ys = -1    # Y方向の1pixel移動量

    vram_pset (x1, y1 ,c)
    e = 0
    if yd < xd:
        while x1 != x2:
            x1 += xs;
            e += (2 * yd)
            if e >= xd:
                y1 += ys
                e -= (2 * xd)

            vram_pset(x1, y1 ,c)
    else:
        while y1 != y2:
            y1 += ys
            e += (2 * xd)
            if e >= yd:
                x1 += xs;
                e -= (2 * yd)

            vram_pset(x1, y1 ,c)

# box fill
def vram_fill(x1 ,y1 ,x2 ,y2 ,color):
  for y in range(y1,y2,1):
    for x in range(x1,x2,1):
      vram_pset(x, y ,color)

# text color
def vram_textcolor(newcolor):
    global def_tcolor
    def_tcolor = newcolor

# locate
def vram_locate(newx,newy):
    global def_posx,def_posy
    def_posx = newx
    def_posy = newy

# scroll
def vram_scroll(xd,yd):
  for y in range(VRAM_HEIGHT):
    for x in range(VRAM_WIDTH):
      color = vram_point(x+xd, y+yd)
      vram_pset(x,y,color)

# put chara
def vram_putch(ch):
    global def_posx,def_posy

    if ch < 0x20:
        if ch == 10:
            def_posx += VRAM_WIDTH
        return

    if def_posx+(8*FONTSIZE) > VRAM_WIDTH:
        def_posx = 0
        def_posy += 8*FONTSIZE

    if def_posy+(8*FONTSIZE) > VRAM_HEIGHT:
        def_posy = VRAM_HEIGHT - (8*FONTSIZE)        
        vram_scroll(0,8*FONTSIZE)

    ptr = (ch - 0x20) * 8
    for i in range(8):
        bitdata = font[ptr]
        ptr += 1
        for j in range(8):
            if bitdata & 0x80:
                tx = def_posx+(j*FONTSIZE)
                ty = def_posy+(i*FONTSIZE)
                for y1 in range(FONTSIZE):
                    for x1 in range(FONTSIZE):
                        vram_pset(tx+x1,ty+y1,def_tcolor);
            bitdata <<= 1
    def_posx += 8*FONTSIZE

#
VRSPSIZE = 7   # Sprite size
VRSPZOOM = 3   # Sprite zoom
# PRINT SPRITE
def vram_spput(x, y, num, color):
    idx =  num * VRSPSIZE
    x -= int(VRSPSIZE*VRSPZOOM/2)
    y -= int(VRSPSIZE*VRSPZOOM/2)
    for j in range(VRSPSIZE):
        dat = sp_pattern[idx]
        idx += 1
        for i in range(VRSPSIZE):
            if dat & (1<<(VRSPSIZE-1)):
                tx = x+(i*VRSPZOOM)    
                ty = y+(j*VRSPZOOM)    
                for y1 in range(VRSPZOOM):
                    for x1 in range(VRSPZOOM):
                        vram_pset(tx+x1,ty+y1,color)

            dat <<= 1

# CLEAR SPRITE
def vram_spclr(x,y):
    x -= int(VRSPSIZE/2)
    y -= int(VRSPSIZE/2)
    for j in range(VRSPSIZE*VRSPZOOM):
        for i in range(VRSPSIZE*VRSPZOOM):
            vram_pset(x+i,y+j,0)

# Display
def disp_update():
    tft_command(0x2C)   # RAMWR (2Ch): Memory Write
    tftdc.high() # data
    tftcs.low()  # enable
    tftspi.write(bytes(vram))
    tftcs.high() # disable 

#----
sankaku = (
    (40 ,6),    #    
    (320,6),    #    
    (180,6),    #    
    (40 ,6),    #    
    (-1 ,-1)    #    
)

# put vectol
def vect_put(vx,vy,angle,zoom,color):
    for i in range(10):
        if sankaku[i][0] == -1:break
        rad = math.radians(sankaku[i][0] + angle)
        x1 = int(math.cos(rad) * sankaku[i][1])
        y1 = int(math.sin(rad) * sankaku[i][1])
        x1 = zoom*x1 + vx
        y1 = zoom*y1 + vy
        if i > 0:
            vram_line(x1,y1,x2,y2,color)
        
        x2 = x1
        y2 = y1

# DEMO
def landscape():
    LANDSCAPEY1 = int((VRAM_HEIGHT/2)-3)
    LANDSCAPEY2 = int((VRAM_HEIGHT/2)+3)
    DEGPITCH = 15
    iso = 0
    color1 = color16bit(0,255,255)
    color2 = color16bit(0,255,  0)
    timeout = 100
    while timeout > 0:
        timeout -= 1
        iso += 3
        if iso < 0:iso += DEGPITCH
        if iso >= DEGPITCH:iso -= DEGPITCH

        vram_cls()
        centerx = int(VRAM_WIDTH/2)
        for i in range(-10,10,1):
            x1 = i*6
            x2 = i*25
            vram_line(centerx+x1,LANDSCAPEY1,centerx+x2, 0,color1)
            vram_line(centerx+x1,LANDSCAPEY2,centerx+x2,VRAM_HEIGHT,color2)

        for deg in range(0,90,DEGPITCH):
            rad = math.radians(deg+iso)
            y = int((1-math.cos(rad))*LANDSCAPEY1)
            vram_line(0,LANDSCAPEY1-y,VRAM_WIDTH,LANDSCAPEY1-y,color1)
            vram_line(0,LANDSCAPEY2+y,VRAM_WIDTH,LANDSCAPEY2+y,color2)
        
        disp_update()

#
class ObjClass:
    def __init__(self):
        self.data = 0
        self.x = -999
        self.y = 0
        self.x1 = 0
        self.y1 = 0
        self.ang = 0
        self.a1 = 0
        self.zoom = 0

#
# DEMO
def vectordemo():
    OFST = 5
    INSEKIMAX =10

    insk = []
    for i in range(INSEKIMAX):
        insk.append(ObjClass())

    color2 = color16bit(255,255,0)

    timeout=100
    while timeout > 0:
        timeout -= 1
        vram_cls()     # clear VRAM

        for i in range(INSEKIMAX):
            tx = insk[i].x
            ty = insk[i].y
            tx += insk[i].x1
            ty += insk[i].y1
            if (ty< -(8<<OFST))or(ty>((VRAM_HEIGHT+8)<<OFST))or(tx < -(8<<OFST))or(tx>((VRAM_WIDTH+8)<<OFST)):
                if random.randrange(2):
                    insk[i].x = -(8 << OFST)
                    insk[i].x1 = random.randrange(40)+60
                else:
                    insk[i].x = (VRAM_WIDTH+8)<<OFST
                    insk[i].x1 = -random.randrange(40)-60
                
                insk[i].ang = random.randrange(36)*10
                insk[i].y = random.randrange(6)*int((VRAM_HEIGHT<<OFST)/6)
                insk[i].y1 = random.randrange(13)-7
                insk[i].a1 = random.randrange(20)-10
                insk[i].zoom = random.randrange(8)+4
                continue
            
            vect_put( tx>>OFST, ty>>OFST, insk[i].ang, insk[i].zoom,color2)
            insk[i].x = tx
            insk[i].y = ty
            insk[i].ang += insk[i].a1
            if insk[i].ang >=360 :insk[i].ang -= 360
            if insk[i].ang <   0 :insk[i].ang += 360
        
        disp_update()

# DEMO
def lifegame():
    WSIZE = int(VRAM_WIDTH/2)
    lx1=( 0, 1, 1, 1, 0,-1,-1,-1)
    ly1=(-1,-1, 0, 1, 1, 1, 0,-1)
    color = color16bit(255,0,255)
    vram_cls()
    for i in range(500):
        x= random.randrange(WSIZE)
        y= random.randrange(WSIZE)
        vram_pset(x,y,color)

    ax=0
    bx=WSIZE
    timeout = 10
    sedai = 0
    while timeout > 0:
        timeout -= 1
        for y in range(WSIZE):
            for x in range(WSIZE):
                color=0
                touch=0
                for i in range(8):
                    if vram_point(ax+x+lx1[i],y+ly1[i]):
                        touch+=1
                        if touch>=4:
                            break

                if touch==2: color=vram_point(ax+x,y)
                if touch==3: color=color16bit(255,255,255)
                vram_pset(bx+x,y,color)
        
        sedai += 1
        vram_fill(0,WSIZE+32,bx+WSIZE-1,WSIZE+64,0)
        vram_textcolor(0xffff)
        vram_locate(0,WSIZE+32)
        vram_putdec(sedai)  # 世代数を表示

        x=ax #swap ax,bx
        ax=bx
        bx=x
        disp_update()

class EnemyClass:
    def __init__(self,x,y,b):
        self.x = x
        self.y = y
        self.b = b

# DEMO
def spacefight():
    TEKIMAX = 15    # 敵の数
    MOVEPITCH = 20  # 移動周期
    MOVESEQ = (10+10+2+2) # 移動シーケンス

    gamespeed = 0 #game speed
    score = 0    #Score
    ax=0 #My Ship X,Y
    ay=0
    overflag = 1
    threthold = int(VRSPSIZE*3/4) * VRSPZOOM

    color1 = color16bit(255,128,  0)
    color2 = color16bit(255,  0,128)
    color3 = color16bit(128,  0,255)
    timeout = 100
    while timeout > 0:
        vram_cls()
        if overflag:
            overflag=0
            vram_textcolor(color16bit(255,255,0))
            vram_locate(13,int(VRAM_HEIGHT/2))
            vram_putstr("READY")
            score=0
            gamespeed = MOVEPITCH
            ax = int(VRAM_WIDTH/2)    # 自機座標
            ay = VRAM_HEIGHT - (VRSPSIZE * VRSPZOOM)
        
        vram_spput(ax, ay, 0,color1)        #my ship
        bx = -1     #自弾座標
        by = -1
        cx = -1     #敵弾座標
        cy = -1
        
        teki = [] # 敵座標
        pitch = int(VRAM_WIDTH/7)
        ofs = int(VRAM_WIDTH/10)
        for i in range(TEKIMAX):
            x = ((i % 5)*pitch)+ofs
            y = (int(i / 5)*pitch)+ofs
            b = 0
            teki.append(EnemyClass(x,y,b))

        tmove = 0
        ttime = 0
        disp_update()
        time.sleep(1)

        while overflag==0:
            vram_cls() 
            key = random.randrange(3)
            if key==1:ax -= 2*VRSPZOOM
            if key==2:ax += 2*VRSPZOOM
            if ax<8*VRSPZOOM:ax=8*VRSPZOOM
            if ax>VRAM_WIDTH-8*VRSPZOOM:ax=VRAM_WIDTH-8*VRSPZOOM
            vram_spput(ax, ay, 0,color1)        #my ship

            if by <= -1:
                bx = ax   # 発射
                by = ay
            else:
                by -= 3*VRSPZOOM
                vram_spput(bx,by,5,color3)    #my meam

            #Enemy Beam
            if cy == -1:
                i=random.randrange(TEKIMAX)
                if teki[i].y != -1:
                    cx = teki[i].x
                    cy = teki[i].y
            else:
                cy += 1*VRSPZOOM  # 弾の移動
                if cy > VRAM_HEIGHT:
                    cy = -1
                else:
                    vram_spput(cx,cy,3,color3)

            ttime = (ttime+1)% gamespeed
            if ttime==0 :
                tmove=(tmove+1) % MOVESEQ
            
            tnum=0
            for i in range(TEKIMAX) :
                x = teki[i].x
                y = teki[i].y
                if(y == -1):continue
                tnum+=1

                if teki[i].b != 0:
                    teki[i].b -= 1
                    vram_spput(x,y,4,1)
                    if teki[i].b==0:
                        teki[i].y = -1
                    continue
                
                if (abs(by-y)<threthold) and (abs(bx-x)<threthold): # 弾が敵に命中
                    if score < 9999:score+=1
                    if gamespeed > 2:gamespeed-=1
                    teki[i].b = 15
                    by = -1
                    continue
                
                if ttime==0:
                    if tmove < 10:#01234
                        x += 2*VRSPZOOM
                    elif tmove < (10+2):#5
                        y += 2*VRSPZOOM
                    elif tmove < (10+2+10):#6789a
                        x -= 2*VRSPZOOM
                    else:
                        y += 2*VRSPZOOM
                    
                    if y >= VRAM_HEIGHT:
                        overflag=1
                
                teki[i].x = x
                teki[i].y = y
                vram_spput(x,y ,1+(tmove & 1),color2)
                continue
            
            if (abs(cy-ay)<threthold) and (abs(cx-ax)<threthold): # 敵の弾が命中
                overflag = 1

            if tnum==0:    #敵全滅
                gamespeed += 8
                break
            
            disp_update()
            timeout -= 1
            if timeout <= 0:break
        
        if overflag: #game over
            vram_spclr(ax,ay)
            vram_spput(ax, ay, 4,color1)
            vram_locate(8,int(VRAM_HEIGHT/4))
            vram_putstr("GAME OVER")
            vram_locate(8,int(VRAM_HEIGHT*3/4))
            vram_putdec(score)
            disp_update()
            time.sleep(2)

# DEMO
def linedemo():
    vram_cls()     # clear VRAM
    xa = random.randrange(VRAM_WIDTH-1)+1
    ya = random.randrange(VRAM_HEIGHT-1)+1
    xb = random.randrange(VRAM_WIDTH-1)+1
    yb = random.randrange(VRAM_HEIGHT-1)+1
    xa1 = random.randrange(17)-8
    ya1 = random.randrange(17)-8
    xb1 = random.randrange(17)-8
    yb1 = random.randrange(17)-8
    timeout = 100
    while timeout > 0:
        timeout -= 1
        xa += xa1
        ya += ya1
        xb += xb1
        yb += yb1
        color = color16bit(random.randrange(256),random.randrange(256),random.randrange(256))
        vram_line(xa ,ya ,xb ,yb ,color)
        if (xa<=0)or(xa>=VRAM_WIDTH) :xa1 = -xa1
        if (ya<=0)or(ya>=VRAM_HEIGHT):ya1 = -ya1
        if (xb<=0)or(xb>=VRAM_WIDTH) :xb1 = -xb1
        if (yb<=0)or(yb>=VRAM_HEIGHT):yb1 = -yb1
        disp_update()

# 
class BallClass:
    def __init__(self,x,y,x1,y1):
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1

# 符合チェック
def fnc_sgn(a):
    if a>0:return 1
    return -1

# DEMO
def balldemo():
    BALLMAX = 20
    MLT = 3
    threthold = VRSPSIZE * VRSPZOOM * MLT
    threthold2 = int(VRSPSIZE * VRSPZOOM/2)
    color1 = color16bit(255,128,255)
    ball = []
    for i in range(BALLMAX):
        x = random.randrange(VRAM_WIDTH)*MLT
        y = random.randrange(VRAM_HEIGHT)*MLT
        x1 = random.randrange(MLT*2)-MLT
        y1 = random.randrange(MLT*2)-MLT
        ball.append(BallClass(x,y,x1,y1))

    timeout = 100
    while timeout > 0:
        timeout -= 1
        vram_cls()
        
        for i in range(BALLMAX):
            x2 = ball[i].x + ball[i].x1
            y2 = ball[i].y + ball[i].y1

            # 衝突
            for j in range(BALLMAX):
                if i==j:continue
                xd = x2-ball[j].x
                yd = y2-ball[j].y

                if (abs(xd) < threthold)and(abs(yd) < threthold):
                    ball[i].x1 = fnc_sgn(xd)*(random.randrange(MLT*2)+1)
                    ball[i].y1 = fnc_sgn(yd)*(random.randrange(MLT*2)+1)
                    ball[j].x1 = -ball[i].x1
                    ball[j].y1 = -ball[i].y1
            
            ball[i].x = x2
            ball[i].y = y2

            x = int(x2/MLT)
            y = int(y2/MLT)
            if x <= threthold2             : ball[i].x1 = (random.randrange(MLT*2)+1)
            if x >= (VRAM_WIDTH-threthold2): ball[i].x1 = -(random.randrange(MLT*2)+1)
            if y <= threthold2              : ball[i].y1 = (random.randrange(MLT*2)+1)
            if y >= (VRAM_HEIGHT-threthold2): ball[i].y1 = -(random.randrange(MLT*2)+1)
            vram_spput(x,y,6,color1)
        
        disp_update()

# 文字表示
def chardemo():
    vram_cls()
    tmpcolor = color16bit(255,0,0)
    for tmpx in range(0,240,10):
        vram_line(0,0,tmpx,239,tmpcolor)

    tmpcolor = color16bit(0,255,0)
    for tmpx in range(0,240,10):
        vram_line(239,0,tmpx,239,tmpcolor)

    tmpcolor = color16bit(0,0,255)
    for tmpx in range(0,240,10):
        vram_line(120,0,tmpx,239,tmpcolor)

    vram_locate(0, 0)
    vram_textcolor(color16bit(255,255,255))
    vram_putstr("TFT LCD\n")
    vram_putstr("DEMO\n")
    disp_update()
    time.sleep(1)

    chrnum = 0x20
    timeout = 100
    while timeout > 0:
        timeout -= 1
        vram_putch(chrnum)
        chrnum += 1
        if(chrnum > 0x5f):
            chrnum = 0x20
        disp_update()
#----
# main
tft_init()

while True:
    chardemo()
    linedemo()
    balldemo()
    landscape()
    vectordemo()
    spacefight()
    lifegame()
