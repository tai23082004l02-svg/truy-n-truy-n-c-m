from pathlib import Path
import json,subprocess,concurrent.futures,math
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent
import os
TMP=Path(os.environ.get('VIDEO_BUILD_DIR', '/tmp/bo-khong-biet-noi-thuong-con-build'));TMP.mkdir(parents=True,exist_ok=True)
# Each point is a cut matched to narration; cell is zero-based, row-major.
plan={
1:[(0,0),(2.38,1),(6.12,2),(10.58,3),(14.42,4),(18.98,5),(22,7),(26.76,8),(28.5,9),(30.62,10),(34.2,11),(37.68,12),(40.56,13),(44.5,15)],
2:[(48,0),(52.5,1),(58,6),(61.4,2),(65.02,5),(69,7),(76.2,8),(80.2,9),(84.8,10),(88.3,11),(92.14,12),(96,13),(100,14)],
3:[(104,0),(107.2,2),(111,3),(115.5,4),(120.28,6),(123.5,7),(127,8),(130,9),(133,10),(136.48,12),(140,13),(143.5,15)],
4:[(147,0),(150,1),(154,3),(157,4),(160.44,5),(164,8),(167.8,10),(171.92,11),(175.7,13),(180.1,15)],
5:[(188.52,2),(195.3,4),(199,5),(201.16,6),(203.2,10),(207,12),(211,13),(214.18,15)],
6:[(218,0),(222,1),(226.32,3),(232.46,2),(238.7,4),(246.14,5),(251.58,6),(259.88,7),(263,8),(267.3,10),(273.76,12),(278.96,13)],
7:[(280.86,0),(287.72,1),(291.5,2),(294.2,3),(297.16,4),(300.68,5),(306.02,6),(309.7,7),(312.84,9),(316.12,10),(319.5,11),(323.54,13),(327,14),(331,15)],
8:[(336.08,0),(339.2,1),(342.46,2),(346.1,3),(350.36,5),(352.8,6),(355,7),(357.18,8),(359,9),(362.34,10),(364.66,11),(368.7,12),(374.98,13),(378.48,15)],
9:[(381.74,0),(387.18,1),(390.14,2),(393.06,3),(397.32,4),(399.52,5),(401.46,6),(404.2,7),(407.2,8),(410,9),(413,10),(416.16,11),(422.78,12),(426.92,13),(429.5,14)],
10:[(433.94,0),(437,2),(438.78,3),(440,4),(443,5),(447.66,6),(451.8,7),(453.48,8),(457,9),(460,10),(463.28,11),(465.8,12),(472.52,13),(475.86,14),(479.62,15)],
11:[(481.6,0),(486.86,2),(491,3),(494.3,4),(496.38,5),(498.18,6),(500.7,8),(503.02,9),(505.5,10),(508,11),(510.46,12),(512.78,13),(515.02,14),(519.16,15)]}
# Crop actual white gutters, not blindly equal quarters.
def runs(ids):
 rs=[]
 for i in ids:
  if rs and i==rs[-1][-1]+1:rs[-1].append(int(i))
  else:rs.append([int(i)])
 return [(r[0],r[-1]) for r in rs]
