import subprocess
U="/root/.claude/uploads/b5d6891b-51f9-5496-9eab-c4f726128166/"
KORA=U+"02fd61a2-KORA-anuncio-15s.mp4"; REEL=U+"2fc8355c-16-1-reel-cara.mp4"
RL=52.567; A=4.8; X1=.3; X2=.4; CTA=4.6
off1=A-X1; off2=off1+RL-X2; TOT=off2+CTA
# punch-zoom segments (jump-cut style)
zooms=[1.0,1.15,1.0,1.25,1.08,1.0,1.18,1.0,1.25,1.0,1.15,1.0]
n=len(zooms); seg=RL/n
fc=[f"[0:v]trim=0:6,setpts=(PTS-STARTPTS)/1.25,scale=1080:1920,fps=30,format=yuv420p,setsar=1,settb=1/30[a]",
    f"[1:v]scale=1080:1920,fps=30,setsar=1,split={n}"+"".join(f"[r{i}]" for i in range(n))]
for i,z in enumerate(zooms):
    s,e=i*seg,min((i+1)*seg,RL)
    w,h=int(1080/z)//2*2,int(1920/z)//2*2
    fc.append(f"[r{i}]trim={s:.3f}:{e:.3f},setpts=PTS-STARTPTS,crop={w}:{h}:(iw-{w})/2:(ih-{h})*0.35,scale=1080:1920,setsar=1[z{i}]")
fc.append("".join(f"[z{i}]" for i in range(n))+f"concat=n={n}:v=1:a=0[b0]")
# overlays on reel: brand bug + product card (slide in/out)
fc.append("[2:v]format=rgba[bug];[3:v]scale=320:-1,format=rgba[card]")
fc.append("[b0][bug]overlay=40:70:enable='gte(t,0.6)'[b1]")
ci,co=20.0,26.0
x=f"if(lt(t,{ci}+0.4),W-(W-720)*(1-pow(1-(t-{ci})/0.4,3)),if(gt(t,{co}-0.4),720+(W-720)*pow((t-{co}+0.4)/0.4,3),720))"
fc.append(f"[b1][card]overlay=x='{x}':y=1150:enable='between(t,{ci},{co})',format=yuv420p,fps=30,settb=1/30[b]")
fc.append(f"[4:v]fps=30,scale=1080:1920,setsar=1,format=yuv420p,settb=1/30[c]")
fc.append(f"[a][b]xfade=transition=zoomin:duration={X1}:offset={off1:.3f}[ab]")
fc.append(f"[ab][c]xfade=transition=fadewhite:duration={X2}:offset={off2:.3f}[abc]")
fc.append(f"color=c=0xC0612F:s=1080x10:r=30[bar];[abc][bar]overlay=x='-1080+1080*t/{TOT:.3f}':y=1910:shortest=1[v]")
fc.append(f"[1:a]adelay={int(off1*1000)}|{int(off1*1000)},apad,atrim=0:{TOT:.3f},afade=t=out:st={off2:.2f}:d=0.6[aout]")
cmd=["ffmpeg","-v","error","-y","-i",KORA,"-i",REEL,"-loop","1","-i","bug.png","-loop","1","-i","card.png","-i","cta.mp4",
     "-filter_complex",";".join(fc),"-map","[v]","-map","[aout]","-t",f"{TOT:.3f}",
     "-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart","/home/user/test-2/KORA-short-edicion.mp4"]
subprocess.run(cmd,check=True); print("total",TOT)
