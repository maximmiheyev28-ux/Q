from PIL import Image, ImageDraw
import os, random
os.makedirs("assets", exist_ok=True)
random.seed(17)

# Parallax-ready night city background, authored at native game resolution.
W,H=480,270
im=Image.new("RGBA",(W,H),(5,7,25,255)); d=ImageDraw.Draw(im)
# moon and layered storm clouds
d.ellipse((335,25,425,115),fill=(222,83,205,255),outline=(255,151,233,255),width=2)
for r in range(0,5):
    d.arc((340+r*2,30+r*2,420-r*2,110-r*2),0,360,fill=(255,145-r*12,238-r*9,180))
for i in range(90):
    x=random.randrange(W); y=random.randrange(0,100)
    d.ellipse((x,y,x+random.randrange(12,55),y+random.randrange(3,12)),fill=(16,20+random.randrange(8),62+random.randrange(25),255))
# skyline depth
for layer in range(3):
    base=170+layer*28
    x=-10
    while x<W:
        bw=random.randrange(18,55); bh=random.randrange(45,135)
        col=[(14,18,55,255),(16,23,72,255),(20,27,65,255)][layer]
        d.rectangle((x,base-bh,x+bw,base),fill=col,outline=(39,48,111,255))
        for wx in range(x+4,x+bw-3,7):
            for wy in range(base-bh+7,base-4,10):
                if random.random()<.48:
                    d.rectangle((wx,wy,wx+2,wy+4),fill=random.choice([(28,203,245,255),(225,39,194,255),(255,164,83,255)]))
        x+=bw+random.randrange(3,10)
# pagoda silhouette and torii
d.polygon([(55,154),(94,130),(133,154),(124,158),(64,158)],fill=(8,10,31,255),outline=(55,77,157,255))
d.rectangle((72,158,116,194),fill=(8,10,31,255))
d.polygon([(330,158),(372,145),(414,158),(408,163),(336,163)],fill=(7,10,30,255))
d.rectangle((348,163,354,204),fill=(7,10,30,255)); d.rectangle((390,163,396,204),fill=(7,10,30,255))
# foreground rooftop architecture
d.rectangle((0,205,480,270),fill=(8,12,28,255))
d.rectangle((0,205,480,210),fill=(23,83,122,255))
for x in range(0,480,32):
    d.rectangle((x,218,x+22,263),fill=(12,18,39,255),outline=(35,50,91,255))
    d.line((x+3,224,x+18,224),fill=(28,130,167,255),width=1)
for x in range(8,480,47):
    d.line((x,211,x,218),fill=(77,111,150,255),width=2)
# neon signs and puddles
for x,y,c in [(24,181,(255,37,187,255)),(202,193,(27,207,255,255)),(420,178,(255,35,183,255))]:
    d.rectangle((x,y,x+19,y+15),fill=(14,18,48,255),outline=c,width=2)
    d.line((x+4,y+7,x+15,y+7),fill=c,width=2)
for x in range(0,480,3):
    if random.random()<.42:
        d.line((x,211,x+random.randrange(1,8),211),fill=random.choice([(24,118,158,120),(179,34,153,120)]))
im.save("assets/city.png")

# Repeating metal rooftop tile
tile=Image.new("RGBA",(16,16),(20,29,48,255)); t=ImageDraw.Draw(tile)
t.rectangle((0,0,15,2),fill=(55,91,117,255)); t.rectangle((0,3,15,14),fill=(24,34,54,255))
t.line((1,5,14,5),fill=(35,54,77,255)); t.line((1,13,14,13),fill=(9,16,32,255))
t.rectangle((2,7,4,9),fill=(64,112,137,255)); t.rectangle((12,7,14,9),fill=(64,112,137,255))
t.point((7,8),fill=(30,202,224,255)); tile.save("assets/metal_tile.png")

