import os
import random
import sys
import pygame as pg
import time
import math


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,-0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool,bool]:
    """
    引数:こうかとん、または爆弾のRect
    戻り値:真理値タプル(横判定結果、縦判定結果)
    画面内ならTrue,画面外ならFalse
    """
    yoko,tate = True,True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko,tate


#課題1
def game_over(screen):
    # 画面をブラックアウト
    blackout = pg.Surface((WIDTH,HEIGHT))
    blackout.fill((0,0,0))
    blackout.set_alpha(128) # 半透明に設定
    screen.blit(blackout, (0, 0))


    # 泣いているこうかとんの画像を表示
    sad_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    sad_kk_rect = sad_kk_img.get_rect(center=(WIDTH//2,HEIGHT//2))
    screen.blit(sad_kk_img, sad_kk_rect)


    # 「Game Over」の文字列を表示
    font = pg.font.Font(None, 74)
    text_surface = font.render("Game Over", True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.center=(WIDTH//2,HEIGHT//2+100)
    screen.blit(text_surface, text_rect)


    pg.display.update()
    time.sleep(5) # 5秒間表示


#課題2
def create_bomb_assets():
    bb_imgs = [] #空のリストを作る
    for r in range(1, 11):
        img = pg.Surface((20*r,20*r))
        pg.draw.circle(img,(255,0,0),(10*r,10*r),10*r)
        img.set_colorkey((0,0,0))
        bb_imgs.append(img)


    accs = [a for a in range(1, 11)] #1から10までの加速度を格納
    return bb_imgs,accs


#課題3(カーソルまで途中)
def create_kk_images(kk_img):
    kk_images = {
        (+5,0): kk_img,
        (0,-5): pg.transform.rotozoom(kk_img,90),
        (+5,-5): pg.transform.rotozoom(kk_img,45),
        (+5,+5): pg.transform.rotozoom(kk_img,45),
        (0,+5): pg.transform.rotozoom(kk_img,-90),
        (-5,+5): pg.transform.rotozoom(kk_img,-45),
        (-5,0): pg.transform.flip(kk_img,True,False),
        (-5,-5): pg.transform.rotozoom(kk_img,-45)
    }
    # for direction in DELTA.keys():
    #     angle = -math.degrees(math.atan2(*DELTA[direction]))
    #     kk_images[direction] = pg.transform.rotozoom(kk_img, angle, 1)
    return kk_images  


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200


    #課題2
    bb_imgs,saccs = create_bomb_assets()
    

    bb = bb_imgs[0]
    # bb = pg.Surface((20, 20)) #空のSurface
    # bb.set_colorkey((0,0,0))
    # pg.draw.circle(bb, (255, 0, 0), (10, 10), 10)
    bb_rct = bb.get_rect() #爆弾rectの抽出
    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery = random.randint(0,HEIGHT)


    # bb_rct = bb_imgs[0].get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
    vx,vy = +5,-5
    

    clock = pg.time.Clock()
    tmr = 0


    kk_images = create_kk_images(kk_img)  # こうかとんの画像を生成
    current_kk_img = kk_images[pg.K_UP]


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            

        screen.blit(bg_img, [0, 0])
        if kk_rct.colliderect(bb_rct): #bb_rct.colliderect(kk_rct)
            #こうかとんと爆弾が重なっていたら
            print("Game Over")
            game_over(screen)
            return
        

        #課題2
        # タイマーに応じて爆弾のサイズと加速度を更新
        index = min(tmr//500,9)
        bb = bb_imgs[index]
        avx = vx * saccs[index]
        avy = vy * saccs[index]
        # avx *= 1 if tmr % 2 == 0 else -1


        bb_rct.move_ip(avx, avy)


        screen.blit(bb, bb_rct)


        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0] #横座標、縦座標
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5


        for key,tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0] #横方向
                sum_mv[1] += tpl[1] #縦方向
                current_kk_img = kk_images[key] 


        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        #screen.blit(kk_img,kk_rct)
        screen.blit(current_kk_img,kk_rct)


        bb_rct.move_ip(vx,vy)
        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1 


        screen.blit(bb, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()