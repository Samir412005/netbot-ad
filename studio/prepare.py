import asyncio,json,pathlib,subprocess,urllib.request,urllib.parse,wave
import numpy as np
import edge_tts
P=pathlib.Path(__file__).parent; U=P/'public';U.mkdir(exist_ok=True)
R=48000;N=48*R

def run(a):
 p=subprocess.run(a,check=True,capture_output=True,text=True);return p.stdout

def fetch(url,path):
 req=urllib.request.Request(url,headers={'User-Agent':'netbot-studio/2.0'})
 with urllib.request.urlopen(req,timeout=25) as r:path.write_bytes(r.read())
fetch('https://raw.githubusercontent.com/google/fonts/main/ofl/cairo/Cairo%5Bslnt,wght%5D.ttf',U/'Cairo.ttf')
background={'mode':'authored-css-mesh','pollinations_attempted':True}
try:
 prompt='cinematic abstract emerald glass ribbon flowing in black space volumetric light no text no symbols vertical studio photography'
 fetch('https://image.pollinations.ai/prompt/'+urllib.parse.quote(prompt)+'?width=1080&height=1920&nologo=true&seed=412005',U/'cinema.jpg')
 from PIL import Image
 im=Image.open(U/'cinema.jpg');im.verify();background={'mode':'pollinations','pollinations_attempted':True}
except Exception as e:
 print('POLLINATIONS_UNAVAILABLE',str(e),flush=True)
 (U/'cinema.jpg').unlink(missing_ok=True)
(U/'background.json').write_text(json.dumps(background))
segments=[(.6,5.8,'عروض الإنترنت؟ البداية أبسط.'),(6.5,16.6,'سمير نت بوت. اختار العرض المتاح من تلجرام.'),(17.5,26.7,'اربط هاتفك بالتطبيق المرافق. على شريحتك أنت، وبموافقتك.'),(27.5,38.6,'راجع الشريحة والتكلفة والطلب. توافق أو تلغي. النجاح حسب تأكيد المشغل.'),(39.5,47.6,'بلا أو تي بي. بعض العروض تحتاج تطبيق المشغل.')]
async def synth():
 for voice in ['ar-DZ-IsmaelNeural','ar-DZ-AminaNeural','ar-SA-HamedNeural']:
  try:
   for i,(start,end,text) in enumerate(segments):
    await asyncio.wait_for(edge_tts.Communicate(text,voice,rate='+0%').save(str(U/f'v{i}.mp3')),timeout=35)
   return voice
  except Exception as e:print('VOICE_RETRY',voice,str(e),flush=True)
 raise RuntimeError('Natural Arabic narration unavailable; no silent substitute for studio edition')
voice=asyncio.run(synth());speech=np.zeros(N,dtype=np.float32);duck=np.ones(N,dtype=np.float32)
actual=[]
for i,(start,end,text) in enumerate(segments):
 raw=U/f'v{i}.wav';run(['ffmpeg','-y','-i',str(U/f'v{i}.mp3'),'-ar',str(R),'-ac','1','-c:a','pcm_s16le',str(raw)])
 with wave.open(str(raw)) as w:x=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float32)/32768
 length=len(x)/R
 assert length<=end-start, f'Voice segment{i} too long:{length} >{end-start}; shorten copy, do not speed up'
 a=int(start*R);speech[a:a+len(x)]+=x
 lo=max(0,a-int(.18*R));hi=min(N,a+len(x)+int(.25*R));duck[lo:hi]=.23
 actual.append({'start':start,'duration':length,'text':text})
# Authored original ambient score: A minor/add9 progression, soft sub and gated arpeggio.
t=np.arange(N,dtype=np.float32)/R;music=np.zeros(N,dtype=np.float32)
for bar,root in enumerate([110,87.307,130.813,97.999]*2):
 a=bar*6*R;b=min(N,a+6*R);z=np.arange(b-a,dtype=np.float32)/R
 env=np.sin(np.pi*np.clip(z/6,0,1))**.7
 pad=sum(np.sin(2*np.pi*root*ratio*z+0.2*k) for k,ratio in enumerate([1,1.5,2,2.25]))/4
 music[a:b]+=pad*.075*env+np.sin(2*np.pi*root/2*z)*.035*env
for k in range(128):
 a=int(k*.375*R);b=min(N,a+int(.30*R));z=np.arange(b-a,dtype=np.float32)/R
 hz=[440,523.251,659.255,783.991,880,659.255,523.251,391.995][k%8]
 music[a:b]+=.023*np.sin(2*np.pi*hz*z)*np.exp(-z*15)
# Smooth sidechain/duck envelope (sampled speech intervals).
kernel=np.ones(4800,dtype=np.float32)/4800;duck=np.convolve(duck[::480],np.ones(10)/10,mode='same').repeat(480)[:N]
sfx=np.zeros(N,dtype=np.float32);rng=np.random.default_rng(412005)
for when in [0,6,17,27,39]:
 a=int(when*R);l=min(int(.65*R),N-a);z=np.arange(l)/R
 noise=rng.normal(0,1,l);noise=np.convolve(noise,np.ones(16)/16,mode='same')
 sfx[a:a+l]+=(noise*.10*np.sin(np.pi*z/.65)**2+np.sin(2*np.pi*(65*z-22*z*z))*.10*np.exp(-z*10))
for when in [10.7,14.5,21.5,31.5,35.5,42.3]:
 a=int(when*R);l=int(.075*R);z=np.arange(l)/R;sfx[a:a+l]+=.05*np.sin(2*np.pi*1600*z)*np.exp(-z*65)
mix=speech*.95+music*duck+sfx
mix=np.tanh(mix*1.25)*.90
stereo=np.stack([mix,mix+np.roll(music,350)*duck*.12],axis=1);stereo=np.clip(stereo,-.98,.98)
with wave.open(str(U/'mix.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(R);w.writeframes((stereo*32767).astype('<i2').tobytes())
meta={'voice':voice,'voice_mode':'edge-tts','rate':'+0%','speech':actual,'score':'original procedural numpy synthesis','ducking':True,'sfx':'original synthesized whoosh impact tick','background':background}
(U/'audio.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2));print('AUDIO_PROVENANCE',json.dumps(meta,ensure_ascii=False),flush=True)