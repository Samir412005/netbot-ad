import asyncio, json, math, os, pathlib, subprocess as sp, urllib.request, shutil
from PIL import Image, ImageDraw, ImageFont, ImageOps, features
import edge_tts
P=pathlib.Path(__file__).resolve().parent; O=P/'out'; O.mkdir(exist_ok=True)
W,H=1080,1920; BG='#0b1512'; PANEL='#14221d'; GREEN='#44e39b'; WHITE='#f4faf6'; MUTED='#b4c8bc'
BASE='https://samir-netbot-video-3n8e59jd000007agwak4t00004en1rq7a000000.salix-sites.comma.surf/'
def run(args):
 print('RUN', ' '.join(map(str,args)),flush=True); return sp.run(list(map(str,args)),check=True,capture_output=True,text=True)
def duration(p):
 return float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',p]).stdout.strip())
def get(url,path):
 with urllib.request.urlopen(url,timeout=45) as r: path.write_bytes(r.read())
font=P/'Amiri-Regular.ttf'; get('https://raw.githubusercontent.com/google/fonts/main/ofl/amiri/Amiri-Regular.ttf',font)
assert features.check('raqm'), 'Arabic text requires RAQM shaping'
for name in ['01-logo.png','02-bot.png','03-app.png']:
 try: get(BASE+'assets/'+name,P/name)
 except Exception as e:
  print('Asset download unavailable; use authored vector illustration',name,str(e)[:120],flush=True)
  art=Image.new('RGB',(1200,720),BG);ad=ImageDraw.Draw(art)
  ad.rounded_rectangle((350,170,850,550),radius=75,fill=PANEL,outline=GREEN,width=12)
  if name=='01-logo.png':
   ad.ellipse((450,300,505,355),fill=WHITE);ad.ellipse((695,300,750,355),fill=WHITE);ad.line((510,440,690,440),fill=GREEN,width=14);ad.line((600,90,600,170),fill=GREEN,width=12)
  else:
   ad.polygon([(600,230),(730,280),(710,420),(600,490),(490,420),(470,280)],outline=GREEN,width=10);ad.line((540,350,585,400,670,310),fill=WHITE,width=14)
  art.save(P/name)
def ft(n): return ImageFont.truetype(str(font),n)
def rtl(draw,text,y,size=52,color=WHITE,x=540,width=900):
 words=text.split(); lines=[]; line=''; f=ft(size)
 for word in words:
  candidate=(line+' '+word).strip()
  if draw.textlength(candidate,font=f,direction='rtl',language='ar')>width and line: lines.append(line);line=word
  else: line=candidate
 if line: lines.append(line)
 for line in lines:
  draw.text((x,y),line,font=f,fill=color,anchor='mt',direction='rtl',language='ar'); y+=int(size*1.55)
 return y