# Pixel-art character builder: distinct silhouettes and palettes.
def actor(kind,frame):
    a=Image.new("RGBA",(32,48),(0,0,0,0)); p=ImageDraw.Draw(a)
    bob=frame%2
    if kind=="hero":
        dark=(15,19,36,255); mid=(37,48,77,255); red=(224,35,87,255); skin=(232,174,148,255); cyan=(77,226,255,255)
        p.ellipse((10,3+bob,23,16+bob),fill=dark,outline=(79,100,142,255))
        p.rectangle((11,8+bob,23,11+bob),fill=skin); p.rectangle((8,13+bob,25,31+bob),fill=dark)
        p.polygon([(8,15+bob),(17,20+bob),(27,16+bob),(23,28+bob),(9,26+bob)],fill=mid)
        p.polygon([(9,16+bob),(2,19+bob),(13,23+bob),(4,27+bob),(18,25+bob)],fill=red)
        p.rectangle((10,29+bob,15,41),fill=dark); p.rectangle((19,29+bob,24,40),fill=dark)
        p.rectangle((7,40,16,44),fill=(7,10,20,255)); p.rectangle((18,39,27,43),fill=(7,10,20,255))
        p.line((22,22,30,15),fill=(173,226,245,255),width=2); p.line((29,15,31,13),fill=cyan,width=1)
    elif kind=="ninja":
        dark=(10,13,29,255); purple=(55,34,83,255); red=(255,53,105,255)
        p.ellipse((9,5,24,19),fill=dark,outline=(112,68,135,255)); p.rectangle((10,12,23,15),fill=red)
        p.rectangle((7,18,26,32),fill=purple); p.polygon([(7,19),(1,24),(10,27),(4,33),(18,29)],fill=red)
        p.rectangle((10,30,15,42),fill=dark); p.rectangle((19,30,24,42),fill=dark)
        p.rectangle((7,41,16,45),fill=(4,6,15,255)); p.rectangle((18,41,27,45),fill=(4,6,15,255))
        p.line((22,25,31,20),fill=(211,223,242,255),width=2)
    elif kind=="gunner":
        dark=(18,24,43,255); armor=(54,72,96,255); orange=(255,95,69,255)
        p.ellipse((9,4,23,18),fill=dark,outline=(109,141,164,255)); p.rectangle((11,11,22,14),fill=orange)
        p.rectangle((7,18,26,33),fill=armor); p.rectangle((5,21,10,31),fill=dark)
        p.rectangle((23,22,31,26),fill=dark); p.rectangle((29,21,32,24),fill=orange)
        p.rectangle((10,32,15,43),fill=dark); p.rectangle((19,32,24,43),fill=dark)
        p.rectangle((7,42,16,46),fill=(4,7,14,255)); p.rectangle((18,42,27,46),fill=(4,7,14,255))
    else:
        dark=(21,20,52,255); glow=(181,49,255,255)
        p.ellipse((6,10,26,30),fill=dark,outline=glow,width=2); p.ellipse((12,16,20,24),fill=glow)
        p.polygon([(6,15),(1,7),(9,11)],fill=(74,81,147,255)); p.polygon([(25,15),(31,7),(23,11)],fill=(74,81,147,255))
        p.line((16,30,16,39),fill=glow,width=2); p.ellipse((12,38,20,46),outline=glow,width=2)
    return a
hero=Image.new("RGBA",(128,48),(0,0,0,0))
for i in range(4): hero.alpha_composite(actor("hero",i),(i*32,0))
hero.save("assets/samurai.png")
foes=Image.new("RGBA",(96,48),(0,0,0,0))
for i,k in enumerate(("ninja","gunner","drone")): foes.alpha_composite(actor(k,0),(i*32,0))
foes.save("assets/enemies.png")

# Projectile atlas: shuriken, bullet, plasma orb, thrown blade.
proj=Image.new("RGBA",(64,16),(0,0,0,0)); q=ImageDraw.Draw(proj)
q.polygon([(8,0),(11,5),(16,8),(11,11),(8,16),(5,11),(0,8),(5,5)],fill=(210,240,255,255),outline=(48,197,255,255))
q.rectangle((19,6,31,9),fill=(255,89,81,255)); q.rectangle((28,5,31,10),fill=(255,198,115,255))
q.ellipse((35,3,47,15),fill=(175,55,255,255),outline=(239,174,255,255),width=2); q.ellipse((39,7,43,11),fill=(255,255,255,255))
q.polygon([(56,1),(63,8),(56,15),(53,8)],fill=(115,235,255,255),outline=(230,255,255,255))
proj.save("assets/projectiles.png")

# Four-frame slash / hit / muzzle-flash FX strip.
fx=Image.new("RGBA",(256,48),(0,0,0,0)); f=ImageDraw.Draw(fx)
for i in range(4):
    ox=i*64; alpha=255-i*48
    f.arc((ox+4,5,ox+58,45),205,330,fill=(75,225,255,alpha),width=max(1,5-i))
    f.arc((ox+9,9,ox+53,41),205,330,fill=(230,250,255,alpha),width=2)
    if i<3:
        for j in range(5-i):
            x=ox+18+j*7; y=8+(j*11+i*5)%31
            f.rectangle((x,y,x+2,y+2),fill=(255,67,170,alpha))
fx.save("assets/effects.png")
print("Generated:", ", ".join(sorted(os.listdir("assets"))))
