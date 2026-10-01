#!/usr/bin/env python3
"""Fluxr short video renderer (YouTube Shorts / TikTok / Reels).

Usage:  python3 video.py config.json out.mp4 [--music] [--voice]
Renders an 18-second 1080x1920 (9:16) animated video, drawn in HTML/CSS and
captured frame by frame with Playwright's Chromium, then encoded with ffmpeg.
Without --music the video is silent (voiceover + music are added later in an
ElevenLabs "composition" node). With --music a quiet synthesized music bed and
soft key clicks are mixed in locally (fallback when ElevenLabs is unavailable).
Add --voice when the video will get an ElevenLabs voiceover: the music bed is
mixed about 17 dB quieter and the key clicks are left out, so the music never
competes with the voice (user, 1 Oct 2026: the tones were overpowering the voice).

config.json uses the same keys as render.py (country, flag, networks, code, theme)
plus optional:
  duration    seconds (default 18). Set it to the voiceover length (rounded up) so the
              whole timeline stretches to fit the voice.
  hook        two short lines for the opening, e.g. "Sending love\\nto Mozambique?"
  cc          the country dialling code, e.g. "258" (shown in step 3)
  voucher_line  default "From R5 at your local store"

Voiceover script that matches the timeline (about 17 s, read at a natural pace):
  0-3 s   "<hook>"
  3-6 s   "Buy a 1Voucher, OTT, Blu or FNB Voucher."
  6-11 s  "Then dial star one three zero, star three one zero two six, star, your voucher PIN, hash."
  11-14 s "Follow the menu, enter their number, and airtime or data lands in seconds."
  14-18 s "Fluxr. No app, no data, any phone. WhatsApp us any time."
"""
import json, sys, pathlib, html, subprocess, math, wave, struct

KIT = pathlib.Path(__file__).resolve().parent
W, H, FPS, DUR = 1080, 1920, 30, 18.0
THEMES = {
    "mint":   ("#F3FCEF", "#DDF7D2", "#C4EFB3"),
    "sunset": ("#FFF6EA", "#FFE3C2", "#FFD09A"),
    "sky":    ("#EEF7FF", "#D6ECFF", "#BCDDFB"),
}
VOUCHERS = ["1voucher.png", "ott-voucher.png", "blu-voucher.png", "fnb-voucher.png"]
WA = '<svg viewBox="0 0 24 24" width="40" height="40"><path fill="#fff" d="M12 2.2a9.7 9.7 0 0 0-8.4 14.6L2.3 21.7l5-1.3A9.7 9.7 0 1 0 12 2.2Zm0 17.6c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A7.9 7.9 0 1 1 12 19.8Zm4.4-5.9c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8 1c-.1.2-.3.2-.5.1a6.5 6.5 0 0 1-3.2-2.8c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5c-.2 0-.4.1-.6.3-.2.2-.8.8-.8 2s.9 2.3 1 2.5c.1.2 1.7 2.6 4.2 3.7 1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.1.2-.6.2-1 .1-1.1l-.5-.3Z"/></svg>'
CALL = '<svg viewBox="0 0 24 24" width="54" height="54"><path fill="#fff" d="M6.6 10.8a15.2 15.2 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2Z"/></svg>'


def build_html(cfg):
    e = lambda s: html.escape(str(s))
    th = THEMES.get(cfg.get("theme", "mint"), THEMES["mint"])
    code = cfg.get("code", "*130*31026*voucher#")
    hook = e(cfg.get("hook", f"Sending love\nto {cfg['country']}?")).replace("\\n", "<br>").replace("\n", "<br>")
    keys = [("1", ""), ("2", "ABC"), ("3", "DEF"), ("4", "GHI"), ("5", "JKL"), ("6", "MNO"),
            ("7", "PQRS"), ("8", "TUV"), ("9", "WXYZ"), ("*", ""), ("0", "+"), ("#", "")]
    keypad = "".join(f'<div class="key" data-k="{k}"><b>{k}</b><i>{s}</i></div>' for k, s in keys)
    tiles = "".join(f'<div class="vt" id="vt{i}"><img src="logos/{v}"></div>' for i, v in enumerate(VOUCHERS))
    tiles_end = "".join(f'<div class="et"><img src="logos/{v}"></div>' for v in VOUCHERS)
    nets = "".join(f'<div class="net"><img src="logos/{e(n)}"></div>' for n in cfg.get("networks", []))
    netcard = (f'<div class="netcard" id="netcard"><h4>Works on</h4><div class="netrow">{nets}</div></div>' if nets else
               '<div class="netcard" id="netcard"><div class="checks"><span>✓ Any phone</span><span>✓ No app</span><span>✓ No data</span></div></div>')
    cc = e(cfg.get("cc", ""))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;font-family:Poppins,'Noto Color Emoji',sans-serif;-webkit-font-smoothing:antialiased}}