D=[9,10,10,10,9]
HEAD=['أبسط من كثرة الخطوات','بوت بسيط، اختيار واضح','على شريحتك أنت','راجع، ثم قرّر','تحكّمك يبقى عندك']
SUB=['عروض الإنترنت اليومية تحتاج خطوات متعدّدة','اختار العرض المتاح والمهيّأ','بوت تلجرام + تطبيق مرافق','موافقتك مطلوبة لكل عملية','حدود واضحة، بلا وعود زائدة']
CAP=['طريقة أوضح لطلب عروض الإنترنت','وجود الزر لا يعني أن الخدمة مفعّلة','تنفيذ حقيقي بموافقة صاحب الشريحة','إذا أكّد المشغّل التفعيل، توصلك النتيجة','ليس تفعيلًا تلقائيًا كاملًا لأي عرض']
SPEECH=[
'كل يوم، عروض الإنترنت تحتاج خطوات كثيرة. مع سمير نت بوت، تبدأ من بوت بسيط في تلجرام.',
'اختار العرض المتاح والمهيأ من القائمة. ستة أزرار واضحة، وما هو قريباً يبقى معلناً، وليس خدمة مفعلة.',
'اربط هاتفك بالتطبيق المرافق. التنفيذ الحقيقي يكون على شريحتك أنت، وليس على حساب شخص آخر.',
'قبل كل عملية، راجع الشريحة والتكلفة وطلب يو إس إس دي. توافق أو تلغي، والنجاح حسب تأكيد المشغل.',
'لا نطلب رمز تحقق، أو أو تي بي. بعض العروض تحتاج تطبيق المشغل. سمير نت بوت، وضوح أكثر وتحكم يبقى عندك.'
]
for i in range(5):
 im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
 for y in range(H):
  v=int(8*math.sin(math.pi*y/H)); d.line((0,y,W,y),fill=(11,21+v,18+v))
 d.rounded_rectangle((64,58,1016,122),radius=28,fill=PANEL,outline='#284739',width=2)
 d.text((540,68),'samir-netbot',font=ft(36),fill=GREEN,anchor='mt')
 rtl(d,['المشكلة والحل','القائمة','التطبيق المرافق','الموافقة والنتيجة','الأمان والحدود'][i],160,36,GREEN)
 y=rtl(d,HEAD[i],225,78); rtl(d,SUB[i],y+12,42,MUTED)
 d.rounded_rectangle((208,570,872,1530),radius=64,fill='#050b08',outline='#446253',width=5)
 d.rounded_rectangle((230,592,850,1508),radius=48,fill=PANEL)
 d.rounded_rectangle((440,609,640,632),radius=12,fill='#050b08')
 if i==0:
  art=Image.open(P/'01-logo.png').convert('RGB'); art=ImageOps.fit(art,(570,330)); im.paste(art,(255,710))
  rtl(d,'شريحتك. موافقتك.',1100,49,GREEN,width=540)
  rtl(d,'طلب من البوت ثم تنفيذ على الهاتف',1215,43,width=520)
 elif i==1:
  rtl(d,'اختار من القائمة',680,44,GREEN,width=530)
  names=['هدية يومية','كم هو رصيدي','عروض الإنترنت','عروض خاصة','تقنية 5G','سناب شات']
  for k,name in enumerate(names):
   col=k%2;row=k//2;x=246+(1-col)*296;y=790+row*176
   d.rounded_rectangle((x,y,x+280,y+158),radius=18,fill='#1b3026',outline='#37634d',width=2)
   rtl(d,name,y+30,34,x=x+140,width=264)
   if k>3: rtl(d,'قريباً — اهتمام فقط',y+94,24,MUTED,x=x+140,width=264)
  rtl(d,'الرصيد: نقاط البوت، لا رصيد المشغّل',1390,28,MUTED,width=550)
 elif i==2:
  art=Image.open(P/'03-app.png').convert('RGB'); art=ImageOps.fit(art,(570,350));im.paste(art,(255,720))
  rtl(d,'هاتفك مرتبط بالتطبيق',1130,43,GREEN,width=520)
  rtl(d,'التنفيذ على شريحتك فقط',1230,42,width=520)
  rtl(d,'بموافقتك لكل عملية',1335,40,MUTED,width=520)
 elif i==3:
  rtl(d,'موافقة على USSD',690,48,GREEN,width=540)
  for k,t in enumerate(['راجع الشريحة','راجع التكلفة','راجع الطلب قبل التنفيذ']):
   yy=820+k*116;d.rounded_rectangle((258,yy,822,yy+98),radius=18,outline='#37634d',width=2);rtl(d,t,yy+18,38,width=530)
  d.rounded_rectangle((260,1210,528,1314),radius=40,outline='#496456',width=2);rtl(d,'إلغاء',1224,40,x=394,width=230)
  d.rounded_rectangle((552,1210,820,1314),radius=40,fill=GREEN);rtl(d,'أوافق',1224,40,'#07140d',x=686,width=230)
  rtl(d,'النجاح حسب ردّ المشغّل',1390,35,GREEN,width=540)
 else:
  d.ellipse((444,694,636,886),outline=GREEN,width=6);d.line((490,788,528,825,593,749),fill=GREEN,width=12)
  for k,t in enumerate(['لا نطلب OTP','لا تحكّم في حسابات الآخرين','بعض العروض تحتاج تطبيق المشغّل']):
   yy=950+k*155;rtl(d,t,yy,39,GREEN if k==0 else WHITE,width=550)
 d.rounded_rectangle((72,1590,1008,1782),radius=28,fill=PANEL,outline='#284739',width=2)
 rtl(d,CAP[i],1615,44,WHITE,width=860)
 rtl(d,'واجهات توضيحية — ليس تسجيلاً لتفعيل حيّ',1820,28,MUTED)
 for k in range(5):d.rounded_rectangle((345+k*82,1872,405+k*82,1880),radius=4,fill=GREEN if k==i else '#30473b')
 im.save(O/f'scene-{i}.png')
# Voice generation is bounded; fallbacks are explicitly recorded.
mode=None;voice=None
async def say(text,name,path):
 await asyncio.wait_for(edge_tts.Communicate(text,name,rate='+0%').save(str(path)),timeout=25)
