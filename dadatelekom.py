
# coding: utf-8

# In[10]:

import numpy as np
import cairocffi as cairo
import moviepy.editor as mpy
import gizeh as gz
import os, re, random


# In[11]:
def gen_gif(term):
    words = []
    regex = re.compile(r"[^a-zA-Z \(\)]")
    f = open('dadablah.txt', 'r')
    for line in f.readlines():
        cl = line.lower().split()
        words.extend(cl)
    bigwords = []
    for w in words:
        w = regex.sub('', w)
        bigwords.append(w)

    def npshift(seq, n):
        return np.concatenate((seq[-n:], seq[:-n]))

    # Rotate array by a random shift
    bigwords = npshift(bigwords, random.randint(0, int(len(bigwords)/2)))
    #bigwords


    # In[12]:

    # image parameters
    W,H = 320,320
    D = 10


    # In[14]:

    # load background png into an image pattern
    image_surface = cairo.ImageSurface.create_from_png("bg/CanvasByMinimaxDadamax.png")
    im = 0+np.frombuffer(image_surface.get_data(), np.uint8)
    im.shape = (image_surface.get_height(), image_surface.get_width(), 4)
    im = im[:,:,[2,1,0,3]] # put RGB back in order
    gizeh_pattern = gz.ImagePattern(im)
    bg_rect = gz.rectangle(W*2, H*2, fill=gizeh_pattern)

    # load additional png
    def get_rand_image():
        random_image_file = os.path.join("img", random.choice(os.listdir("img")))
        random_image_file
        image_surface = cairo.ImageSurface.create_from_png(random_image_file)
        im = 0+np.frombuffer(image_surface.get_data(), np.uint8)
        im.shape = (image_surface.get_height(), image_surface.get_width(), 4)
        gizeh_pattern = gz.ImagePattern(im)
        return gz.rectangle(W*2, H*2, fill=gizeh_pattern)

    start_at = 0
    fr_timer = 0
    chunk_len = 4
    scenelen = 10

    rand_images = [get_rand_image() for i in range(0,D)]

    def make_frame(t):
        surface = gz.Surface(W,H, bg_color=(0,0.0,0.0))
        bg_rect.draw(surface)
        rand_images[int(t)].draw(surface)

        next_frm = chunk_len * int(t / scenelen)
        nf_from = int(t) * chunk_len
        nf_to = nf_from + chunk_len
        chosen = bigwords[nf_from:nf_to]

        for i in range(0, chunk_len):
            fade = 1
            if i == int((t * 2) % chunk_len): fade = 0.5
                #((chunk_len - i) / chunk_len) + 1 * (t % scenelen)),
            ti = gz.text(chosen[i],
              fontfamily="Century Schoolbook", fontsize=50,
              fill=(1, 0.9, 0.6, fade),
              xy=(W/2,60 + i * 70))
            ti.draw(surface)

        counter = gz.text("%d" % t,
                      fontfamily="Courier New", fontsize=10,
                      fill=(1,1,1), xy=(10, H-20))
        counter.draw(surface)

        return surface.get_npimage()

    clip = mpy.VideoClip(make_frame, duration=D)
    clip.write_gif("output.gif", fps=4, opt="OptimizePlus")

    return " ".join(bigwords)
    # ![](output.gif)
