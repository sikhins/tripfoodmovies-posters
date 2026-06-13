#!/usr/bin/env python3
"""
Blank to Bold — Full automation bot.
Generates poster for given slot index and posts to Instagram via Zapier webhook.
Usage: python3 poster_bot.py <slot_index> <zapier_webhook_url>
slot_index: 0=8am 1=10am 2=12pm 3=2pm 4=5pm 5=8pm
"""

import json, datetime, base64, urllib.request, urllib.parse, sys, os
from playwright.sync_api import sync_playwright

TODAY  = datetime.date.today()
DAY    = TODAY.weekday()
TOKEN  = os.environ["GH_TOKEN"]
ZAPIER = os.environ["ZAPIER_WEBHOOK"]
REPO   = "sikhins/tripfoodmovies-posters"
LOGO   = "https://raw.githubusercontent.com/sikhins/tripfoodmovies-posters/main/assets/logo.png"

STORIES = [
    {"category":"LOGO STORY","tag":"Origin Drop","line1":"Nike Paid","line2":"$35.","highlight":"$35.","stat":"$35","caption":"The most recognised logo on earth was bought for $35. 🔴\n\nIn 1971, Phil Knight overheard Portland State student Carolyn Davidson say she couldn't afford an oil painting class. He hired her at $2 per hour.\n\nShe designed 5 logo options. Knight chose the Swoosh — reluctantly.\n\nHis exact words: \"I don't love it, but it will grow on me.\"\n\nShe billed $35 total. The company was still called Blue Ribbon Sports — not yet Nike.\n\nIn 1983, Nike flew her to a surprise party. They gave her a diamond-and-gold Swoosh ring and company stock estimated at over $1 million.\n\nThe $35 logo has appeared on over 800 million products.\n\n—\nFollow @blank.to.bold for a daily design fact that will change how you see the world.\n\n#NikeLogo #LogoDesign #BrandingStory #DesignHistory #GraphicDesign #DesignFacts #LogoDesigner #BrandIdentity #BlankToBold #DesignEducation #DesignCommunity #IconicLogos #CarolynDavidson #VisualIdentity #CreativeDirection #BrandDesign #DesignInspiration #LogoStory #MarketingDesign #DesignThinking"},
    {"category":"LOGO STORY","tag":"Logo Secret","line1":"FedEx Hides","line2":"an Arrow.","highlight":"an Arrow.","stat":"40+","caption":"There's a hidden arrow in the FedEx logo. It's been there since 1994. ➡️\n\nLook at the space between the letters E and x. There's a perfect white arrow pointing forward — embedded intentionally by designer Lindon Leader.\n\nThe arrow represents speed, precision, and forward motion — the core of FedEx's brand promise.\n\nThe logo has won over 40 design awards.\n\nOnce you see the arrow, you can never unsee it.\n\n—\nFollow @blank.to.bold for a daily design fact that will change how you see the world.\n\n#FedExLogo #LogoDesign #HiddenLogo #BrandingStory #GraphicDesign #DesignFacts #LogoDesigner #BrandIdentity #BlankToBold #DesignEducation #DesignCommunity #IconicLogos #VisualIdentity #NegativeSpace #DesignHistory #CreativeDirection #LogoStory #BrandDesign #DesignThinking #DesignInspiration"},
    {"category":"FONT STORY","tag":"Type Origin","line1":"Helvetica.","line2":"Born by Accident.","highlight":"Born by Accident.","stat":"1957","caption":"In 1957, Max Miedinger was asked to update an old font. What he created became Helvetica — the world's most used typeface.\n\nIt was meant to be neutral. That neutrality made it iconic.\n\nNYC Subway. NASA. Toyota. All Helvetica.\n\n—\nFollow @blank.to.bold for a daily design fact that will change how you see the world.\n\n#Helvetica #TypographyHistory #FontStory #TypeDesign #GraphicDesign #BlankToBold #DesignFacts #DesignHistory #DesignEducation #DesignCommunity #Typeface #VisualDesign #DesignInspiration #FontDesign #TypeInspiration"},
    {"category":"BRAND STORY","tag":"Brand Origin","line1":"Apple's Logo","line2":"Was a Mistake.","highlight":"Was a Mistake.","stat":"1977","caption":"Apple's first logo in 1976 was a detailed Newton illustration. Steve Jobs hated it.\n\nRob Janoff redesigned it in 1977. The bite was added so it didn't look like a cherry at small sizes.\n\nA practical printing fix became the world's most iconic logo.\n\n—\nFollow @blank.to.bold for a daily design fact that will change how you see the world.\n\n#AppleLogo #BrandHistory #LogoDesign #BrandingStory #GraphicDesign #BlankToBold #DesignFacts #BrandIdentity #DesignHistory #DesignEducation #DesignCommunity #IconicLogos #VisualIdentity #DesignInspiration #BrandDesign"},
    {"category":"COLOR STORY","tag":"Color Fact","line1":"Tiffany Blue.","line2":"Owned by Law.","highlight":"Owned by Law.","stat":"1837","caption":"Tiffany Blue isn't just a colour. It's a legal weapon. 🔵\n\nTiffany & Co. has owned Pantone 1837 since 1998 — trademarked so strictly that no other company can use it in jewellery packaging.\n\nA colour decision made in 1845 is now a billion-dollar brand asset protected by law.\n\n—\nFollow @blank.to.bold for a daily design fact that will change how you see the world.\n\n#TiffanyBlue #BrandIdentity #ColorTheory #LogoDesign #BrandingStrategy #DesignHistory #ColorPsychology #VisualIdentity #BrandDesign #GraphicDesign #DesignFacts #BrandStory #CreativeDirection #DesignCommunity #BlankToBold #DesignEducation #BrandColor #MarketingDesign #LuxuryBranding #DesignInspiration"},
    {"category":"FONT STORY","tag":"Type Fact","line1":"Comic Sans","line2":"Saved Lives.","highlight":"Saved Lives.","stat":"1994","caption":"You hate Comic Sans. But Comic Sans has saved lives. 🦸\n\nThe British Dyslexia Association found it's one of the most readable fonts for dyslexic readers.\n\nMedical teams use it because it reduces patient anxiety. NASA used it in their 2012 Mars Curiosity press conference.\n\nNever judge a font by its reputation.\n\n—\nFollow @blank.to.bold for a daily design fact that will change how you see the world.\n\n#ComicSans #Typography #FontDesign #TypeDesign #GraphicDesign #DesignFacts #TypeHistory #Dyslexia #DesignStory #BlankToBold #DesignEducation #DesignCommunity #FontLover #TypeInspiration #DesignHistory #InclusiveDesign #Accessibility #DesignThinking #BrandingFacts #VisualDesign"},
    {"category":"UX STORY","tag":"UX Origin","line1":"QWERTY Was","line2":"Built to Fail.","highlight":"Built to Fail.","stat":"40%","caption":"The keyboard you're using right now was designed to slow you down. ⌨️\n\nQWERTY was invented in 1873 to place common letter pairs far apart — preventing typewriter keys from jamming.\n\nThat problem was solved in the 1950s. The layout never changed.\n\nDvorak is 40% faster. Nobody switches.\n\n—\nFollow @blank.to.bold for a daily design fact that will change how you see the world.\n\n#QWERTY #KeyboardDesign #UXDesign #DesignHistory #InteractionDesign #ProductDesign #DesignFacts #UserExperience #BlankToBold #DesignEducation #DesignCommunity #DesignThinking #TechHistory #HumanCenteredDesign #DesignStory #UXHistory #DigitalDesign #DesignInspiration #GraphicDesign #BrandingFacts"},
    {"category":"BRAND STORY","tag":"Brand Fact","line1":"Coca-Cola","line2":"Invented Santa.","highlight":"Invented Santa.","stat":"1931","caption":"Before 1931, Santa Claus had no standard look — he appeared in many forms, wearing green, blue, or brown robes.\n\nIn 1931, Coca-Cola hired illustrator Haddon Sundblom to create a Santa for their winter campaign. That image became the global standard.\n\nA soft drink company defined what Santa looks like for the entire world.\n\n—\nFollow @blank.to.bold for a daily design fact that will change how you see the world.\n\n#CocaCola #BrandHistory #SantaClaus #BrandingStory #GraphicDesign #BlankToBold #DesignFacts #BrandIdentity #DesignHistory #VisualIdentity #DesignEducation #DesignCommunity #BrandDesign #AdvertisingHistory #DesignInspiration"},
    {"category":"LOGO STORY","tag":"Logo Fact","line1":"Google's Logo","line2":"Breaks Rules.","highlight":"Breaks Rules.","stat":"1999","caption":"Look at the Google logo. The letters don't follow consistent baseline rules. The 'e' is slightly tilted.\n\nDesigner Ruth Kedar deliberately broke typographic rules in 1999.\n\nThe most recognised logo in the world makes a statement by being slightly wrong.\n\n—\nFollow @blank.to.bold for a daily design fact that will change how you see the world.\n\n#GoogleLogo #LogoDesign #BrandingStory #GraphicDesign #BlankToBold #DesignFacts #LogoDesigner #BrandIdentity #DesignHistory #DesignEducation #DesignCommunity #IconicLogos #Typography #VisualIdentity #DesignInspiration"},
    {"category":"COLOR STORY","tag":"Color Story","line1":"Purple Was","line2":"Only for Kings.","highlight":"Only for Kings.","stat":"4M","caption":"For most of human history, purple dye required over 4 million sea snails per pound.\n\nRoman law restricted it to emperors. Anyone else wearing it could be executed.\n\nIn 1856, an 18-year-old accidentally created synthetic purple dye and became a millionaire.\n\nColor has always been power.\n\n—\nFollow @blank.to.bold for a daily design fact that will change how you see the world.\n\n#ColorHistory #PurpleDye #ColorTheory #DesignHistory #GraphicDesign #BlankToBold #DesignFacts #ColorPsychology #BrandColors #DesignEducation #DesignCommunity #VisualDesign #ColorInspiration #DesignStory #DesignInspiration"},
    {"category":"UX STORY","tag":"UX Fact","line1":"Loading Bars","line2":"Are Often Fake.","highlight":"Are Often Fake.","stat":"99%","caption":"Loading bars that speed up toward the end feel faster — even when they take the same total time.\n\nEngineers deliberately program progress bars to appear to accelerate near completion. It's designed perception, not real progress.\n\nPerception is part of the product.\n\n—\nFollow @blank.to.bold for a daily design fact that will change how you see the world.\n\n#UXDesign #ProgressBar #DesignPsychology #UserExperience #GraphicDesign #BlankToBold #DesignFacts #InteractionDesign #DesignHistory #ProductDesign #DesignEducation #DesignCommunity #DigitalDesign #UXResearch #DesignInspiration"},
    {"category":"FONT STORY","tag":"Type Story","line1":"Futura","line2":"Went to the Moon.","highlight":"Went to the Moon.","stat":"1969","caption":"On July 20, 1969, Apollo 11 left a plaque on the moon set in Futura.\n\nFutura was designed by Paul Renner in 1927, inspired by Bauhaus principles of pure geometric forms.\n\nA font designed in Germany in 1927 travelled 384,000 kilometres to the moon.\n\n—\nFollow @blank.to.bold for a daily design fact that will change how you see the world.\n\n#Futura #TypographyHistory #FontStory #TypeDesign #GraphicDesign #BlankToBold #DesignFacts #NASA #TypeInspiration #DesignHistory #DesignEducation #DesignCommunity #Typeface #VisualDesign #DesignInspiration"},
]

