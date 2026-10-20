import json,pathlib,subprocess,hashlib,shutil,os
from PIL import Image,ImageDraw
P=pathlib.Path(__file__).parent;O=P/'out';O.mkdir(exist_ok=True)

def run(a):
 p=subprocess.run(a,capture_output=True,text=True)
 if p.returncode: print(p.stderr);p.check_returncode()
 return p.stdout,p.stderr
checks=[];times=[2,5.7,6.7,10.8,16.7,18,21.5,26.7,28,35.8,40.3,45.8]
for variant in ['A','B']:
 video=O/f'netbot-studio-{variant}.mp4'
 # Stream-copy remux to guarantee faststart, keeping Remotion picture and 192k AAC.
 temp=O/f'temp-{variant}.mp4';run(['ffmpeg','-y','-i',str(video),'-c','copy','-movflags','+faststart',str(temp)]);temp.replace(video)
 text,_=run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(video)]);probe=json.loads(text)
 print('FFPROBE_STUDIO_'+variant,text,flush=True);(O/f'ffprobe-{variant}.json').write_text(text)
 v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio');duration=float(probe['format']['duration'])
 assert 45<=duration<=50 and v['width']==1080 and v['height']==1920
 assert v['r_frame_rate']=='60/1' and v['codec_name']=='h264' and v['profile']=='High' and a['codec_name']=='aac'
 _,vol=run(['ffmpeg','-i',str(video),'-vn','-af','volumedetect','-f','null','-']);print('AUDIO_LEVEL_'+variant,vol[-2000:],flush=True)
 import re
 mean=float(re.findall(r'mean_volume: ([-\d.]+)',vol)[-1]);assert mean>-45
 frames=O/f'frames-{variant}';frames.mkdir(exist_ok=True)
 sheet=Image.new('RGB',(1080,2688),'#101713');d=ImageDraw.Draw(sheet)
 for i,t in enumerate(times):
  frame=frames/f'frame-{i+1:02}.jpg';run(['ffmpeg','-y','-ss',str(t),'-i',str(video),'-frames:v','1','-q:v','2',str(frame)])
  im=Image.open(frame);im.thumbnail((350,622));x=(i%3)*360+5;y=(i//3)*672+34;sheet.paste(im,(x,y));d.text((x+10,y-25),f'{variant} | {i+1:02} | {t:.1f}s',fill='white')
  # Separate cropped real UI evidence permits text-level inspection at native detail.
  if i in [3,6,9,11]:Image.open(frame).crop((190,530,890,1630)).save(frames/f'ui-{i+1:02}.jpg',quality=94)
 sheet.save(O/f'contact-{variant}.jpg',quality=94)
 shutil.copy(frames/'frame-12.jpg',O/f'cover-{variant}.jpg')
 checks.append({'variant':variant,'duration':duration,'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'video_codec':v['codec_name'],'profile':v['profile'],'video_bitrate':v.get('bit_rate'),'audio_codec':a['codec_name'],'audio_bitrate':a.get('bit_rate'),'mean_volume_db':mean,'bytes':video.stat().st_size,'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'review_frames':12,'visual_review':'pending human/agent vision review, not claimed by automated check'})
(O/'validation.json').write_text(json.dumps({'engine':'Remotion React + Chromium','videos':checks,'audio':json.loads((P/'public/audio.json').read_text()),'frame_times_seconds':times},ensure_ascii=False,indent=2))
print('VALIDATED_STUDIO',json.dumps(checks),flush=True)
shutil.make_archive(str(O/'review-frames'),'zip',O,base_dir='frames-A')
# Bundle all24 native frames,8 UI crops and both sheets in one editable evidence archive.
import zipfile
with zipfile.ZipFile(O/'all-review-frames.zip','w',zipfile.ZIP_DEFLATED) as z:
 for variant in ['A','B']:
  for file in (O/f'frames-{variant}').glob('*.jpg'):z.write(file,file.relative_to(O))
  z.write(O/f'contact-{variant}.jpg',f'contact-{variant}.jpg')