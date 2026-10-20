import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Audio,Composition,Img,continueRender,delayRender,interpolate,interpolateColors,registerRoot,spring,staticFile,useCurrentFrame} from 'remotion';
import {Phone,Bot} from './Phone';
import background from './public/background.json';
const T=[0,360,1020,1620,2340,2880];
const mix=(f:number,range:number[],out:number[])=>interpolate(f,range,out,{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
const clamp=(x:number)=>Math.max(0,Math.min(1,x));
const Head=({lines,local,color,accent}:{lines:string[],local:number,color:string,accent:string})=><div data-safe="heading" style={{position:'absolute',top:202,left:78,right:78,direction:'rtl',textAlign:'center',fontWeight:800,fontSize:87,lineHeight:1.43,color}}>{lines.map((s,i)=>{const p=spring({frame:local-8-i*13,fps:60,config:{damping:22,stiffness:125}});return <div key={s} style={{clipPath:`inset(0 0 ${(1-p)*100}% 0)`,transform:`translateY(${(1-p)*65}px)`,color:i===lines.length-1?accent:color,opacity:clamp(p)}}>{s}</div>})}</div>;
const Film=({variant='A'}:{variant?:string})=>{
 const [fontHandle]=useState(()=>delayRender('Cairo Arabic font'));useEffect(()=>{document.fonts.load('800 87px Cairo').then(()=>document.fonts.ready).then(()=>continueRender(fontHandle));},[fontHandle]);
 const f=useCurrentFrame(),b=variant==='B';const phase=f<360?0:f<1020?1:f<1620?2:f<2340?3:4;const local=f-T[phase];
 const light=!b&&[0,2,4].includes(phase);const ink=light?'#1d1d1f':'#f2fff8',sub=light?'#4c6358':'#abc4b5',accent=light?'#16794e':'#51edab';
 const sceneIn=spring({frame:local,fps:60,config:{damping:24,stiffness:110}});
 const nearCut=Math.min(...T.slice(1,-1).map(t=>Math.abs(f-t)));const flash=b?clamp(1-nearCut/13)*.26:clamp(1-nearCut/18)*.11;
 const ry=mix(f,[0,120,359,440,900,1020,1150,1500,1620,1760,2250,2340,2500,2879],b?[25,-12,6,-7,8,18,-6,7,-20,6,-4,14,-5,0]:[35,-12,-5,4,-5,16,-6,-3,-14,4,0,14,-5,0]);
 const rz=b?mix(f,[0,130,359,500,1020,1200,1620,1800,2340,2500,2879],[-18,8,-3,-7,9,-5,-9,5,8,-4,0]):Math.sin(f/380)*2;
 const px=b?Math.sin(f/270)*30:Math.sin(f/500)*14;
 const py=mix(f,[0,120,340,440,990,1120,1570,1720,2280,2460,2879],[800,606,582,570,570,575,580,565,565,570,560]);
 const scale=mix(f,[0,100,340,450,990,1120,1570,1720,2280,2460,2879],[.55,.88,.94,.97,.97,.94,.94,.96,.96,.90,.91]);
 const headings=[['خطوات كثيرة؟','خلّيها أبسط.'],['اختيار واضح.','من تلجرام.'],['على شريحتك','أنت.'],['راجع.','ثم قرّر.'],['وضوح أكثر.','وتحكّمك يبقى.']];
 const captions=[['بوت بسيط + تطبيق مرافق','بداية منظّمة لعروض الإنترنت'],['اختر عرضاً متاحاً ومهيّأً','5G وسناب شات: قريباً، غير مفعّلين'],['التنفيذ الحقيقي على هاتفك','وبموافقتك أنت'],['توافق أو تلغي قبل كل عملية','النجاح حسب تأكيد المشغّل'],['بلا OTP أو حسابات الآخرين','بعض العروض تحتاج تطبيق المشغّل']];
 const progress=f/2880;
 return <AbsoluteFill data-build="netbot-studio-v2" style={{background:light?'#f5f5f7':'#050c09',fontFamily:'Cairo',overflow:'hidden'}}>
 <style>{`@font-face{font-family:Cairo;src:url('${staticFile('Cairo.ttf')}') format('truetype');font-weight:200 1000}*{box-sizing:border-box}body{margin:0}`}</style>
 <Audio src={staticFile('mix.wav')} volume={1}/>
 {b&&background.mode==='pollinations'&&<Img src={staticFile('cinema.jpg')} style={{position:'absolute',inset:0,width:'100%',height:'100%',objectFit:'cover',opacity:.20,transform:`scale(${1.1+f/50000}) translateY(${Math.sin(f/600)*30}px)`}}/>}
 <AbsoluteFill style={{background:light?'radial-gradient(ellipse at 50% 70%,#d3e3db 0%,transparent 56%)':'radial-gradient(ellipse at 50% 63%,#174c3266 0%,transparent 60%)',transform:`translate(${Math.sin(f/180)*30}px,${Math.cos(f/260)*30}px)`}}/>
 {b&&<><AbsoluteFill style={{background:'radial-gradient(ellipse at 5% 35%,#00836b42,transparent 44%),radial-gradient(ellipse at 90% 82%,#076e9142,transparent 42%)'}}/>{[0,1,2].map(i=><div key={i} style={{position:'absolute',left:-170+i*55,top:590+i*90,width:1420-i*100,height:550+i*40,borderRadius:'50%',border:`${i===0?3:1}px solid ${i===1?'#5bd6ff45':'#51edab45'}`,transform:`rotate(${-31+Math.sin(f/280+i)*13}deg) rotateX(${50+i*8}deg)`,boxShadow:i===0?'0 0 35px #51edab15':'none'}}/>)}{Array.from({length:30},(_,i)=><div key={i} style={{position:'absolute',width:i%4===0?4:2,height:i%4===0?4:2,borderRadius:10,background:i%3===0?'#72e9ff':'#79e6b1',opacity:.15+(i%5)*.07,left:(i*157+Math.sin(f/110+i)*32)%1080,top:(i*97-f*(.08+i%3*.04)+3840)%1920}}/>)}<div style={{position:'absolute',width:1800,height:2,background:'linear-gradient(90deg,transparent,#51edab90,transparent)',top:1600+Math.sin(f/150)*80,left:-300,transform:'rotate(-38deg)',boxShadow:'0 0 18px #51edab'}}/></>}
 {!b&&<><div style={{position:'absolute',width:1000,height:460,left:40,top:1480,borderRadius:'50%',background:light?'radial-gradient(ellipse,#45584d25,transparent 65%)':'radial-gradient(ellipse,#71ebb61a,transparent 65%)',transform:`scaleX(${.8+Math.sin(f/300)*.06})`}}/><div style={{position:'absolute',left:-350,top:1510,width:1800,height:480,borderRadius:'50%',borderTop:`1px solid ${light?'#bacbc0':'#38614b'}`,transform:`rotate(${-9+Math.sin(f/450)*4}deg)`}}/></>}
 <div style={{position:'absolute',left:78,top:95,right:78,display:'flex',alignItems:'center',justifyContent:'space-between',color:ink}}><div style={{display:'flex',alignItems:'center',gap:13}}><Bot size={47}/><span style={{fontSize:28,fontWeight:700,letterSpacing:1}}>samir-netbot</span></div><div style={{fontSize:21,letterSpacing:3,color:sub}}>BOT + APP</div></div>
 <Head key={phase} lines={headings[phase]} local={local} color={ink} accent={accent}/>
 <div style={{position:'absolute',left:78,right:78,top:488,textAlign:'center',fontSize:27,color:sub,direction:'rtl',opacity:mix(local,[28,65],[0,1]),transform:`translateY(${mix(local,[28,65],[12,0])}px)`}}>{['أقل تشتّتاً. أكثر وضوحاً.','واجهة بسيطة. قرار واعٍ.','ربط آمن بإذن صاحب الهاتف.','موافقة صريحة. في كل مرة.','سمير نت بوت'][phase]}</div>
 <div style={{position:'absolute',left:280+px,top:py,transformOrigin:'260px 500px',transform:`perspective(1600px) rotateY(${ry}deg) rotateX(${Math.sin(f/380)*3}deg) rotateZ(${rz}deg) scale(${scale})`}}><Phone phase={phase} neon={b}/></div>
 {phase===0&&local<220&&['تطبيق المشغّل','قوائم متفرّقة','خطوات يومية'].map((s,i)=>{const p=spring({frame:local-10-i*15,fps:60,config:{damping:20}});const exit=mix(local,[145,215],[0,1]);return <div key={s} style={{position:'absolute',left:i%2===0?72:650,top:680+i*220,padding:'17px 23px',width:350,background:light?'#fffffff0':'#1d392ef0',border:`1px solid ${light?'#d6ded8':'#416654'}`,borderRadius:20,fontSize:27,direction:'rtl',color:ink,opacity:clamp(p)*(1-exit),transform:`translate(${exit*(i%2===0?-260:260)}px,${(1-p)*45}px) rotate(${i%2===0?-7:7}deg)`,boxShadow:'0 16px 45px #0001'}}>{s}</div>})}
 {phase===3&&<div style={{position:'absolute',left:735,top:1325,width:100,height:100,borderRadius:'50%',border:'2px solid #51edab',opacity:clamp(1-Math.abs(f-1900)/70),transform:`scale(${mix(f,[1830,1970],[.2,2])})`}}/>}
 <div data-safe="captions" style={{position:'absolute',top:1660,left:78,right:78,textAlign:'center',direction:'rtl',fontSize:33,fontWeight:600,lineHeight:1.8,color:ink,opacity:mix(local,[20,45],[0,1])}}>{captions[phase][0]}<div style={{fontSize:27,color:sub,fontWeight:400}}>{captions[phase][1]}</div></div>
 <div style={{position:'absolute',top:1810,left:78,right:78,display:'flex',justifyContent:'space-between',alignItems:'center',fontSize:21,color:sub,direction:'rtl'}}><span>واجهات توضيحية · ليست عملية تفعيل فعلية</span><span style={{fontFamily:'Arial',fontSize:19}}>0{phase+1} / 05</span></div>
 <div style={{position:'absolute',left:78,bottom:62,width:924,height:3,background:light?'#d7e3da':'#294637'}}><div style={{width:`${progress*100}%`,height:3,background:accent}}/></div>
 <AbsoluteFill style={{pointerEvents:'none',opacity:flash,background:b?'linear-gradient(100deg,#8cf7da,#75a6ff)':'#ffffff',mixBlendMode:'screen'}}/>
 {b&&nearCut<12&&<AbsoluteFill style={{pointerEvents:'none',borderLeft:'9px solid #ec497b',borderRight:'9px solid #55e8ff',opacity:clamp(1-nearCut/12),transform:`translateX(${Math.sin(f*3)*7}px)`}}/>}
 </AbsoluteFill>;
};
const Root=()=> <>{['A','B'].map(variant=><Composition key={variant} id={`Studio${variant}`} component={Film} durationInFrames={2880} fps={60} width={1080} height={1920} defaultProps={{variant}}/>)}</>;
registerRoot(Root);