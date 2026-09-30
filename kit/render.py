#!/usr/bin/env python3
"""Fluxr daily poster renderer.

Usage:  python3 render.py config.json out.png
Run from the kit folder (it loads logos/ relative to this file).
Renders a 1080x1350 (4:5) poster with real logos, drawn in HTML/CSS
and screenshotted with Playwright's Chromium. No network needed.

config.json keys (all strings unless noted):
  country        e.g. "Zimbabwe"
  flag           flag emoji of the destination, e.g. "🇿🇼"
  networks       list of logo file names in logos/, e.g. ["econet.png","netone.png","telecel.png"]
  pill           short tag in the lime pill, e.g. "No app needed"
  headline       big white headline, keep it under ~16 characters per line; use \n for a 2nd line
  sub            one line under the headline, e.g. "Airtime or data to Zimbabwe in seconds."
  code           dial code shown in the lime bar. Default "*130*31026#".
                 Long form sometimes: "*130*31026*voucher*263Number#"
  code_label     text above the bar. Default "Buy a voucher, dial and follow the menu:"
  networks_label text above the network logos. Default "Works on"
  theme          "mint" (default) or "sunset" or "sky" - background of the top area
"""
import json, sys, pathlib, html

KIT = pathlib.Path(__file__).resolve().parent

THEMES = {
    "mint":   ("#F3FCEF", "#DDF7D2", "#C4EFB3"),
    "sunset": ("#FFF6EA", "#FFE3C2", "#FFD09A"),
    "sky":    ("#EEF7FF", "#D6ECFF", "#BCDDFB"),
}

ICON_MAIL = '<svg viewBox="0 0 24 24" width="24" height="24"><path fill="#fff" d="M3 6.5A1.5 1.5 0 0 1 4.5 5h15A1.5 1.5 0 0 1 21 6.5v11a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 17.5v-11Zm2 .9V17h14V7.4l-7 5.1-7-5.1Zm1.6-.4L12 11l5.4-4H6.6Z"/></svg>'
ICON_WEB = '<svg viewBox="0 0 24 24" width="24" height="24"><path fill="#fff" d="M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18Zm6.9 8h-3a14 14 0 0 0-1.3-5.4A7 7 0 0 1 18.9 11ZM12 5.1c.9 1.2 1.7 3.3 1.9 5.9h-3.8c.2-2.6 1-4.7 1.9-5.9ZM9.4 5.6A14 14 0 0 0 8.1 11h-3a7 7 0 0 1 4.3-5.4ZM5.1 13h3a14 14 0 0 0 1.3 5.4A7 7 0 0 1 5.1 13Zm6.9 5.9c-.9-1.2-1.7-3.3-1.9-5.9h3.8c-.2 2.6-1 4.7-1.9 5.9Zm2.6-.5a14 14 0 0 0 1.3-5.4h3a7 7 0 0 1-4.3 5.4Z"/></svg>'
ICON_WA = '<svg viewBox="0 0 24 24" width="26" height="26"><path fill="#fff" d="M12 2.2a9.7 9.7 0 0 0-8.4 14.6L2.3 21.7l5-1.3A9.7 9.7 0 1 0 12 2.2Zm0 17.6c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A7.9 7.9 0 1 1 12 19.8Zm4.4-5.9c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8 1c-.1.2-.3.2-.5.1a6.5 6.5 0 0 1-3.2-2.8c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5c-.2 0-.4.1-.6.3-.2.2-.8.8-.8 2s.9 2.3 1 2.5c.1.2 1.7 2.6 4.2 3.7 1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.1.2-.6.2-1 .1-1.1l-.5-.3Z"/></svg>'
ICON_CALL = '<svg viewBox="0 0 24 24" width="34" height="34"><path fill="#fff" d="M6.6 10.8a15.2 15.2 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2Z"/></svg>'

VOUCHERS = ["1voucher.png", "ott-voucher.png", "blu-voucher.png", "fnb-voucher.png"]


def build_html(cfg):
    e = lambda s: html.escape(str(s))
    theme = THEMES.get(cfg.get("theme", "mint"), THEMES["mint"])
    code = cfg.get("code", "*130*31026#")
    code_len = len(code)
    code_size = 66 if code_len <= 14 else (46 if code_len <= 26 else 38)
    headline = e(cfg["headline"]).replace("\\n", "<br>").replace("\n", "<br>")
    two_line = "<br>" in headline
    nets = "".join(f'<div class="net"><img src="logos/{e(n)}"></div>' for n in cfg.get("networks", []))
    vouchers = "".join(f'<div class="tile"><img src="logos/{v}"></div>' for v in VOUCHERS)
    keys = [("1", ""), ("2", "ABC"), ("3", "DEF"), ("4", "GHI"), ("5", "JKL"), ("6", "MNO"),
            ("7", "PQRS"), ("8", "TUV"), ("9", "WXYZ"), ("*", ""), ("0", "+"), ("#", "")]
    keypad = "".join(f'<div class="key"><b>{k}</b><i>{s}</i></div>' for k, s in keys)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;font-family:Poppins,'Noto Color Emoji',sans-serif;-webkit-font-smoothing:antialiased}}