for candidate in ['ar-DZ-IsmaelNeural','ar-DZ-AminaNeural','ar-SA-HamedNeural']:
 try:
  asyncio.run(say(SPEECH[0],candidate,O/'raw-0.mp3')); assert duration(O/'raw-0.mp3')>1
  voice=candidate;mode='edge-tts';break
 except Exception as e: print('TTS candidate failed:',candidate,type(e).__name__,str(e)[:200],flush=True)
if mode:
 try:
  for i in range(1,5):asyncio.run(say(SPEECH[i],voice,O/f'raw-{i}.mp3'))
 except Exception as e:print('TTS incomplete; use consistent fallback',str(e)[:180]);mode=None
if not mode:
 try:
  for i,text in enumerate(SPEECH):run(['espeak-ng','-v','ar','-s','145','-w',O/f'raw-{i}.wav',text])
  mode='espeak-ng';voice='ar'
 except Exception as e: print('Arabic speech fallback unavailable:',str(e)[:200]);mode='original-ambient-tones';voice=None
for i,dur in enumerate(D):
 if mode=='original-ambient-tones':
  run(['ffmpeg','-y','-f','lavfi','-i',f'sine=frequency=220:sample_rate=48000:duration={dur}','-af','volume=0.10,afade=t=in:d=1,afade=t=out:st='+str(dur-1)+':d=1','-ac','2',O/f'audio-{i}.wav'])
 else:
  raw=O/f'raw-{i}.mp3' if mode=='edge-tts' else O/f'raw-{i}.wav';length=duration(raw);tempo=max(0.9,length/(dur-0.6))
  run(['ffmpeg','-y','-i',raw,'-af',f'atempo={tempo:.6f},apad,atrim=duration={dur},afade=t=in:d=0.05,afade=t=out:st={dur-0.2}:d=0.2','-ar','48000','-ac','2',O/f'audio-{i}.wav'])
 vf=f"zoompan=z='1+0.000035*on':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={dur*30}:s=1080x1920:fps=30,fade=t=in:st=0:d=0.3,fade=t=out:st={dur-0.3}:d=0.3"
 run(['ffmpeg','-y','-i',O/f'scene-{i}.png','-i',O/f'audio-{i}.wav','-vf',vf,'-t',dur,'-r','30','-c:v','libx264','-threads','2','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart',O/f'clip-{i}.mp4'])
(O/'concat.txt').write_text('\n'.join("file 'clip-%s.mp4'"%i for i in range(5)))
final=O/'netbot-ad-48s.mp4'
run(['ffmpeg','-y','-f','concat','-safe','0','-i',O/'concat.txt','-c','copy','-movflags','+faststart',final])
probe=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',final]).stdout)
print('FFPROBE_VERIFICATION_JSON\n'+json.dumps(probe,ensure_ascii=False,indent=2),flush=True)
(O/'ffprobe.json').write_text(json.dumps(probe,ensure_ascii=False,indent=2))
a=[s for s in probe['streams'] if s['codec_type']=='audio'];v=[s for s in probe['streams'] if s['codec_type']=='video'];length=float(probe['format']['duration'])
assert 45<=length<=50 and a and a[0]['codec_name']=='aac' and v[0]['codec_name']=='h264'
assert v[0]['width']==1080 and v[0]['height']==1920
vol=run(['ffmpeg','-i',final,'-vn','-af','volumedetect','-f','null','-']).stderr
print('AUDIO_LEVEL_VERIFICATION\n'+vol[-3000:],flush=True)
import re
mean=float(re.search(r'mean_volume: ([\-\d.]+) dB',vol).group(1));assert mean>-60,'Silent audio rejected'
validation={'duration_seconds':length,'video_codec':'h264','audio_codec':'aac','width':1080,'height':1920,'audio_present':True,'mean_volume_db':mean,'voice_mode':mode,'voice':voice,'scene_count':5,'conceptual_ui':True}
(O/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2))
print('VALIDATED_VIDEO '+json.dumps(validation),flush=True)
# Contact sheet and poster prove the current rendered assets, not a mockup screenshot.
sheet=Image.new('RGB',(1080,960),BG)
for i in range(5):sheet.paste(Image.open(O/f'scene-{i}.png').resize((216,384)),(216*i,260))
sheet.save(O/'contact-sheet.jpg',quality=90);shutil.copy(O/'scene-0.png',O/'poster.png')
