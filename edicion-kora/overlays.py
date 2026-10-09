from PIL import Image, ImageDraw, ImageFont, ImageFilter
F="/root/.claude/skills/synced/1105a344-2261-4c7b-b8e0-949fe1cfb1ba_bc04ba54-0cca-4cc1-801e-a1635b07c215/motion-de-marca/fuentes"
OR=(192,97,47); CREAM=(244,235,221); DARK=(30,26,23)
# brand bug
f=ImageFont.truetype(F+"/ArchivoBlack-Regular.ttf",40); g=ImageFont.truetype(F+"/Inter-SemiBold.ttf",26)
bug=Image.new("RGBA",(520,90),(0,0,0,0)); d=ImageDraw.Draw(bug)
d.rounded_rectangle((0,0,519,89),45,fill=OR+(235,))
d.text((32,18),"KORA",font=f,fill=CREAM); d.text((175,30),"burbujas de altura",font=g,fill=CREAM)
bug.save("bug.png")
# product card
can=Image.open("can.png").convert("RGB").resize((285,495))
W,H=345,640; card=Image.new("RGBA",(W+60,H+60),(0,0,0,0))
sh=Image.new("RGBA",card.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((30,40,30+W,40+H),36,fill=(0,0,0,140))
card=Image.alpha_composite(card,sh.filter(ImageFilter.GaussianBlur(16)))
inner=Image.new("RGBA",(W,H),CREAM+(255,)); m=Image.new("L",(W,H),0); ImageDraw.Draw(m).rounded_rectangle((0,0,W-1,H-1),36,fill=255)
im=Image.new("L",can.size,0); ImageDraw.Draw(im).rounded_rectangle((0,0,284,494),26,fill=255)
inner.paste(can,(30,30),im)
d=ImageDraw.Draw(inner); h=ImageFont.truetype(F+"/ArchivoBlack-Regular.ttf",30)
t="PRUÉBALA FRÍA"; w=d.textlength(t,font=h); d.text(((W-w)/2,560),t,font=h,fill=OR)
card.paste(inner,(30,30),m); card.save("card.png")
