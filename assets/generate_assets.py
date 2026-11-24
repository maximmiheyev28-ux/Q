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
    # Carefully layered native-resolution pixel character art.
    a=Image.new("RGBA",(32,48),(0,0,0,0)); p=ImageDraw.Draw(a)
    bob=frame%2
    if kind=="hero":
        ink=(7,10,23,255); shadow=(17,23,43,255); steel=(38,53,82,255)
        light=(91,119,157,255); red=(224,35,82,255); red_hi=(255,91,125,255)
        skin=(227,171,147,255); cyan=(76,224,255,255); white=(220,245,255,255)
        # silhouette, tied hair and angular headband
        p.polygon([(8,8+bob),(11,3+bob),(21,3+bob),(25,9+bob),(24,16+bob),(27,21+bob),(26,30+bob),(23,35+bob),(9,35+bob),(6,29+bob),(5,18+bob)],fill=ink)
        p.polygon([(8,8+bob),(12,4+bob),(21,5+bob),(24,10+bob),(19,13+bob),(10,12+bob)],fill=shadow)
        p.rectangle((10,10+bob,22,15+bob),fill=skin)
        p.rectangle((11,10+bob,13,11+bob),fill=(255,218,190,255))
        p.rectangle((17,12+bob,21,13+bob),fill=ink)
        p.polygon([(6,8+bob),(11,3+bob),(24,5+bob),(27,9+bob),(22,8+bob),(14,7+bob),(8,12+bob)],fill=(26,33,58,255))
        p.line((8,8+bob,23,7+bob),fill=red_hi,width=2); p.rectangle((13,7+bob,18,9+bob),fill=red)
        # layered shoulder plates and torso with bright rim highlights
        p.polygon([(10,15+bob),(17,17+bob),(24,14+bob),(28,19+bob),(24,25+bob),(22,31+bob),(9,31+bob),(6,23+bob)],fill=steel)
        p.polygon([(10,16+bob),(16,19+bob),(22,16+bob),(25,19+bob),(21,22+bob),(11,22+bob)],fill=light)
        p.line((8,19+bob,12,22+bob),fill=white,width=1); p.line((22,18+bob,26,19+bob),fill=cyan,width=1)
        p.rectangle((12,22+bob,21,29+bob),fill=shadow)
        for yy in (23,26,28): p.line((12,yy+bob,21,yy+bob),fill=steel,width=1)
        p.polygon([(8,22+bob),(12,24+bob),(11,29+bob),(7,27+bob)],fill=red)
        p.polygon([(20,23+bob),(25,20+bob),(26,24+bob),(22,28+bob)],fill=red_hi)
        p.line((10,29+bob,23,29+bob),fill=(255,183,104,255),width=2)
        # belt, split armored skirt, articulated legs and boots
        p.rectangle((10,30+bob,23,33+bob),fill=ink); p.line((11,31+bob,22,31+bob),fill=red_hi,width=1)
        p.rectangle((15,30+bob,18,33+bob),fill=(241,195,111,255))
        p.polygon([(10,33+bob),(16,34+bob),(14,39),(9,39)],fill=steel)
        p.polygon([(18,34+bob),(23,32+bob),(24,39),(19,39)],fill=steel)
        p.line((10,35+bob,14,35+bob),fill=light,width=1); p.line((20,35+bob,23,35+bob),fill=light,width=1)
        p.rectangle((9,39,15,43),fill=shadow); p.rectangle((19,39,25,43),fill=shadow)
        p.line((9,41,15,41),fill=steel,width=1); p.line((19,41,25,41),fill=steel,width=1)
        p.polygon([(7,43),(16,43),(17,46),(5,46)],fill=ink); p.polygon([(18,43),(26,43),(29,46),(17,46)],fill=ink)
        p.line((7,44,14,44),fill=light,width=1); p.line((20,44,26,44),fill=light,width=1)
        # visible sheath and luminous katana, crisp pixel highlights
        p.line((21,27,29,17),fill=ink,width=4); p.line((22,26,30,16),fill=(188,221,240,255),width=2)
        p.line((27,17,31,12),fill=white,width=1); p.line((19,28,24,23),fill=(255,194,115,255),width=2)
        p.point((30,13),fill=cyan); p.point((28,15),fill=cyan)
    elif kind=="ninja":
        ink=(7,9,24,255); violet=(43,29,72,255); mid=(82,58,126,255); red=(255,48,111,255)
        p.polygon([(8,9),(12,4),(22,5),(25,12),(24,19),(28,25),(25,34),(8,34),(5,24)],fill=ink)
        p.polygon([(9,8),(13,5),(22,7),(24,12),(19,14),(10,13)],fill=violet)
        p.rectangle((10,12,22,16),fill=(229,183,167,255)); p.line((11,13,14,12),fill=red,width=2); p.line((18,12,21,13),fill=red,width=2)
        p.polygon([(7,17),(24,16),(27,24),(23,31),(10,31),(5,24)],fill=violet)
        p.polygon([(8,18),(17,21),(24,18),(22,23),(10,23)],fill=mid)
        p.polygon([(8,22),(2,19),(1,26),(12,28),(5,33),(17,30)],fill=red)
        p.rectangle((10,31,15,42),fill=ink); p.rectangle((19,30,24,41),fill=ink)
        p.line((11,34,14,34),fill=mid); p.line((20,34,23,34),fill=mid)
        p.rectangle((7,41,16,45),fill=ink); p.rectangle((18,40,27,44),fill=ink)
        p.line((8,42,15,42),fill=red,width=1); p.line((20,41,26,41),fill=red,width=1)
        p.line((22,25,31,19),fill=(222,238,255,255),width=2); p.point((30,19),fill=red)
    elif kind=="gunner":
        ink=(9,14,31,255); armor=(42,58,82,255); hi=(101,128,157,255); orange=(255,101,67,255)
        p.polygon([(9,8),(12,4),(22,5),(25,12),(23,18),(27,25),(24,34),(8,34),(5,24)],fill=ink)
        p.rectangle((10,11,22,16),fill=(194,158,139,255)); p.rectangle((11,12,14,13),fill=orange)
        p.polygon([(8,17),(24,16),(27,23),(23,32),(9,32),(5,23)],fill=armor)
        p.polygon([(8,18),(16,20),(23,18),(22,23),(10,24)],fill=hi)
        p.rectangle((11,24,21,29),fill=ink); p.line((12,25,20,25),fill=orange,width=1)
        p.rectangle((5,21,10,30),fill=ink); p.line((6,23,9,23),fill=hi)
        p.rectangle((22,21,30,26),fill=ink); p.rectangle((28,20,32,24),fill=orange)
        p.rectangle((10,32,15,42),fill=ink); p.rectangle((19,32,24,42),fill=ink)
        p.line((11,35,14,35),fill=hi); p.line((20,35,23,35),fill=hi)
        p.rectangle((7,41,16,45),fill=ink); p.rectangle((18,41,27,45),fill=ink)
        p.line((8,42,15,42),fill=orange,width=1); p.line((20,42,26,42),fill=orange,width=1)
    else:
        ink=(13,13,39,255); purple=(80,56,149,255); glow=(194,63,255,255); cyan=(79,229,255,255)
        p.ellipse((5,8,27,31),fill=ink,outline=purple,width=2)
        p.ellipse((9,12,23,27),fill=purple,outline=glow,width=2)
        p.ellipse((13,16,19,23),fill=cyan); p.point((15,18),fill=(255,255,255,255))
        p.polygon([(6,14),(1,5),(11,11)],fill=purple); p.polygon([(26,14),(31,5),(21,11)],fill=purple)
        p.line((16,30,16,39),fill=glow,width=2); p.ellipse((11,37,21,47),outline=glow,width=2)
        p.line((12,40,20,40),fill=cyan,width=1)
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