SLOTS = ["8am","10am","12pm","2pm","5pm","8pm"]
SLOT_CONFIGS = [
    {"bg":"#0A0A0A","fg":"#F5F0E8","ac":"#E63022"},
    {"bg":"#F5F0E8","fg":"#0A0A0A","ac":"#E63022"},
    {"bg":"#0A0A0A","fg":"#F5F0E8","ac":"#E63022"},
    {"bg":"#F5F0E8","fg":"#0A0A0A","ac":"#E63022"},
    {"bg":"#E63022","fg":"#F5F0E8","ac":"#0A0A0A"},
    {"bg":"#F5F0E8","fg":"#0A0A0A","ac":"#E63022"},
]
LAYOUTS = ["L1","L2","L3","L4","L5","L6"]

def get_story(slot_idx):
    start = (DAY * 6) % len(STORIES)
    return STORIES[(start + slot_idx) % len(STORIES)]

def pill(text, bg, fg="#fff"):
    return f'<span style="background:{bg};color:{fg};border-radius:999px;padding:6px 36px;font-style:italic;font-weight:900;display:inline-block;letter-spacing:-1px;line-height:1.2">{text}</span>'

def nav(fg, s):
    return f'<div style="display:flex;justify-content:space-between;align-items:center"><img src="{LOGO}" style="width:60px;height:60px;display:block"/><span style="font-size:20px;font-weight:700;color:{fg};opacity:.35;letter-spacing:2px;text-transform:uppercase">{s["category"]}</span></div>'

