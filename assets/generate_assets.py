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
    size=(48,64) if kind=="hero" else (32,48)
    a=Image.new("RGBA",size,(0,0,0,0)); p=ImageDraw.Draw(a)
    bob=frame%2
    if kind=="hero":
        # Hand-authored pixel sprite: 48x64 native pixels, four deliberate animation poses.
        ink=(5,8,20,255); deep=(12,18,36,255); navy=(23,34,58,255)
        steel=(43,62,91,255); mid=(75,103,139,255); pale=(139,174,205,255)
        red=(190,27,68,255); scarlet=(246,54,96,255); gold=(244,183,95,255)
        skin=(222,170,145,255); skin_hi=(255,211,177,255)
        blade=(113,229,255,255); blade_hi=(235,255,255,255)
        # Native hand-placed contours and pixel accents; frame variations are authored, not random.
        stride=(0,1,-1,0)[frame%4]
        # Long tied hair and silhouette
        p.polygon([(14,11),(18,5),(29,3),(37,8),(39,17),(35,23),(38,29),(34,35),(12,35),(8,28),(10,18)],fill=ink)
        p.polygon([(17,9),(21,6),(29,6),(35,10),(36,16),(31,19),(17,17)],fill=deep)
        p.polygon([(28,7),(37,9),(39,15),(35,19),(31,17)],fill=navy)
        p.polygon([(34,13),(43,9),(41,17),(37,22),(33,20)],fill=red)
        p.line((36,13,42,10),fill=scarlet,width=2)
        # Face, sharp mask, eye and headband
        p.polygon([(17,12),(31,12),(34,18),(31,25),(20,26),(16,20)],fill=skin)
        p.rectangle((18,14,21,17),fill=skin_hi)
        p.polygon([(17,18),(23,18),(25,21),(18,22)],fill=ink)
        p.polygon([(26,18),(32,17),(31,21),(26,21)],fill=ink)
        p.point((22,19),fill=blade); p.point((29,19),fill=scarlet)
        p.polygon([(15,12),(20,8),(31,8),(36,12),(33,15),(20,13)],fill=navy)
        p.line((17,12,33,11),fill=scarlet,width=2)
        p.rectangle((23,10,27,12),fill=gold)
        p.polygon([(18,23),(32,22),(31,27),(24,30),(17,27)],fill=ink)
        p.line((20,25,30,24),fill=pale,width=1)
        # Neck and layered asymmetric shoulder armor
        p.rectangle((23,26,29,31),fill=skin)
        p.polygon([(17,27),(24,30),(31,27),(39,32),(36,42),(31,46),(15,44),(10,36)],fill=ink)
        p.polygon([(17,28),(24,31),(30,29),(36,33),(33,38),(24,36),(14,39),(12,35)],fill=steel)
        p.polygon([(13,31),(21,32),(19,38),(12,37)],fill=mid)
        p.line((13,32,19,33),fill=pale,width=2)
        p.polygon([(29,30),(37,31),(40,36),(35,40),(29,37)],fill=navy)
        p.line((31,31,37,33),fill=blade,width=1)
        # Torso plate, seams, emblem and waist sash
        p.polygon([(19,34),(31,35),(34,43),(30,49),(17,48),(14,41)],fill=deep)
        p.polygon([(20,35),(29,36),(31,42),(27,45),(19,43)],fill=steel)
        p.line((20,36,27,37),fill=pale,width=1)
        p.polygon([(22,39),(27,39),(26,43),(22,42)],fill=red)
        p.point((24,40),fill=gold)
        p.line((17,44,31,45),fill=ink,width=3)
        p.line((16,45,32,46),fill=scarlet,width=2)
        p.rectangle((23,44,27,48),fill=gold)
        # Flowing split coat and scarf: distinctive crimson silhouette
        p.polygon([(16,43),(21,47),(19,54),(13,60),(8,59),(12,51)],fill=red)
        p.polygon([(17,46),(20,49),(16,55),(11,58),(14,51)],fill=scarlet)
        p.polygon([(29,44),(34,41),(38,49),(35,57),(30,60),(31,52)],fill=red)
        p.polygon([(32,46),(35,49),(33,55),(31,57)],fill=scarlet)
        p.line((12,52,17,49),fill=gold,width=1)
        # Arms, articulated gloves and katana grip
        p.polygon([(14,35),(19,38),(17,45),(13,48),(10,44)],fill=navy)
        p.line((14,38,17,40),fill=mid,width=2)
        p.polygon([(31,35),(36,36),(38,42),(34,47),(30,44)],fill=steel)
        p.line((33,37,36,40),fill=pale,width=1)
        p.polygon([(10,43),(15,44),(15,48),(11,49),(8,46)],fill=ink)
        p.polygon([(33,43),(38,42),(40,46),(36,49),(32,47)],fill=ink)
        p.line((34,44,38,45),fill=gold,width=1)
        # Legs and split shin guards, varied pose for a readable four-frame walk cycle
        p.polygon([(17,47),(24,48),(23,55),(18+stride,58),(13+stride,56)],fill=navy)
        p.polygon([(26,47),(32,47),(34-stride,54),(31-stride,58),(26,55)],fill=deep)
        p.line((17,50,22,50),fill=mid,width=2); p.line((27,50,32,50),fill=mid,width=2)
        p.polygon([(15+stride,54),(22+stride,55),(21+stride,60),(13+stride,60)],fill=steel)
        p.polygon([(27-stride,54),(33-stride,54),(35-stride,60),(27-stride,60)],fill=steel)
        p.line((16+stride,56,21+stride,56),fill=pale,width=1)
        p.line((28-stride,56,33-stride,56),fill=pale,width=1)
        p.polygon([(12+stride,59),(22+stride,59),(24+stride,63),(9+stride,63)],fill=ink)
        p.polygon([(27-stride,59),(36-stride,59),(40-stride,63),(26-stride,63)],fill=ink)
        p.line((12+stride,60,21+stride,60),fill=mid,width=1)
        p.line((29-stride,60,36-stride,60),fill=mid,width=1)
        # Sheathed sword on back; blade and crossguard are crisp individual pixels
        p.line((32,37,43,25),fill=ink,width=5)
        p.line((33,36,43,26),fill=pale,width=2)
        p.line((39,29,45,23),fill=blade_hi,width=1)
        p.line((29,39,36,32),fill=gold,width=2)
        p.point((44,24),fill=blade)
        # Held katana swings through four distinct, intentionally drawn poses
        poses=[((37,42),(46,30),(47,28)),((38,42),(46,25),(47,23)),((37,43),(45,31),(47,29)),((36,42),(44,34),(46,32))]
        (g,h,tip)=poses[frame%4]
        p.line((g[0]-5,g[1]+1,g[0]+3,g[1]-5),fill=ink,width=4)
        p.line((g[0]-3,g[1],g[0]+3,g[1]-5),fill=gold,width=2)
        p.line((g[0],g[1],h[0],h[1]),fill=blade,width=3)
        p.line((h[0],h[1],tip[0],tip[1]),fill=blade_hi,width=1)
        p.point(tip,fill=(255,255,255,255))
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
hero=Image.new("RGBA",(192,64),(0,0,0,0))
for i in range(4): hero.alpha_composite(actor("hero",i),(i*48,0))
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