.poster{{position:relative;width:1080px;height:1350px;overflow:hidden;background:#0D372B}}
.hero{{position:absolute;left:0;top:0;width:1080px;height:730px;
  background:radial-gradient(900px 600px at 80% 20%, {theme[0]} 0%, {theme[1]} 55%, {theme[2]} 100%)}}
.ring{{position:absolute;border-radius:50%;border:2px solid rgba(13,55,43,.08)}}
.blob{{position:absolute;border-radius:50%;background:#85ED70;opacity:.28;filter:blur(2px)}}
.logo{{position:absolute;left:52px;top:46px;height:66px}}
.phone{{position:absolute;left:96px;top:132px;width:344px;height:700px;border-radius:54px;background:#101512;
  padding:13px;transform:rotate(-6deg);box-shadow:0 40px 70px rgba(13,55,43,.35), inset 0 0 0 2px #2b332f}}
.screen{{width:100%;height:100%;border-radius:42px;background:#fff;overflow:hidden;position:relative}}
.notch{{position:absolute;left:50%;top:12px;width:96px;height:26px;margin-left:-48px;border-radius:14px;background:#101512}}
.status{{position:absolute;top:16px;left:28px;right:26px;display:flex;justify-content:space-between;font-size:15px;font-weight:600;color:#111}}
.dialed{{position:absolute;top:92px;left:0;right:0;text-align:center;font-size:37px;font-weight:600;color:#111;letter-spacing:.5px}}
.dialsub{{position:absolute;top:142px;left:0;right:0;text-align:center;font-size:15px;color:#2E9E4F;font-weight:500}}
.keypad{{position:absolute;top:186px;left:34px;right:34px;display:grid;grid-template-columns:repeat(3,1fr);row-gap:14px;column-gap:18px}}
.key{{height:70px;border-radius:50%;width:70px;margin:0 auto;background:#EEF1EF;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.key b{{font-size:28px;font-weight:500;color:#111;line-height:1}} .key i{{font-style:normal;font-size:9px;letter-spacing:1.5px;color:#555;height:10px}}
.call{{position:absolute;top:534px;left:50%;margin-left:-38px;width:76px;height:76px;border-radius:50%;background:#34C759;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 18px rgba(52,199,89,.45)}}
.flagwrap{{position:absolute;left:688px;top:100px;width:236px;height:236px;border-radius:50%;background:#fff;
  box-shadow:0 24px 50px rgba(13,55,43,.22);display:flex;align-items:center;justify-content:center;font-size:150px;line-height:1}}
.flagwrap span{{transform:translateY(6px)}}
.route{{position:absolute;left:536px;top:362px;height:62px;padding:0 26px;border-radius:31px;background:#0D372B;color:#fff;
  display:flex;align-items:center;gap:12px;font-size:25px;font-weight:600;white-space:nowrap}}
.route .arrow{{color:#85ED70;font-weight:700}}
.nets{{position:absolute;left:536px;top:444px;width:488px;padding:18px 22px 20px;border-radius:26px;background:#fff;box-shadow:0 20px 44px rgba(13,55,43,.16)}}
.nets h4{{font-size:19px;font-weight:600;color:#0D372B;opacity:.7;margin-bottom:10px;letter-spacing:.3px}}
.netrow{{display:flex;gap:14px;align-items:center;justify-content:space-between}}
.net{{flex:1;height:66px;display:flex;align-items:center;justify-content:center}}
.net img{{max-height:64px;max-width:142px;object-fit:contain}}
.dash{{position:absolute;left:380px;top:104px}}
.wave{{position:absolute;left:0;top:628px;width:1080px;height:110px}}
.panel{{position:absolute;left:0;top:730px;width:1080px;height:520px;background:#0D372B}}
.content{{position:absolute;left:56px;right:56px;bottom:146px}}
.pill{{display:inline-block;height:50px;line-height:50px;padding:0 26px;border-radius:25px;background:#85ED70;color:#0D372B;font-size:25px;font-weight:600}}
h1{{margin-top:12px;color:#fff;font-weight:700;font-size:{72 if two_line else 84}px;line-height:1.02;letter-spacing:-1.5px}}
.sub{{margin-top:{6 if two_line else 10}px;color:#D9F7CF;font-size:31px;font-weight:500;letter-spacing:-.3px}}
.lbl{{margin-top:{12 if two_line else 20}px;color:#fff;opacity:.85;font-size:24px;font-weight:500}}
.bar{{margin-top:10px;height:94px;border-radius:24px;background:#85ED70;display:flex;align-items:center;justify-content:center;
  color:#0D372B;font-size:{code_size}px;font-weight:700;letter-spacing:1px;box-shadow:0 10px 30px rgba(133,237,112,.25)}}
.tiles{{margin-top:18px;display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}
.tile{{height:82px;border-radius:18px;background:#fff;display:flex;align-items:center;justify-content:center}}
.tile img{{max-height:50px;max-width:188px;object-fit:contain}}
.footer{{position:absolute;left:0;bottom:0;width:1080px;height:116px;background:#fff;display:flex;align-items:center;padding:0 44px;gap:22px}}
.footer .flogo{{height:50px}}
.div{{width:2px;height:54px;background:rgba(13,55,43,.18)}}
.fitems{{flex:1;display:flex;justify-content:space-between;align-items:center}}
.fi{{display:flex;align-items:center;gap:10px;color:#0D372B;font-size:22px;font-weight:600;white-space:nowrap}}
.ic{{width:44px;height:44px;border-radius:50%;background:#0D372B;display:flex;align-items:center;justify-content:center}}
.ic.wa{{background:#25D366}}
.checks{{display:flex;justify-content:space-between;padding:8px 4px}} .checks span{{font-size:25px;font-weight:600;color:#0D372B;white-space:nowrap}}
</style></head><body><div class="poster">
<div class="hero">
  <div class="ring" style="left:-160px;top:220px;width:760px;height:760px"></div>
  <div class="ring" style="left:-60px;top:320px;width:560px;height:560px"></div>
  <div class="blob" style="left:860px;top:-80px;width:300px;height:300px"></div>
  <div class="blob" style="left:470px;top:600px;width:180px;height:180px;opacity:.2"></div>
  <img class="logo" src="logos/fluxr-green.png">
  <svg class="dash" width="330" height="160" viewBox="0 0 330 160"><path d="M10 150 C 90 30, 210 10, 300 60" fill="none" stroke="#0D372B" stroke-opacity=".35" stroke-width="4" stroke-dasharray="4 14" stroke-linecap="round"/>
    <path d="M300 60 l-22 -4 m22 4 l-10 20" stroke="#0D372B" stroke-opacity=".45" stroke-width="4" stroke-linecap="round" fill="none"/></svg>
  <div class="phone"><div class="screen"><div class="notch"></div>
    <div class="status"><span>09:41</span><span>●●● 5G</span></div>
    <div class="dialed">{e(code if len(code) <= 14 else "*130*31026#")}</div>
    <div class="dialsub">Fluxr · any phone, no app</div>
    <div class="keypad">{keypad}</div>
    <div class="call">{ICON_CALL}</div>
  </div></div>
  <div class="flagwrap"><span>{e(cfg['flag'])}</span></div>
  <div class="route"><span>🇿🇦 South Africa</span><span class="arrow">→</span><span>{e(cfg['flag'])} {e(cfg['country'])}</span></div>
  {f'<div class="nets"><h4>{e(cfg.get("networks_label", "Works on"))}</h4><div class="netrow">{nets}</div></div>' if nets else '<div class="nets"><div class="checks"><span>✓ Any phone</span><span>✓ No app</span><span>✓ No data</span></div></div>'}
</div>
<svg class="wave" viewBox="0 0 1080 110" preserveAspectRatio="none"><path d="M0 60 C 240 -10, 520 10, 760 44 C 900 64, 1000 58, 1080 30 L1080 110 L0 110 Z" fill="#0D372B"/></svg>
<div class="panel"></div>
<div class="content">
  <div class="pill">{e(cfg['pill'])}</div>
  <h1>{headline}</h1>
  <div class="sub">{e(cfg['sub'])}</div>
  <div class="lbl">{e(cfg.get('code_label', 'Buy a voucher, dial and follow the menu:'))}</div>
  <div class="bar">{e(code)}</div>
  <div class="tiles">{vouchers}</div>
</div>
<div class="footer">
  <img class="flogo" src="logos/fluxr-green.png"><div class="div"></div>
  <div class="fitems">
    <div class="fi"><div class="ic">{ICON_MAIL}</div>info@fluxr.co.za</div>
    <div class="fi"><div class="ic">{ICON_WEB}</div>www.fluxr.co.za</div>
    <div class="fi"><div class="ic wa">{ICON_WA}</div>+27 60 636 0061</div>
  </div>
</div>
</div></body></html>"""


def main():
    cfg = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = pathlib.Path(sys.argv[2]).resolve()
    page_path = KIT / "_poster.html"
    page_path.write_text(build_html(cfg), encoding="utf-8")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        pg.goto(page_path.as_uri())
        pg.wait_for_load_state("networkidle")
        pg.evaluate("document.fonts.ready")
        # report any overflow so the caller can shorten text
        issues = pg.evaluate("""() => {
          const r=[]; const W=1080;
          for (const el of document.querySelectorAll('h1,.sub,.lbl,.bar,.route,.fi,.pill,.nets')) {
            const b=el.getBoundingClientRect(); if (b.right>W-40 || el.scrollWidth>el.clientWidth+1) r.push(el.className||el.tagName);
          }
          const c=document.querySelector('.tiles').getBoundingClientRect(); if (c.bottom>1350-116-8) r.push('content too tall: '+Math.round(c.bottom));
          const imgs=[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src); if (imgs.length) r.push('missing images: '+imgs.join(','));
          return r; }""")
        pg.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
        b.close()
    print("saved", out)
    print("LAYOUT ISSUES:", issues if issues else "none")


if __name__ == "__main__":
    main()