def footer(fg, ac):
    fc = "#fff" if ac != "#F5F0E8" else "#0A0A0A"
    return f'<div style="display:flex;justify-content:space-between;align-items:center;border-top:1.5px solid {fg}18;padding-top:20px;margin-top:auto"><span style="font-size:18px;color:{fg};opacity:.25;font-weight:500">@blank.to.bold</span><div style="background:{ac};color:{fc};border-radius:999px;padding:6px 22px;font-size:17px;font-weight:800;letter-spacing:1.5px">B/B</div></div>'

def css(bg, fg):
    return f"*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1350px;overflow:hidden;background:{bg};font-family:'Inter',system-ui,sans-serif;color:{fg}}}"

def build_html(slot_idx, s, cfg):
    bg,fg,ac = cfg["bg"],cfg["fg"],cfg["ac"]
    h1 = s["line1"]
    h2 = s["line2"].replace(s["highlight"],"")
    hi = s["highlight"]
    pb = "#0A0A0A" if bg=="#E63022" else ac
    pf = "#F5F0E8"
    pl = pill(hi, pb, pf)
    fs_map = {0:"136px",1:"148px",2:"106px",3:"120px",4:"116px",5:"140px"}
    fs = fs_map.get(slot_idx,"120px")
    # Adjust for long text
    total = len(h1)+len(h2)+len(hi)
    if total > 22: fs = str(int(fs.replace("px",""))-16)+"px"

    layouts = [
        # L1 Centered
        f"""<div style="padding:72px 80px;height:100%;display:flex;flex-direction:column">{nav(fg,s)}<div style="flex:1;display:flex;flex-direction:column;justify-content:center"><h1 style="font-size:{fs};font-weight:900;line-height:.95;letter-spacing:-4px">{h1}<br>{pl} {h2}</h1></div>{footer(fg,ac)}</div>""",
        # L2 Top flush
        f"""<div style="padding:72px 80px;height:100%;display:flex;flex-direction:column">{nav(fg,s)}<h1 style="font-size:{fs};font-weight:900;line-height:.92;letter-spacing:-5px;margin-top:48px">{h1}<br>{pl} {h2}</h1><div style="flex:1"></div><div style="font-size:22px;font-weight:600;color:{fg};opacity:.28;letter-spacing:3px;text-transform:uppercase;margin-bottom:32px">{s["tag"]}</div>{footer(fg,ac)}</div>""",
        # L3 Stat + split
        f"""<div style="padding:72px 80px;height:100%;display:flex;flex-direction:column">{nav(fg,s)}<div style="flex:1;display:flex;gap:0;align-items:center"><div style="width:4px;background:{ac};align-self:stretch;margin-right:48px;flex-shrink:0"></div><div style="flex:1"><span style="font-size:180px;font-weight:900;line-height:.85;letter-spacing:-6px;color:{ac};display:block;margin-bottom:20px">{s["stat"]}</span><h1 style="font-size:{fs};font-weight:900;line-height:1.0;letter-spacing:-3px">{h1}<br>{pl} {h2}</h1></div></div>{footer(fg,ac)}</div>""",
        # L4 Ghost word
        f"""<div style="padding:72px 80px;height:100%;display:flex;flex-direction:column;position:relative;overflow:hidden"><div style="position:absolute;right:-40px;top:50%;transform:translateY(-60%);font-size:380px;font-weight:900;color:{fg};opacity:.05;letter-spacing:-16px;line-height:1;white-space:nowrap;pointer-events:none">{s["stat"]}</div>{nav(fg,s)}<div style="flex:1;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:1"><h1 style="font-size:{fs};font-weight:900;line-height:1.0;letter-spacing:-3px">{h1}<br>{pl} {h2}</h1></div>{footer(fg,ac)}</div>""",
        # L5 Bottom anchored with accent bar
        f"""<div style="padding:72px 80px;height:100%;display:flex;flex-direction:column">{nav(fg,s)}<div style="height:6px;background:{'#0A0A0A' if bg=='#E63022' else ac};width:120px;margin:40px 0 56px"></div><div style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;padding-bottom:48px"><h1 style="font-size:{fs};font-weight:900;line-height:.96;letter-spacing:-3px">{h1}<br>{pl} {h2}</h1></div>{footer(fg,ac)}</div>""",
        # L6 Tag then headline bottom
        f"""<div style="padding:72px 80px;height:100%;display:flex;flex-direction:column">{nav(fg,s)}<div style="flex:1"></div><div style="font-size:22px;font-weight:700;color:{fg};opacity:.22;letter-spacing:3px;text-transform:uppercase;margin-bottom:28px">{s["tag"]}</div><h1 style="font-size:{fs};font-weight:900;line-height:.93;letter-spacing:-4px;margin-bottom:48px">{h1}<br>{pl} {h2}</h1>{footer(fg,ac)}</div>""",
    ]

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@900&display=swap" rel="stylesheet">
<style>{css(bg,fg)}</style></head><body>{layouts[slot_idx]}</body></html>"""

def render(html, out):
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={"width":1080,"height":1350})
        page.set_content(html, wait_until="networkidle")
        page.wait_for_timeout(1600)
        page.screenshot(path=out, full_page=False, type="jpeg", quality=97)
        b.close()

def github_upload(path, fname):
    with open(path,"rb") as f:
        content = base64.b64encode(f.read()).decode()
    url_api = f"https://api.github.com/repos/{REPO}/contents/{fname}"
    headers = {"Authorization":f"token {TOKEN}","Content-Type":"application/json","Accept":"application/vnd.github.v3+json"}
    try:
        req = urllib.request.Request(url_api, headers=headers)
        with urllib.request.urlopen(req) as r:
            sha = json.loads(r.read())["sha"]
        payload = json.dumps({"message":f"Update {fname}","content":content,"sha":sha}).encode()
    except:
        payload = json.dumps({"message":f"Add {fname}","content":content}).encode()
    req2 = urllib.request.Request(url_api, data=payload, headers=headers, method="PUT")
    with urllib.request.urlopen(req2) as r:
        return json.loads(r.read())["content"]["download_url"]

def post_instagram(image_url, caption, slot_label):
    # Post via Zapier webhook
    data = json.dumps({"image_url": image_url, "caption": caption, "slot": slot_label}).encode()
    req = urllib.request.Request(ZAPIER, data=data, headers={"Content-Type":"application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()

if __name__ == "__main__":
    slot_idx = int(sys.argv[1])  # 0-5
    print(f"Running slot {slot_idx} [{SLOTS[slot_idx]}]")

    s   = get_story(slot_idx)
    cfg = SLOT_CONFIGS[slot_idx]
    out = f"/tmp/poster_slot{slot_idx}.jpg"
    fn  = f"blanktobold/{TODAY}-slot{slot_idx+1}-{SLOTS[slot_idx]}.jpg"

    print(f"Story: {s['line1']} {s['line2']}")
    render(build_html(slot_idx, s, cfg), out)
    print(f"✓ Rendered")

    image_url = github_upload(out, fn)
    print(f"✓ Uploaded: {image_url}")

    result = post_instagram(image_url, s["caption"], SLOTS[slot_idx])
    print(f"✓ Posted: {result}")