#stage{{position:absolute;inset:0;background:radial-gradient(1200px 1100px at 75% 18%, {th[0]} 0%, {th[1]} 55%, {th[2]} 100%);overflow:hidden}}
.abs{{position:absolute}}
.blob{{position:absolute;border-radius:50%;background:#85ED70;opacity:.25}}
#logo{{left:60px;top:70px;height:84px}}
.scene{{position:absolute;inset:0;opacity:0}}
/* scene 1 */
#flag{{left:50%;top:330px;width:420px;height:420px;margin-left:-210px;border-radius:50%;background:#fff;box-shadow:0 30px 70px rgba(13,55,43,.22);display:flex;align-items:center;justify-content:center;font-size:250px;line-height:1}}
#flag span{{transform:translateY(10px)}}
#hook{{left:70px;right:70px;top:860px;text-align:center;color:#0D372B;font-weight:700;font-size:104px;line-height:1.05;letter-spacing:-2px}}
#route{{left:50%;top:1240px;transform:translateX(-50%);height:84px;padding:0 36px;border-radius:42px;background:#0D372B;color:#fff;display:flex;align-items:center;gap:16px;font-size:36px;font-weight:600;white-space:nowrap}}
#route .ar{{color:#85ED70}}
/* scene 2 */
#s2t{{left:70px;right:70px;top:300px;text-align:center;color:#0D372B;font-weight:700;font-size:96px;letter-spacing:-2px;line-height:1.05}}
#s2s{{left:70px;right:70px;top:520px;text-align:center;color:#0D372B;opacity:.75;font-weight:500;font-size:40px}}
#vgrid{{left:90px;right:90px;top:680px;display:grid;grid-template-columns:1fr 1fr;gap:34px}}
.vt{{height:230px;border-radius:34px;background:#fff;box-shadow:0 18px 40px rgba(13,55,43,.14);display:flex;align-items:center;justify-content:center}}
.vt img{{max-width:330px;max-height:110px;object-fit:contain}}
/* scene 3 */
#s3t{{left:70px;right:70px;top:220px;text-align:center;color:#0D372B;font-weight:700;font-size:84px;letter-spacing:-1.5px}}
#phone{{left:50%;top:400px;width:620px;height:1260px;margin-left:-310px;border-radius:90px;background:#101512;padding:22px;box-shadow:0 50px 90px rgba(13,55,43,.35), inset 0 0 0 3px #2b332f}}
.screen{{width:100%;height:100%;border-radius:70px;background:#fff;position:relative;overflow:hidden}}
.notch{{position:absolute;left:50%;top:20px;width:170px;height:46px;margin-left:-85px;border-radius:24px;background:#101512}}
.status{{position:absolute;top:28px;left:52px;right:48px;display:flex;justify-content:space-between;font-size:26px;font-weight:600;color:#111}}
#dialed{{position:absolute;top:175px;left:10px;right:10px;text-align:center;font-size:44px;font-weight:600;color:#111;white-space:nowrap;min-height:70px}}
#dialed .pin{{background:#85ED70;color:#0D372B;border-radius:12px;padding:0 8px}}
#cursor{{display:inline-block;width:4px;height:48px;background:#2E9E4F;vertical-align:middle;margin-left:4px}}
.keypad{{position:absolute;top:330px;left:56px;right:56px;display:grid;grid-template-columns:repeat(3,1fr);row-gap:26px}}
.key{{width:130px;height:130px;margin:0 auto;border-radius:50%;background:#EEF1EF;display:flex;flex-direction:column;align-items:center;justify-content:center;transition:none}}
.key b{{font-size:52px;font-weight:500;color:#111;line-height:1}} .key i{{font-style:normal;font-size:16px;letter-spacing:2px;color:#555;height:18px}}
.key.on{{background:#85ED70}}
#call{{position:absolute;top:1000px;left:50%;width:140px;height:140px;margin-left:-70px;border-radius:50%;background:#34C759;display:flex;align-items:center;justify-content:center;box-shadow:0 12px 30px rgba(52,199,89,.45)}}
/* scene 4 */
#s4card{{left:80px;right:80px;top:330px;border-radius:48px;background:#fff;box-shadow:0 30px 70px rgba(13,55,43,.18);padding:70px 60px}}
.step{{display:flex;align-items:center;gap:30px;font-size:46px;font-weight:600;color:#0D372B;margin:0 0 46px}}
.step .n{{flex:0 0 84px;height:84px;border-radius:50%;background:#0D372B;color:#85ED70;display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:700}}
.step.done .n{{background:#2E9E4F;color:#fff}}
#bigok{{left:50%;top:1060px;transform:translateX(-50%);white-space:nowrap;height:120px;padding:0 50px;border-radius:60px;background:#0D372B;color:#fff;display:flex;align-items:center;gap:18px;font-size:50px;font-weight:700}}
#netcard{{position:absolute;left:80px;right:80px;top:1240px;padding:34px 40px;border-radius:40px;background:#fff;box-shadow:0 20px 50px rgba(13,55,43,.14)}}
#netcard h4{{font-size:30px;font-weight:600;color:#0D372B;opacity:.7;margin-bottom:16px}}
.netrow{{display:flex;justify-content:space-around;align-items:center}}
.net img{{max-height:100px;max-width:240px;object-fit:contain}}
.checks{{display:flex;justify-content:space-between}} .checks span{{font-size:40px;font-weight:600;color:#0D372B}}
/* scene 5 end card */
#end{{background:#0D372B}}
#endlogo{{left:50%;top:250px;height:150px;transform:translateX(-50%)}}
#endtag{{left:70px;right:70px;top:470px;text-align:center;color:#D9F7CF;font-size:44px;font-weight:500}}
#endlbl{{left:80px;right:80px;top:640px;text-align:center;color:#fff;font-size:40px;font-weight:500;opacity:.85}}
#endbar{{left:80px;right:80px;top:710px;height:150px;border-radius:40px;background:#85ED70;color:#0D372B;display:flex;align-items:center;justify-content:center;font-size:66px;font-weight:700;letter-spacing:1px}}
#endgrid{{left:80px;right:80px;top:920px;display:grid;grid-template-columns:1fr 1fr;gap:28px}}
.et{{height:150px;border-radius:30px;background:#fff;display:flex;align-items:center;justify-content:center}}
.et img{{max-width:300px;max-height:84px;object-fit:contain}}
#endwa{{left:50%;top:1330px;transform:translateX(-50%);white-space:nowrap;display:flex;align-items:center;gap:20px;color:#fff;font-size:54px;font-weight:700}}
#endwa .ic{{width:84px;height:84px;border-radius:50%;background:#25D366;display:flex;align-items:center;justify-content:center}}
#endweb{{left:0;right:0;top:1460px;text-align:center;color:#D9F7CF;font-size:42px;font-weight:600}}
</style></head><body><div id="stage">
<div class="blob" style="left:760px;top:-140px;width:460px;height:460px"></div>
<div class="blob" style="left:-120px;top:1500px;width:380px;height:380px;opacity:.18"></div>
<img id="logo" class="abs" src="logos/fluxr-green.png">

<div class="scene" id="s1">
  <div id="flag" class="abs"><span>{e(cfg['flag'])}</span></div>
  <div id="hook" class="abs">{hook}</div>
  <div id="route" class="abs"><span>South Africa</span><span class="ar">→</span><span>{e(cfg['country'])}</span></div>
</div>

<div class="scene" id="s2">
  <div id="s2t" class="abs">Buy a voucher</div>
  <div id="s2s" class="abs">{e(cfg.get('voucher_line', 'From R5 at your local store'))}</div>
  <div id="vgrid" class="abs">{tiles}</div>
</div>

<div class="scene" id="s3">
  <div id="s3t" class="abs">Then dial</div>
  <div id="phone" class="abs"><div class="screen"><div class="notch"></div>
    <div class="status"><span>09:41</span><span>●●● 5G</span></div>
    <div id="dialed"></div>
    <div class="keypad">{keypad}</div>
    <div id="call">{CALL}</div>
  </div></div>
</div>

<div class="scene" id="s4">
  <div id="s4card" class="abs">
    <div class="step done" id="st1"><div class="n">1</div><div>Buy a voucher</div></div>
    <div class="step done" id="st2"><div class="n">2</div><div>Dial {e(code)}</div></div>
    <div class="step" id="st3"><div class="n">3</div><div>Follow the menu, enter<br>their number{(' (' + cc + '…)') if cc else ''}</div></div>
  </div>
  <div id="bigok" class="abs">⚡ Airtime or data in seconds</div>
  {netcard}
</div>

<div class="scene" id="end">
  <img id="endlogo" class="abs" src="logos/fluxr-white.png">
  <div id="endtag" class="abs">No app. No data. Any phone.</div>
  <div id="endlbl" class="abs">Buy a voucher and dial</div>
  <div id="endbar" class="abs">{e(code)}</div>
  <div id="endgrid" class="abs">{tiles_end}</div>
  <div id="endwa" class="abs"><div class="ic">{WA}</div>+27 60 636 0061</div>
  <div id="endweb" class="abs">www.fluxr.co.za</div>
</div>
</div>
<script>
const CODE = {json.dumps(code)}; const DUR = {float(cfg.get('duration', 18))};
const cl=(x,a,b)=>Math.max(a,Math.min(b,x));
const p=(t,a,b)=>cl((t-a)/(b-a),0,1);
const eo=x=>1-Math.pow(1-x,3);
const eb=x=>{{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);}};
function show(id,t,a,b,fi=0.35,fo=0.35){{const el=document.getElementById(id);let o=Math.min(p(t,a,a+fi),1-p(t,b-fo,b));el.style.opacity=cl(o,0,1);el.style.visibility=o>0?'visible':'hidden';return o;}}
function setT(t0){{
  const t=t0*18/DUR;
  show('s1',t,0,3.2,0.2);
  const f=eb(p(t,0.1,0.7)); document.getElementById('flag').style.transform=`scale(${{f}})`;
  const h=eo(p(t,0.5,1.1)); const hk=document.getElementById('hook'); hk.style.opacity=h; hk.style.transform=`translateY(${{(1-h)*60}}px)`;
  const r=eo(p(t,1.2,1.7)); const ro=document.getElementById('route'); ro.style.opacity=r; ro.style.transform=`translateX(-50%) translateY(${{(1-r)*40}}px)`;
  show('s2',t,3.0,6.2);
  for(let i=0;i<4;i++){{const v=eb(p(t,3.4+i*0.45,3.9+i*0.45));const el=document.getElementById('vt'+i);el.style.opacity=cl(v,0,1);el.style.transform=`scale(${{0.6+0.4*v}})`;}}
  show('s3',t,6.0,11.4);
  const ph=eo(p(t,6.0,6.6)); document.getElementById('phone').style.transform=`translateY(${{(1-ph)*500}}px)`;
  // typing from 6.6 to 10.2
  const n=Math.floor(cl((t-6.6)/3.6,0,1)*CODE.length+0.0001);
  let typed=CODE.slice(0,n);
  let disp=typed.replace('voucher','<span class="pin">voucher</span>');
  if(typed.includes('v')&&!typed.includes('voucher')){{disp=typed.replace(/v[a-z]*$/,m=>'<span class="pin">'+m+'</span>');}}
  const blink=(Math.floor(t*2.5)%2===0)?'<span id="cursor"></span>':'';
  document.getElementById('dialed').innerHTML=disp+(t<10.4?blink:'');
  const last=typed.slice(-1);
  document.querySelectorAll('.key').forEach(k=>k.classList.toggle('on', t>6.6&&t<10.2&&k.dataset.k===last && ((t-6.6)/3.6*CODE.length)%1<0.7));
  const cp=p(t,10.3,10.9); document.getElementById('call').style.transform=`scale(${{1+0.18*Math.sin(cp*Math.PI)}})`;
  show('s4',t,11.2,14.4);
  const c4=eo(p(t,11.2,11.7)); document.getElementById('s4card').style.transform=`translateY(${{(1-c4)*80}}px)`;
  document.getElementById('st3').classList.toggle('done', t>12.4);
  const ok=eb(p(t,12.5,13.0)); const bo=document.getElementById('bigok'); bo.style.opacity=cl(ok,0,1); bo.style.transform=`translateX(-50%) scale(${{0.7+0.3*ok}})`;
  const nc=eo(p(t,12.9,13.4)); const ncel=document.getElementById('netcard'); ncel.style.opacity=nc; ncel.style.transform=`translateY(${{(1-nc)*60}}px)`;
  show('end',t,14.2,99,0.4);
  document.getElementById('logo').style.opacity=1-p(t,14.0,14.4);
  const eg=eo(p(t,14.6,15.2)); document.getElementById('endgrid').style.opacity=eg;
  const ew=eo(p(t,15.2,15.7)); document.getElementById('endwa').style.opacity=ew; document.getElementById('endweb').style.opacity=ew;
}}
setT(0);
</script></body></html>"""


def synth_music(path, dur=DUR, clicks=None, peak=0.35):
    """Quiet warm pad + soft plucks (C major-ish loop), 44.1 kHz stereo WAV."""
    import numpy as np
    sr = 44100
    t = np.arange(int(sr * dur)) / sr
    chords = [[261.63, 329.63, 392.0], [220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [196.0, 246.94, 293.66]]
    out = np.zeros_like(t)
    bar = 2.25
    for i in range(int(dur / bar) + 1):
        a, b = i * bar, min((i + 1) * bar, dur)
        m = (t >= a) & (t < b)
        env = np.clip((t[m] - a) / 0.4, 0, 1) * np.clip((b - t[m]) / 0.4, 0, 1)
        for f in chords[i % 4]:
            out[m] += 0.05 * env * (np.sin(2 * np.pi * f * t[m]) + 0.3 * np.sin(2 * np.pi * 2 * f * t[m]))
        for k, f in enumerate(chords[i % 4] + [chords[i % 4][0] * 2]):
            s = a + k * bar / 4
            mm = (t >= s) & (t < s + 0.6)
            out[mm] += 0.04 * np.exp(-(t[mm] - s) * 7) * np.sin(2 * np.pi * f * 2 * t[mm])
    for c in (clicks or []):
        mm = (t >= c) & (t < c + 0.04)
        out[mm] += 0.05 * np.exp(-(t[mm] - c) * 120) * np.sin(2 * np.pi * 1800 * t[mm])
    out *= np.clip(t / 0.8, 0, 1) * np.clip((dur - t) / 1.2, 0, 1)
    out = (out / max(1e-9, np.abs(out).max()) * peak * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(np.repeat(out[:, None], 2, axis=1).tobytes())


def main():
    cfg = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = pathlib.Path(sys.argv[2]).resolve()
    music = "--music" in sys.argv
    voice = "--voice" in sys.argv  # quiet bed under a voiceover, no clicks
    page = KIT / "_video.html"
    dur = float(cfg.get("duration", DUR))
    page.write_text(build_html(cfg), encoding="utf-8")
    silent = out.with_suffix(".silent.mp4") if music else out
    from playwright.sync_api import sync_playwright
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                           "-movflags", "+faststart", str(silent)], stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.goto(page.as_uri()); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
        missing = pg.evaluate("[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src)")
        if missing: print("MISSING IMAGES:", missing)
        for i in range(int(dur * FPS)):
            pg.evaluate(f"setT({i / FPS})")
            ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
        b.close()
    ff.stdin.close(); ff.wait()
    if music:
        code = cfg.get("code", "*130*31026*voucher#")
        k = dur / 18.0
        clicks = [(6.6 + i * 3.6 / len(code)) * k for i in range(len(code))] + [10.35 * k]
        wav = out.with_suffix(".wav")
        synth_music(wav, dur=dur, clicks=None if voice else clicks, peak=0.05 if voice else 0.35)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), "-i", str(wav), "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(out)], check=True)
        silent.unlink(); wav.unlink()
    page.unlink(missing_ok=True)
    print("saved", out)


if __name__ == "__main__":
    main()
