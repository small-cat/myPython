# -*- encoding: utf-8 -*-
import sys, pygame
from pygame.locals import *
from random import randrange

__author__ = "Sholegance (mblrwuzy@gmail.com)"
__date__ = "June 26th 2017"


class EvilSmile(pygame.sprite.Sprite):
    """
    Just for fun
    """
    def __init__(self, smile_image):
        super(EvilSmile, self).__init__()
        # 在画 sprite 的时使用的图像和矩形
        self.image = smile_image
        self.rect = self.image.get_rect()
        self.img_weight = self.rect.width      # record weight of image
        self.reset()

    def reset(self):
        """
        将图片移动到屏幕顶端的随机位置
        """
        self.rect.top = -self.rect.height
        # self.rect.centerx = randrange(screen_size[0])
        # centerx - 矩形中心 x 的坐标
        # centery - 矩形中心 y 的坐标
        # 保证矩形在 screen 窗口之内
        self.rect.centerx = randrange(self.img_weight//2, screen_size[0] - self.img_weight//2)

    def update(self):
        """
        update image, show next frame
        """
        self.rect.top += 1
        if self.rect.top > screen_size[1]:
            self.reset()


# initialization
pygame.init()
screen_size = [800, 600]        # weight hight
pygame.display.set_mode(screen_size)
pygame.mouse.set_visible(False) # 隐藏鼠标光标

# load image
smile_image = pygame.image.load('evil_smile.jpg').convert()

# create a sprite group, and add a EvilSmile object to it
sprites = pygame.sprite.RenderUpdates()
sprites.add(EvilSmile(smile_image))

# get screen, and fill
screen = pygame.display.get_surface()
bg = (255, 255, 255) # white
screen.fill(bg)
pygame.display.flip()


def clear_callback(surf, rect):
    """
    clear image
    """
    surf.fill(bg, rect)

while True:
    # check event
    for event in pygame.event.get():     # 获取所有最近的事件
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()

    # 清除前面的位置
    sprites.clear(screen, clear_callback)
    # update all image
    sprites.update()
    # draw
    updates = sprites.draw(screen)
    # 更新所需显示的部分
    pygame.display.update(updates)
    pygame.time.delay(1)
