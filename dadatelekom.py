
# coding: utf-8

# In[1]:

import numpy as np
import cairocffi as cairo
import moviepy.editor as mpy
import gizeh as gz
import os, re, random

def gen_gif(term):
    # In[2]:

    words = []
    regex = re.compile(r"[^a-zA-Z ]")
    f = open('dadablah.txt', 'r')
    for line in f.readlines():
        cl = line.lower().split()
        words.extend(cl)
    bigwords = []
    for w in words:
        w = regex.sub('', w)
        if len(w) > 1:
            bigwords.append(w)
    #bigwords


    # In[23]:

    # image parameters
    W,H = 320,320
    D = 5


    # In[89]:

    # load background png into an image pattern
    image_surface = cairo.ImageSurface.create_from_png("bg/CanvasByMinimaxDadamax.png")
    im = 0+np.frombuffer(image_surface.get_data(), np.uint8)
    im.shape = (image_surface.get_height(), image_surface.get_width(), 4)
    im = im[:,:,[2,1,0,3]] # put RGB back in order
    gizeh_pattern = gz.ImagePattern(im)
    bg_rect = gz.rectangle(W*2, H*2, fill=gizeh_pattern)

    # load additional png
    random_image_file = os.path.join("img", random.choice(os.listdir("img")))
    random_image_file
    image_surface = cairo.ImageSurface.create_from_png(random_image_file)
    im = 0+np.frombuffer(image_surface.get_data(), np.uint8)
    im.shape = (image_surface.get_height(), image_surface.get_width(), 4)
    gizeh_pattern = gz.ImagePattern(im)
    image_1 = gz.rectangle(W*2, H*2, fill=gizeh_pattern)

    start_at = 0
    fr_timer = 0
    chunk_len = 4

    pad = 50
    x, y = [], []
    for i in range(0, chunk_len):
        x.append(random.randint(pad, W-pad))
        y.append(random.randint(pad, H-pad))

    def make_frame(t):
        surface = gz.Surface(W,H, bg_color=(0,0.0,0.0))
        bg_rect.draw(surface)
        image_1.draw(surface)

        next_frm = chunk_len * int(t)
        chosen = bigwords[next_frm : next_frm + chunk_len]
        if t % 1 == 0:
            for i in range(0, chunk_len):
                x[i] = random.randint(pad, W-pad)
                y[i] = random.randint(pad, H-pad)

        t1 = gz.text(chosen[0],
                      fontfamily="Impact", fontsize=50,
                      fill=(1,1,1), angle=-(t/D)*np.pi/2).translate((x[0],y[0]))

        t2 = gz.text(chosen[1],
                      fontfamily="Impact", fontsize=60,
                      fill=(1,1,1), xy=(y[0],x[0]))

        angle = 2*np.pi*(1.0+t/D)
        center = W*(0.5+gz.polar2cart(0.3,angle))
        t3 = gz.text(chosen[2],
                      fontfamily="Impact", fontsize=70,
                      fill=(1,0,0), xy=center)

        t4 = gz.text(chosen[3],
                      fontfamily="Impact", fontsize=90,
                      fill=(1,0.8,0.4,t*0.2), xy=(x[2]-t*30,y[2]))

        t2.draw(surface)
        t4.draw(surface)
        t3.draw(surface)
        t1.draw(surface)

        counter = gz.text("%d" % t,
                      fontfamily="Courier New", fontsize=10,
                      fill=(1,1,1), xy=(10, H-20))
        counter.draw(surface)

        return surface.get_npimage()

    clip = mpy.VideoClip(make_frame, duration=D)
    clip.write_gif("output.gif", fps=5, opt="OptimizePlus")


    # ![](output.gif..)