crops={}
for sheet in plan:
 p=ROOT/f'project/assets/sheet-{sheet:02}.png'
 if not p.exists():raise FileNotFoundError(p)
 a=np.array(Image.open(p).convert('RGB'));h,w=a.shape[:2];white=np.min(a,axis=2)>205
 xr=[r for r in runs(np.where(white.mean(0)>.95)[0]) if r[1]-r[0]>=1 and 10<r[0]<w-10]
 yr=[r for r in runs(np.where(white.mean(1)>.95)[0]) if r[1]-r[0]>=1 and 10<r[0]<h-10]
 assert len(xr)==len(yr)==3,(sheet,xr,yr)
 xs=[(1,xr[0][0]-2),(xr[0][1]+3,xr[1][0]-2),(xr[1][1]+3,xr[2][0]-2),(xr[2][1]+3,w-2)]
 ys=[(1,yr[0][0]-2),(yr[0][1]+3,yr[1][0]-2),(yr[1][1]+3,yr[2][0]-2),(yr[2][1]+3,h-2)]
 cells=[]
 for cell in range(16):
  x0,x1=xs[cell%4];y0,y1=ys[cell//4];cw=x1-x0;ch=y1-y0
  # Fit a 16:9 center crop without stretching; strip gutters before scale.
  if cw/ch>16/9:nw=int(ch*16/9);x0+=(cw-nw)//2;cw=nw
  else:nh=int(cw*9/16);y0+=(ch-nh)//2;ch=nh
  cells.append({'x':x0,'y':y0,'width':cw,'height':ch})
 crops[str(sheet)]={'source_size':[w,h],'vertical_gutters':xr,'horizontal_gutters':yr,'cells':cells}
(ROOT/'project/grid-crops.json').write_text(json.dumps(crops,indent=2))
points=sorted((t,s,c) for s,items in plan.items() for t,c in items)
# Remove cuts closer than 2.5 seconds; keep story-matched anchors and avoid flashes.
filtered=[]
for point in points:
 if not filtered or point[0]-filtered[-1][0]>=2.5: filtered.append(point)
points=filtered
TOTAL=round(524.376*24)
shots=[]
for i,(t,s,c) in enumerate(points):
 start=round(t*24);end=round(points[i+1][0]*24) if i+1<len(points) else TOTAL
 assert end>start
 shots.append({'index':i,'start_frame':start,'end_frame':end,'start':start/24,'end':end/24,'frames':end-start,'sheet':s,'cell':c,'crop':crops[str(s)]['cells'][c]})
(ROOT/'project/shots.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2))
print('SHOTS',len(shots),'FRAMES',TOTAL,flush=True)
def run(shot):
 i=shot['index'];p=TMP/f'shot-{i:03}.mp4';c=shot['crop']
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1','-framerate','24','-i',str(ROOT/f"project/assets/sheet-{shot['sheet']:02}.png"),'-vf',f"crop={c['width']}:{c['height']}:{c['x']}:{c['y']},scale=1280:720:flags=lanczos,setsar=1,format=yuv420p",'-frames:v',str(shot['frames']),'-c:v','libx264','-preset','veryfast','-tune','stillimage','-crf','18','-threads','1','-an',str(p)]
 subprocess.run(cmd,check=True)
 return i
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for i in pool.map(run,shots):
  if i%10==0:print('ENCODED',i,flush=True)
(TMP/'concat.txt').write_text(''.join(f"file '{TMP/f'shot-{s['index']:03}.mp4'}'\n" for s in shots))
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(TMP/'concat.txt'),'-c','copy',str(TMP/'silent.mp4')],check=True)
print('SILENT COMPLETE',flush=True)
# Normalize the user's audio without changing pace, then burn Vietnamese captions.
audio=ROOT/'audio-goc.mp3'
subfilter=f"subtitles={ROOT/'subtitles.srt'}:force_style='FontName=Noto Sans,FontSize=23,PrimaryColour=&H00FFFFFF,OutlineColour=&H00151515,BorderStyle=1,Outline=1.5,Shadow=0.4,MarginV=24'"
norm='loudnorm=I=-16:TP=-1.8:LRA=11:measured_I=-20.17:measured_TP=-0.45:measured_LRA=4.40:measured_thresh=-30.54:offset=0.39:linear=true'
cmd=['ffmpeg','-hide_banner','-y','-i',str(TMP/'silent.mp4'),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-vf',subfilter,'-af',norm,'-c:v','libx264','-preset','fast','-crf','22','-tune','stillimage','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-ar','48000','-movflags','+faststart','-t',str(TOTAL/24),str(ROOT/'Bo-khong-biet-noi-thuong-con.mp4')]
with (TMP/'final-encode.log').open('w') as log:subprocess.run(cmd,check=True,stderr=log,stdout=log)
print('FINAL COMPLETE',flush=True)
