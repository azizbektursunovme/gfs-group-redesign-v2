#!/usr/bin/env python3
"""Build the static GFS GROUP LLC site.

Reads the content snapshot in _src/data (taken from the live site's API)
and writes the pages into the parent folder:

    python _src/build.py
"""
import html
import json
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
DATA = SRC / "data"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))["data"]


def clean(s):
    # one banner in the source data has a broken em dash
    return (s or "").replace("�", "—").strip()


def e(s):
    return html.escape(clean(str(s)), quote=True)


S = load("settings.json")

PHONE = clean(S["contact.phone"])
PHONE_SHORT = "(636) 442-1334"
TEL = "tel:" + S["contact.phoneFull"]
EMAIL = clean(S["contact.email"])
EMAIL_HR = "hr@gfs-groupllc.com"
ADDRESS = clean(S["contact.address"])
MAP_URL = S["contact.mapUrl"]
MAP_EMBED = S["contact.mapEmbedUrl"]
HOURS = [h.strip() for h in S["contact.workingHours"].split("|")]
APPLY_URL = "https://intelliapp.driverapponline.com/c/2415900?r=Noza"
FORM_ID = "inline-bQz7IIiAOwL2rSPfubC0"
FORM_URL = "https://link.runxai.com/widget/form/bQz7IIiAOwL2rSPfubC0"  # current GoHighLevel form the fields come from
SITE = clean(S["site.name"])
TAGLINE = clean(S["site.tagline"])

NAV = [
    ("why-us.html", "Why Us"),
    ("services.html", "Services"),
    ("partners.html", "Partners"),
    ("reviews.html", "Reviews"),
    ("contact-us.html", "Contact"),
]

# ------------------------------------------------------------------ icons

STROKE = {
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    "mail": '<path d="M3 6h18v12H3zM3 7l9 6 9-6"/>',
    "pin": '<path d="M12 21s7-6.2 7-11.5a7 7 0 0 0-14 0C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "pause": '<path d="M8 5v14M16 5v14"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="3.6"/><path d="M17.3 6.7h.01"/>',
    "deposit": '<rect x="3" y="6" width="18" height="12" rx="1.5"/><circle cx="12" cy="12" r="2.6"/><path d="M6.5 9.5v.01M17.5 14.5v.01"/>',
    "lanes": '<path d="M9 3L5 21M15 3l4 18M12 4.5v2.5M12 10.5V13M12 16.5V19"/>',
    "home": '<path d="M4 11l8-7 8 7M6 9.5V20h12V9.5M10 20v-6h4v6"/>',
    "medal": '<circle cx="12" cy="9" r="5"/><path d="M9 13.4L7.5 21l4.5-2.5 4.5 2.5-1.5-7.6"/>',
    "growth": '<path d="M4 20h16M5 16l5-5 3 3 6-7M15 7h4v4"/>',
    "truck": '<path d="M3 6h11v10H3zM14 9h4l3 3v4h-7z"/><circle cx="7" cy="17.5" r="2"/><circle cx="17" cy="17.5" r="2"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.2 8-8 9-4.8-1-8-4.5-8-9V6zM8.5 12l2.5 2.5 4.5-5"/>',
    "headset": '<path d="M5 14v-2a7 7 0 0 1 14 0v2M5 13h2.5v5H6a1 1 0 0 1-1-1zM19 13h-2.5v5H18a1 1 0 0 0 1-1zM18.5 18.5c0 1.4-1.6 2.2-4 2.2"/>',
    "chat": '<path d="M4 5h16v11H10l-5 4v-4H4z"/>',
}
FILLED = {
    "star": '<path d="M12 2.6l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5L12 17.4l-5.8 3.1 1.1-6.5L2.6 9.4l6.5-.9z"/>',
    "play": '<path d="M7 5l12 7-12 7z"/>',
    "facebook": '<path d="M14 8.5V7c0-.8.5-1 1-1h2V3h-2.7C11.6 3 10.5 4.8 10.5 6.8v1.7H8v3h2.5V21H14v-9.5h2.6l.4-3z"/>',
    "linkedin": '<path d="M4.5 9h3.2v11H4.5zM6.1 4a1.9 1.9 0 1 1 0 3.8 1.9 1.9 0 0 1 0-3.8zM10 9h3v1.6c.5-1 1.7-1.9 3.5-1.9 3 0 4 1.9 4 4.9V20h-3.2v-5.6c0-1.5-.4-2.6-1.9-2.6s-2.2 1.1-2.2 2.6V20H10z"/>',
}


def sprite():
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" aria-hidden="true">']
    for k, v in STROKE.items():
        out.append(f'<symbol id="i-{k}" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{v}</g></symbol>')
    for k, v in FILLED.items():
        out.append(f'<symbol id="i-{k}" viewBox="0 0 24 24"><g fill="currentColor">{v}</g></symbol>')
    out.append('<symbol id="i-arrow" viewBox="0 0 48 48"><path transform="rotate(45 24 24)" d="M24 3 43 24H31.5v21h-15V24H5z"/></symbol>')
    out.append("</svg>")
    return "".join(out)


def icon(name, cls=""):
    c = f"icon {cls}".strip()
    return f'<svg class="{c}" aria-hidden="true"><use href="#i-{name}"/></svg>'


def arrow(cls="sign__arrow"):
    return f'<svg class="{cls}" viewBox="0 0 48 48" aria-hidden="true"><use href="#i-arrow"/></svg>'


# ------------------------------------------------------------ components

_ids = iter(range(1, 10_000))

SHIELD = "M8 22Q60 2 112 22C117 52 104 92 60 116 16 92 3 52 8 22Z"
US_SHIELD = "M60 7C47 15 30 15 17 9c2 13-7 24-9 36-3 31 17 54 52 68 35-14 55-37 52-68-2-12-11-23-9-36-13 6-30 6-43-2Z"


def num_size(value, base):
    n = len(value)
    return base if n <= 2 else round(base * {3: .8, 4: .66, 5: .56}.get(n, .48))


def marker_svg(shape, value, crown=""):
    """A route marker carrying a number, drawn in the brand colours."""
    v = e(value)
    label = f' role="img" aria-label="{v}"'
    if shape == "shield":
        cid = f"mk{next(_ids)}"
        return (
            f'<svg class="mk" viewBox="0 0 120 120"{label}><defs><clipPath id="{cid}"><path d="{SHIELD}"/></clipPath></defs>'
            f'<g clip-path="url(#{cid})"><rect width="120" height="120" fill="#1e3b7e"/><rect width="120" height="41" fill="#e13a40"/>'
            f'<rect y="39" width="120" height="3" fill="#fff"/></g>'
            f'<path d="{SHIELD}" fill="none" stroke="#fff" stroke-width="2.6" transform="translate(5.4 5.9) scale(.91)"/>'
            f'<text x="60" y="33" text-anchor="middle" font-size="10.5" letter-spacing="1.4" fill="#fff">{e(crown.upper())}</text>'
            f'<text x="60" y="{88 if len(value) <= 2 else 84}" text-anchor="middle" font-size="{num_size(value, 46)}" fill="#fff">{v}</text></svg>'
        )
    if shape == "us":
        return (
            f'<svg class="mk" viewBox="0 0 120 120"{label}><path d="{US_SHIELD}" fill="#fff" stroke="#0f1d3d" stroke-width="5" stroke-linejoin="round"/>'
            f'<text x="60" y="{80 if len(value) <= 2 else 76}" text-anchor="middle" font-size="{num_size(value, 50)}" fill="#0f1d3d">{v}</text></svg>'
        )
    if shape == "circle":
        return (
            f'<svg class="mk" viewBox="0 0 120 120"{label}><rect x="5" y="5" width="110" height="110" rx="13" fill="#0f1d3d"/>'
            f'<ellipse cx="60" cy="60" rx="47" ry="41" fill="#fff"/>'
            f'<text x="60" y="{78 if len(value) <= 2 else 74}" text-anchor="middle" font-size="{num_size(value, 50)}" fill="#0f1d3d">{v}</text></svg>'
        )
    return (
        f'<svg class="mk" viewBox="0 0 120 120"{label}><rect x="3" y="17" width="114" height="86" rx="11" fill="#e13a40"/>'
        f'<rect x="8.5" y="22.5" width="103" height="75" rx="6.5" fill="none" stroke="#fff" stroke-width="3"/>'
        f'<text x="60" y="{76 if len(value) <= 2 else 73}" text-anchor="middle" font-size="{num_size(value, 48)}" fill="#fff">{v}</text></svg>'
    )


def markers(items):
    """items: (shape, value, crown, label, description)"""
    out = ['<ul class="markers">']
    for shape, value, crown, label, desc in items:
        out.append(f'<li class="marker">{marker_svg(shape, value, crown)}<p class="marker__label">{e(label)}</p>')
        if desc:
            out.append(f'<p class="marker__desc">{e(desc)}</p>')
        out.append("</li>")
    out.append("</ul>")
    return "".join(out)


def figures(items, cls=""):
    c = f"figures {cls}".strip()
    return f'<ul class="{c}">' + "".join(
        f'<li><p class="figure__n">{e(n)}</p><p class="figure__l">{e(l)}</p></li>' for n, l in items
    ) + "</ul>"


def rows(items):
    return '<ul class="rows">' + "".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in items) + "</ul>"


def pillars(items):
    return '<ul class="pillars">' + "".join(
        f'<li class="pillar"><div class="reg"><div class="reg__face"><h3>{e(t)}</h3></div></div>'
        f'<span class="post" aria-hidden="true"></span><p class="pillar__text">{e(d)}</p></li>'
        for t, d in items
    ) + "</ul>"


def bars(items):
    return '<ul class="bars">' + "".join(
        f'<li><p class="bar__top"><span>{e(l)}</span><span>{p}%</span></p>'
        f'<div class="bar__track"><div class="bar__fill" style="width:{p}%"></div></div></li>'
        for l, p in items
    ) + "</ul>"


def stars(n):
    s = "".join(f'<svg class="{"" if i < n else "off"}" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-star"/></svg>' for i in range(5))
    return f'<span class="stars" role="img" aria-label="{n} out of 5 stars">{s}</span>'


SOURCES = {"GOOGLE": "Google review", "FACEBOOK": "Facebook review", "WEBSITE": "Website review"}


def quote(r, with_cat=False):
    cat = f' data-cat="{review_cat(r["role"])}"' if with_cat else ""
    return (
        f'<li class="quote"{cat}><p class="quote__meta">{stars(r["rating"])}<span>{SOURCES.get(r["source"], "")}</span></p>'
        f'<blockquote>“{e(r["text"])}”</blockquote>'
        f'<p class="quote__who">{e(r["name"])} <span>— {e(r["role"])}</span></p></li>'
    )


def btn(label, href, kind="primary", extra=""):
    ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
    return f'<a class="btn btn--{kind}" href="{e(href)}"{ext}{extra}>{label}</a>'


def tab(text):
    return f'<p class="sign-tab">{e(text)}</p>'


def sign_cta(title, text, buttons, tab_text=""):
    return (
        '<section class="section section--flush-top"><div class="wrap"><div class="tabbed">'
        + (tab(tab_text) if tab_text else "")
        + f'<div class="sign sign--cta"><div><h2>{title}</h2><p>{e(text)}</p></div>'
        f'<div class="btn-row">{"".join(buttons)}</div></div></div></div></section>'
    )


def page_hero(title, lead, chips=(), buttons=(), side=""):
    chips_html = '<ul class="chips">' + "".join(f'<li class="chip">{e(c)}</li>' for c in chips) + "</ul>" if chips else ""
    buttons_html = f'<div class="btn-row">{"".join(buttons)}</div>' if buttons else ""
    return (
        '<section class="page-hero"><div class="gantry" aria-hidden="true"></div><div class="wrap">'
        f'<div class="rig"><div class="sign sign--title sign--lit is-swept"><h1>{title}</h1>{arrow()}</div></div>'
        f'<div class="page-hero__below"><p class="lead">{e(lead)}</p>'
        f'<div class="page-hero__side">{chips_html}{buttons_html}{side}</div></div></div></section>'
    )


def mileage(rows_, cls=""):
    c = f"sign sign--mileage {cls}".strip()
    return f'<div class="{c}"><dl>' + "".join(
        f'<div class="mile-row"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows_
    ) + "</dl></div>"


LANES = (
    '<svg class="lanes" viewBox="0 0 600 300" fill="none" aria-hidden="true">'
    '<g stroke="#4a6fa5" stroke-opacity=".55" stroke-width="7">'
    '<path d="M600 114H440L350 24H0"/><path d="M600 126H380l-60-60H0"/><path d="M600 138H320l-30-30H0"/>'
    '<path d="M600 162H320l-30 30H0"/><path d="M600 174H380l-60 60H0"/><path d="M600 186H440l-90 90H0"/></g>'
    '<path d="M600 150H0" stroke="#e13a40" stroke-width="4"/></svg>'
)

# ----------------------------------------------------------------- layout


def header(active):
    nav = "".join(
        f'<a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == active else ""}>{t}</a>' for h, t in NAV
    )
    menu = "".join(f'<li><a href="{h}">{t}{arrow("")}</a></li>' for h, t in [("index.html", "Home")] + NAV)
    return f"""
<a class="skip" href="#main">Skip to content</a>
{sprite()}
<header class="site-header">
  <div class="wrap site-header__in">
    <a class="brand" href="index.html" aria-label="{SITE} — home"><img src="assets/img/logo.png" alt="{SITE}" width="120" height="46"></a>
    <nav class="nav" aria-label="Main">{nav}</nav>
    <a class="header__phone" href="{TEL}">{icon("phone")}{PHONE}</a>
    <a class="btn btn--primary btn--sm" href="{APPLY_URL}" target="_blank" rel="noopener">Drive with Us</a>
    <a class="btn btn--line btn--sm" href="contact-us.html#{FORM_ID}">Contact Us</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">{icon("menu", "i-open")}{icon("close", "i-close")}<span class="menu-btn__label">Menu</span></button>
  </div>
  <div class="menu" id="menu" hidden>
    <nav class="sign" aria-label="Mobile"><ul class="menu__list">{menu}</ul></nav>
    <div class="menu__extra">
      <a class="btn btn--line" href="{TEL}">{icon("phone")}{PHONE}</a>
      <a class="btn btn--blue" href="contact-us.html#{FORM_ID}">Contact Us</a>
    </div>
  </div>
</header>"""


def footer(cta=True):
    quick = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in [("index.html", "Home")] + [n for n in NAV if n[0] != "services.html"])
    services = "".join(
        f'<li><a href="services.html">{s}</a></li>'
        for s in ["CDL Driver Recruiting", "Owner-Operator Programs", "Fleet Partnerships", "Carrier &amp; Logistics"]
    )
    hours = "<br>".join(e(h) for h in HOURS)
    band = f"""
<section class="cta">
  {LANES}
  <div class="wrap cta__in"><div class="cta__copy">
    <h2>{e(S["footer.ctaTitle"])}</h2>
    <p>{e(S["footer.ctaSubtitle"])}</p>
    <div class="btn-row">{btn(e(S["footer.ctaButtonText"]), "contact-us.html")}{btn(icon("phone") + PHONE_SHORT, TEL, "ghost")}</div>
  </div></div>
</section>"""
    return (band if cta else "") + f"""
<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__about">
        <img class="footer__logo" src="assets/img/logo.png" alt="{SITE}" width="136" height="52" loading="lazy">
        <p>{e(S["footer.description"])}</p>
        <ul class="socials">
          <li><a href="{e(S["social.facebook"])}" target="_blank" rel="noopener" aria-label="Facebook">{icon("facebook")}</a></li>
          <li><a href="{e(S["social.linkedin"])}" target="_blank" rel="noopener" aria-label="LinkedIn">{icon("linkedin")}</a></li>
          <li><a href="{e(S["social.instagram"])}" target="_blank" rel="noopener" aria-label="Instagram">{icon("instagram")}</a></li>
        </ul>
      </div>
      <nav aria-label="Quick links"><h2>Quick links</h2><ul>{quick}</ul></nav>
      <nav aria-label="Our services"><h2>Our services</h2><ul>{services}</ul></nav>
      <div><h2>Contact us</h2>
        <ul class="footer__contact">
          <li>{icon("phone")}<span><a href="{TEL}"><b>{PHONE}</b></a><small>Call us anytime</small></span></li>
          <li>{icon("mail")}<span><a href="mailto:{EMAIL}"><b>{EMAIL}</b></a><small>Send us a message</small></span></li>
          <li>{icon("pin")}<span><a href="{e(MAP_URL)}" target="_blank" rel="noopener"><b>{e(ADDRESS)}</b></a><small>View on Google Maps</small></span></li>
          <li>{icon("clock")}<span><b>Business hours</b><small>{hours}</small></span></li>
        </ul>
      </div>
    </div>
    <ul class="creds">
      <li>{icon("shield")}USDOT &amp; MC Certified</li>
      <li>{icon("check")}Licensed Freight Broker</li>
      <li>{icon("star")}{AVG:.1f}/5 Driver Rating</li>
    </ul>
    <div class="footer__bar">
      <p>© 2026 {SITE}. All rights reserved.</p>
      <ul><li><a href="privacy-policy.html">Privacy Policy</a></li><li><a href="terms-of-service.html">Terms of Service</a></li></ul>
    </div>
  </div>
</footer>"""


def page(file, title, desc, body, active=None, cta=True):
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="keywords" content="{e(S["seo.keywords"])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#1e3b7e">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Overpass:wght@400;600;700;800&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{footer(cta)}
<script src="assets/js/site.js" defer></script>
</body>
</html>
"""
    (OUT / file).write_text(doc, encoding="utf-8", newline="\n")
    print("wrote", file, f"{len(doc) / 1024:.0f} KB")


# ---------------------------------------------------------------- content

WHY_STATS = [
    ("us", "5+", "", "Years of excellent service", "Reliable logistics execution backed by consistency, speed, and accountable communication."),
    ("shield", "48", "States", "States served", "Consistent, dependable performance"),
    ("circle", "250+", "", "Drivers nationwide", "A growing network of professional drivers delivering excellence across all routes."),
    ("plate", "24/7", "", "Support always available", "Round-the-clock assistance ensuring you're never alone on the road."),
]

REASONS = [
    ("Drivers First, Always", "We know what drivers deserve — real respect, steady miles, and top pay that reflects your hard work and dedication."),
    ("You Are Part of the Team", "At GFS Group, you're not just a number — you're part of a team that values your time, your skills, and your life on and off the road."),
    ("Flexible Routes & 24/7 Support", "We offer competitive rates, flexible routes, and round-the-clock support to keep you moving and earning every mile."),
    ("Built for Your Success", "Ready for a company that drives your success? Join GFS Group today — Where Drivers Come First!"),
]

PILLARS = [
    ("Drivers First, Always", "We know what drivers deserve — real respect, steady miles, and top pay that reflects your hard work and dedication."),
    ("Regulation-Ready", "Our team aligns each operation with DOT/FMCSA expectations, reducing avoidable risk and ensuring full compliance."),
    ("Protected", "We verify load details, lane requirements, and communication checkpoints before execution begins."),
    ("Reliable", "When conditions change, we respond fast with practical alternatives that protect schedule commitments."),
]

KEEP_UPPER = {"CDL", "GFS", "LLC", "USDOT", "MC", "DOT"}


def sign_case(s):
    """Banner titles are stored in capitals; guide signs read better in mixed case."""
    return " ".join(w if (w in KEEP_UPPER or not w.isalpha()) else w.capitalize() for w in clean(s).split())


def all_reviews():
    """Reviews from the snapshot, minus exact duplicates and the test entry."""
    seen, out = set(), []
    for r in sorted(load("reviews.json"), key=lambda r: r["order"]):
        key = (r["name"], r["text"])
        if key in seen or r["name"].lower().startswith("test"):
            continue
        seen.add(key)
        out.append(r)
    return out


def review_cat(role):
    r = role.lower()
    if "owner" in r:
        return "owner"
    if r.endswith("driver"):
        return "driver"
    return "partner"


def all_partners():
    return [p for p in sorted(load("partners.json"), key=lambda p: p["order"]) if not p["name"].lower().startswith("test")]


def plaque(p):
    if p["logoUrl"]:
        src = "assets/img/partners/" + p["logoUrl"].rsplit("/", 1)[-1]
        return f'<li class="plaque"><img src="{src}" alt="{e(p["name"])}" loading="lazy"></li>'
    return f'<li class="plaque plaque--text">{e(p["name"])}</li>'


REVIEWS = all_reviews()
PARTNERS = all_partners()
PSEC = load("partners_section.json")
AVG = sum(r["rating"] for r in REVIEWS) / len(REVIEWS)
RECOMMEND = round(100 * sum(r["rating"] >= 4 for r in REVIEWS) / len(REVIEWS))


def contact_rows(email=EMAIL):
    return [
        ("Phone", f'<a href="{TEL}">{PHONE}</a>'),
        ("Email", f'<a href="mailto:{email}">{email}</a>'),
        ("Address", f'<a href="{e(MAP_URL)}" target="_blank" rel="noopener">{e(ADDRESS)}</a>'),
        ("Hours", "".join(f"<span>{e(h)}</span>" for h in HOURS)),
    ]


# ------------------------------------------------------------------- home


def home():
    slides = sorted(load("hero-banners.json"), key=lambda b: b["order"])
    exits, legends, copies, photos = [], [], [], []
    for i, b in enumerate(slides):
        on = i == 0
        title = f"<span>{e(sign_case(b['title']))}</span> <span>{e(sign_case(b['subtitle']))}</span>"
        label = e(sign_case(b["title"]) + " " + sign_case(b["subtitle"]))
        exits.append(
            f'<button class="exit" type="button" role="tab" id="exit-{i}" aria-controls="slide-{i}" '
            f'aria-selected="{"true" if on else "false"}" tabindex="{0 if on else -1}" aria-label="Exit {i + 1}: {label}">EXIT {i + 1}</button>'
        )
        tag = "h1" if on else "p"
        legends.append(f'<{tag} class="legend{" is-active" if on else ""}" data-slide="{i}">{title}</{tag}>')
        link = APPLY_URL  # hero buttons open the Tenstreet application
        copies.append(
            f'<div class="copy{" is-active" if on else ""}" id="slide-{i}" role="tabpanel" aria-labelledby="exit-{i}" data-slide="{i}">'
            f'<p class="hero__desc">{e(b["description"])}</p>'
            f'<div class="btn-row">{btn(e(b["ctaText"]), link)}{btn(icon("phone") + e(b["secondaryCtaText"]), b["secondaryCtaLink"], "line")}</div></div>'
        )
        src = "assets/img/hero/" + b["imageUrl"].rsplit("/", 1)[-1]
        photos.append(f'<img src="{src}" alt="" data-slide="{i}"{" class=" + chr(34) + "is-active" + chr(34) if on else " loading=" + chr(34) + "lazy" + chr(34)}>')

    featured = [r for r in REVIEWS if r["isFeatured"]][:5]
    home_partners = [p for p in PARTNERS if p["logoUrl"]][:12]

    body = f"""
<section class="hero" data-hero>
  <div class="gantry" aria-hidden="true"></div>
  <div class="wrap">
    <div class="rig rig--tabs">
      <div class="exits">
        <button class="exits__pause" type="button" aria-pressed="false" aria-label="Pause rotation">{icon("pause", "i-pause")}{icon("play", "i-play")}</button>
        <div class="exits__tabs" role="tablist" aria-label="Featured messages">{"".join(exits)}</div>
      </div>
      <div class="sign sign--overhead sign--lit is-swept">
        <div class="legends">{"".join(legends)}</div>
        {arrow()}
      </div>
    </div>
    <div class="hero__below">
      <div>
        <div class="copies">{"".join(copies)}</div>
        <ul class="badges">
          <li>{icon("check")}USDOT Certified</li>
          <li>{icon("check")}250+ Drivers</li>
          <li>{icon("check")}24/7 Support</li>
        </ul>
      </div>
      <div class="hero__photo">{"".join(photos)}</div>
    </div>
  </div>
</section>

<section class="section" id="why-us">
  <div class="wrap">
    <div class="head head--split">
      <h2>Why Choose {SITE}?</h2>
      <div class="head__side">
        <p class="lead">Reliable logistics solutions based on experience, speed, and global reach are why companies choose us.</p>
        <a class="text-link" href="why-us.html">Why drivers choose GFS</a>
      </div>
    </div>
    {markers(WHY_STATS)}
  </div>
</section>

<section class="section section--surface" id="pillars">
  <div class="wrap">
    <div class="head head--split">
      <h2>{e(S["why_us.pillars.title"])}</h2>
      <p class="lead">{e(S["why_us.pillars.subtitle"])}</p>
    </div>
    {pillars(PILLARS)}
  </div>
</section>

<section class="section" id="partners">
  <div class="wrap">
    <div class="sign board">
      <div class="board__head">
        <h2>{e(PSEC["title"])}</h2>
        <p>{e(PSEC["subtitle"])}</p>
      </div>
      <ul class="plaques">{"".join(plaque(p) for p in home_partners)}</ul>
      <div class="board__foot">
        <p>{len(PARTNERS)} brokers and carriers listed on the full board.</p>
        {btn("See all partners", "partners.html", "white")}
      </div>
    </div>
  </div>
</section>

<section class="section section--surface" id="reviews">
  <div class="wrap split">
    <div class="split__aside">
      <h2>Trusted by Businesses Nationwide</h2>
      <p class="lead">Join thousands of satisfied clients who rely on {SITE} for their logistics needs. Here's what they have to say.</p>
      {figures([(f"{AVG:.1f}", "Average Rating"), ("2,250+", "Happy Customers"), (f"{RECOMMEND}%", "Would Recommend")], "figures--2")}
      {btn("Read all reviews", "reviews.html", "blue")}
    </div>
    <ul class="quotes">{"".join(quote(r) for r in featured)}</ul>
  </div>
</section>

<section class="section" id="contact">
  <div class="wrap split split--even">
    <div class="split__aside">
      <h2>Contact {SITE}</h2>
      <p class="lead">If you have any questions about delivery, partnership, or want to learn more about our logistics services — feel free to reach out.</p>
      {btn("View full contact page", "contact-us.html", "blue")}
    </div>
    {mileage(contact_rows())}
  </div>
</section>
"""
    page("index.html", S["seo.defaultMetaTitle"], S["seo.defaultMetaDesc"], body)


# ----------------------------------------------------------------- why us

BENEFITS = [
    ("deposit", "Weekly Direct Deposit", "Get paid every week, on time — no delays, no excuses."),
    ("lanes", "Steady Freight Lanes", "Consistent routes with our top partners across 48 states."),
    ("home", "Home Time That Works", "Schedules built around your life — not the other way around."),
    ("medal", "Sign-On & Safety Bonuses", "Industry-leading bonus programs that reward your dedication."),
    ("growth", "Career Growth Programs", "Training, mentorship, and clear paths to advance your career."),
    ("truck", "Modern Equipment", "Well-maintained, late-model trucks equipped with the latest safety tech."),
]

VOICES = [
    ("Five years with GFS and I still look forward to every shift. The pay is honest, the dispatchers are real humans, and I actually feel valued here.", "Tony B.", "OTR Driver, 5 years with GFS"),
    ("GFS gave me home time that actually worked with my family. I did not think that was possible in trucking. Now I am a believer and I recommend everyone here.", "James L.", "Regional Driver, 4 years with GFS"),
    ("Transparent pay, real support, no games. As an owner-operator I cleared 40% more than my previous company. The numbers speak for themselves.", "Rachel S.", "Owner-Operator, 2 years with GFS"),
]


def why_us():
    services = "".join(
        f'<li class="service"><span class="service__pic">{icon(i)}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>'
        for i, t, d in BENEFITS
    )
    voices = "".join(
        f'<li class="quote"><p class="quote__meta">{stars(5)}</p><blockquote>“{e(t)}”</blockquote>'
        f'<p class="quote__who">{e(n)} <span>— {e(r)}</span></p></li>'
        for t, n, r in VOICES
    )
    body = (
        page_hero(
            f"Why Choose {SITE}?",
            f"We built {SITE} around one simple truth — when drivers succeed, everyone succeeds. Here is why thousands of professionals trust us every mile, every day.",
            ["No Hidden Fees", "Weekly Pay", "24/7 Dispatch", "Top-Tier Partners"],
            [btn(f"Join {SITE}", APPLY_URL), btn("Our Services", "services.html", "line")],
        )
        + f"""
<section class="section">
  <div class="wrap split">
    <div class="split__aside">
      <h2>What Makes Us Different</h2>
      <p class="lead">It is not just about moving freight — it is about building careers, relationships, and lasting trust on every road.</p>
    </div>
    {rows(REASONS[1:])}
  </div>
</section>

<section class="section section--surface">
  <div class="wrap split split--even">
    <figure class="photo"><img src="https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&amp;fit=crop&amp;w=1200&amp;q=80" alt="{SITE} logistics fleet" loading="lazy" width="1200" height="900"></figure>
    <div class="panel">
      <p class="score"><b>4.9</b><span>Average driver satisfaction score</span></p>
      {bars([("Pay & Compensation", 96), ("Dispatch Communication", 97), ("Home Time Flexibility", 94), ("Equipment Quality", 95), ("Company Culture", 98)])}
      <p class="note">Based on internal driver surveys — 2024</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head head--split">
      <h2>Everything You Need to Thrive on the Road</h2>
      <p class="lead">We do not just offer jobs — we offer full careers built on real support, real pay, and real respect for your time and your family.</p>
    </div>
    <div class="tabbed">{tab("Driver Benefits")}<div class="sign"><ul class="services">{services}</ul></div></div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="wrap split">
    <div class="split__aside">
      <p class="kicker">Real Voices</p>
      <h2>Hear It from Our Drivers</h2>
      <a class="text-link" href="reviews.html">Read all {len(REVIEWS)} reviews</a>
    </div>
    <ul class="quotes">{voices}</ul>
  </div>
</section>
"""
        + sign_cta(
            "Ready to Drive with the Best?",
            "Join our growing family of professional drivers and partners. Your success is our mission — let us build it together.",
            [btn("Apply Now", APPLY_URL, "white"), btn("View Services", "services.html", "ghost")],
            "Now Hiring",
        )
    )
    page("why-us.html", f"Why Us — {SITE}", f"Why drivers, owner-operators and fleet partners choose {SITE}: weekly pay, 24/7 dispatch, steady lanes and top-tier partners.", body, "why-us.html", cta=False)


# --------------------------------------------------------------- services


def services():
    side = mileage(
        [(e(s), arrow("mile-arrow")) for s in ["CDL Driver Recruiting", "Owner-Operator Programs", "Fleet Partnerships", "Carrier & Logistics"]],
        "sign--list",
    )
    body = (
        page_hero(
            "Our Services",
            S["footer.description"],
            buttons=[btn("Get Started Today", "contact-us.html"), btn(icon("phone") + PHONE_SHORT, TEL, "line")],
        )
        + f"""
<section class="section">
  <div class="wrap split split--even">
    <div class="split__aside">
      <h2>{e(S["why_us.key_points.title"])}</h2>
      <p class="lead">{e(S["why_us.key_points.subtitle"])}</p>
      <p class="lead">Reliable logistics solutions based on experience, speed, and global reach are why companies choose us. We collaborate with industry-leading brands to deliver exceptional value and innovation.</p>
      <a class="text-link" href="index.html#pillars">The four pillars behind every delivery</a>
    </div>
    {side}
  </div>
</section>
"""
        + sign_cta(
            f"Ready to Join {SITE}?",
            f"{TAGLINE}. Experience the difference of working with a team that truly values your success, safety, and satisfaction.",
            [btn("Get Started Today", "contact-us.html", "white"), btn("Why Choose GFS", "why-us.html", "ghost")],
        )
    )
    page("services.html", f"Services — {SITE}", "CDL driver recruiting, owner-operator programs, fleet partnerships, and carrier and logistics services across 48 states.", body, "services.html", cta=False)


# --------------------------------------------------------------- partners

PARTNER_ICONS = ["star", "shield", "deposit", "lanes", "headset", "growth"]
PARTNER_STAT_DESC = [
    ("circle", "", "Industry leaders across all freight sectors"),
    ("us", "", "Consistent, dependable performance"),
    ("plate", "", "Proven track record of reliable delivery"),
    ("shield", "States", "Full contiguous US network"),
]
REQUIREMENTS = [
    ("Active MC Authority (FMCSA)", "Current Motor Carrier authority in good standing with the FMCSA."),
    ("Good safety record", "Satisfactory DOT safety rating and a clean compliance history."),
    ("Valid insurance coverage", "Active Auto Liability ($1M) and Cargo ($100k) policies."),
    ("Signed carrier agreement", f"Completed and executed {SITE} carrier packet."),
]


def partners():
    stats = [(shape, s["value"], crown, s["label"], desc) for s, (shape, crown, desc) in zip(PSEC["stats"], PARTNER_STAT_DESC)]
    groups = []
    for cat, name in [("BROKER", "Brokers"), ("CARRIER", "Carriers")]:
        items = [p for p in PARTNERS if p["category"] == cat]
        groups.append(
            f'<div class="board__group"><h3>{name} <small>{len(items)} active partners</small></h3>'
            f'<ul class="plaques">{"".join(plaque(p) for p in items)}</ul></div>'
        )
    feats = "".join(
        f'<li class="feature">{icon(i)}<h3>{e(b["title"])}</h3><p>{e(b["desc"])}</p></li>' for i, b in zip(PARTNER_ICONS, PSEC["benefits"])
    )
    steps = "".join(
        f'<li class="stop"><span class="milepost"><small>MILE</small><b>{int(s["step"])}</b></span><h3>{e(s["title"])}</h3><p>{e(s["desc"])}</p></li>'
        for s in PSEC["howItWorks"]
    )
    reqs = "".join(f'<li class="reg"><div class="reg__face"><div><h3>{e(t)}</h3><p>{e(d)}</p></div></div></li>' for t, d in REQUIREMENTS)
    body = (
        page_hero(
            "Our Trusted Partners",
            "We collaborate with the most trusted names in North American logistics — giving our drivers access to the best loads, lanes, and opportunities in the industry.",
            ["50+ Partners", "48 States", "Top-Tier Brokers", "Quick Pay"],
            [btn("Become a Partner", "contact-us.html"), btn(f"Why {SITE}", "why-us.html", "line")],
        )
        + f"""
<section class="section">
  <div class="wrap">{markers(stats)}</div>
</section>

<section class="section section--flush-top">
  <div class="wrap">
    <div class="tabbed">{tab("Trusted Network")}
      <div class="sign board">
        <div class="board__head"><h2>{e(PSEC["title"])}</h2><p>{e(PSEC["subtitle"])}</p></div>
        {"".join(groups)}
      </div>
    </div>
  </div>
</section>

<section class="section section--surface">
  <div class="wrap">
    <div class="head head--split">
      <div><p class="kicker">Partner Advantages</p><h2>What You Get When You Partner with {SITE}</h2></div>
      <p class="lead">Our partner relationships are built on mutual success.</p>
    </div>
    <ul class="features">{feats}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap split split--even">
    <figure class="photo"><img src="https://images.unsplash.com/photo-1560472355-536de3962603?auto=format&amp;fit=crop&amp;w=1200&amp;q=80" alt="{SITE} partnership" loading="lazy" width="1200" height="900"></figure>
    <div class="panel">
      <h2 class="h3">Partner Performance</h2>
      {bars([(p["label"], p["pct"]) for p in PSEC["performance"]])}
    </div>
  </div>
</section>

<section class="section section--surface">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Simple Process</p>
      <h2>How to Become a Partner</h2>
    </div>
    <ol class="route">{steps}</ol>
    <div class="btn-row route__cta">{btn("Start Your Application", "contact-us.html")}</div>
  </div>
</section>

<section class="section">
  <div class="wrap split split--even">
    <div class="split__aside">
      <p class="kicker">Requirements</p>
      <h2>What you need to get started</h2>
      <p class="lead">We maintain high standards to protect our carriers, our shippers, and the freight we move. Here's what you'll need:</p>
    </div>
    <ul class="reqs">{reqs}</ul>
  </div>
</section>
"""
        + sign_cta(
            f"Partner with {SITE}",
            "We are always looking for new partnerships that bring real value to our driver network.",
            [btn("Get in Touch", "contact-us.html", "white"), btn(f"Why {SITE}", "why-us.html", "ghost")],
        )
    )
    page("partners.html", f"Partners — {SITE}", f"The brokers and carriers {SITE} works with, what partners get, and how to become one.", body, "partners.html", cta=False)


# ---------------------------------------------------------------- reviews


def reviews():
    n = len(REVIEWS)
    cats = {c: sum(1 for r in REVIEWS if review_cat(r["role"]) == c) for c in ("driver", "owner", "partner")}
    counts = {s: sum(1 for r in REVIEWS if r["rating"] == s) for s in range(5, 0, -1)}
    recommend = round(100 * sum(1 for r in REVIEWS if r["rating"] >= 4) / n)
    stats = [
        ("circle", f"{n}+", "", "Verified Reviews", "From our community"),
        ("us", f"{AVG:.1f}", "", "Average Rating", "Out of 5.0 stars"),
        ("plate", f"{recommend}%", "", "Would Recommend", "Rated 4 stars or higher"),
        ("shield", "5+", "Years", "Years of Trust", "Building loyalty daily"),
    ]
    filt = "".join(
        f'<button class="chip" type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{l}<b>{c}</b></button>'
        for k, l, c in [("all", "All Reviews", n), ("driver", "Drivers", cats["driver"]), ("owner", "Owner-Operators", cats["owner"]), ("partner", "Partners", cats["partner"])]
    )
    breakdown = "".join(
        f'<li><p class="bar__top"><span>{s} stars ({c})</span><span>{round(100 * c / n)}%</span></p>'
        f'<div class="bar__track"><div class="bar__fill" style="width:{round(100 * c / n)}%"></div></div></li>'
        for s, c in counts.items()
    )
    trust = [
        ("shield", "Verified Reviewer Identity", "Every review comes from a real driver, partner, or operator in our network."),
        ("star", "No Incentivized Reviews", "We never pay for reviews. Our rating is earned, not bought."),
        ("chat", "We Respond to Every Review", "Our team actively engages with feedback — positive and constructive alike."),
    ]
    body = (
        page_hero(
            "What Our Community Says",
            f"Real stories from real drivers, owner-operators, and logistics partners. See why {SITE} consistently earns a {AVG:.1f}-star rating.",
        )
        + f"""
<section class="section">
  <div class="wrap">{markers(stats)}</div>
</section>

<section class="section section--flush-top" data-reviews>
  <div class="wrap">
    <div class="head head--split">
      <div><p class="kicker">Testimonials</p><h2>Voices from the GFS Family</h2></div>
      <p class="lead">From first-day drivers to multi-year veterans — here's what the people who work with us every day have to say.</p>
    </div>
    <div class="filter" role="group" aria-label="Filter reviews">{filt}<p class="filter__count" aria-live="polite">Showing <span data-count>{n}</span> reviews</p></div>
    <ul class="quotes quotes--cols">{"".join(quote(r, True) for r in REVIEWS)}</ul>
  </div>
</section>

<section class="section section--surface">
  <div class="wrap split split--even">
    <div>
      <p class="kicker">Why Trust GFS Reviews</p>
      <h2>Consistent Excellence Across Every Platform</h2>
      <p class="lead lead--gap">Our reputation isn't built on one platform — it's earned daily across every touchpoint.</p>
      <ul class="features features--stack">{"".join(f'<li class="feature">{icon(i)}<h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, t, d in trust)}</ul>
    </div>
    <div class="panel">
      <p class="score"><b>{AVG:.1f}</b><span>Based on {n} reviews</span></p>
      <ul class="bars">{breakdown}</ul>
    </div>
  </div>
</section>
"""
        + sign_cta(
            "Part of the GFS Family? We'd Love to Hear from You",
            "Your story matters. Sharing your experience helps us grow and helps others find a company they can trust.",
            [btn("Share Your Story", "contact-us.html", "white"), btn("Join Our Team", APPLY_URL, "ghost")],
        )
    )
    page("reviews.html", f"Reviews — {SITE}", f"Reviews of {SITE} from drivers, owner-operators and logistics partners.", body, "reviews.html", cta=False)


# ---------------------------------------------------------------- contact


CONSENTS = [
    (
        "sms_non_marketing",
        "By checking this box, I consent to receive non-marketing SMS/text messages from GFS GROUP LLC regarding my driver application, recruiting updates, interview scheduling, qualification follow-ups, document reminders, onboarding reminders, support replies, and other job opportunity-related notifications. Message frequency may vary. Message and data rates may apply. Reply HELP for help and STOP to opt out at any time.",
    ),
    (
        "sms_marketing",
        "By checking this box, I consent to receive marketing SMS/text messages from GFS GROUP LLC regarding company news, announcements, recruiting campaigns, promotional updates, and special offers. Message frequency may vary. Message and data rates may apply. Reply HELP for help and STOP to opt out at any time.",
    ),
]
SEE_LEGAL = 'See our <a href="privacy-policy.html">Privacy Policy</a> and <a href="terms-of-service.html">Terms of Service</a> for more information.'


def field(fid, name, label, *, type_="text", required=False, full=False, ghl="", **attrs):
    """One labelled input. `ghl` is the field id in the current GoHighLevel form."""
    extra = "".join(f' {k}="{v}"' for k, v in attrs.items())
    opt = "" if required else ' <span class="opt">(optional)</span>'
    req = ' required aria-required="true"' if required else ""
    data = f' data-ghl="{ghl}"' if ghl else ""
    return (
        f'<div class="field{" field--full" if full else ""}"><label for="{fid}">{label}{opt}</label>'
        f'<input id="{fid}" name="{name}" type="{type_}"{req}{data}{extra} aria-describedby="{fid}-err">'
        f'<p class="field__error" id="{fid}-err" hidden></p></div>'
    )


def contact_form():
    """Same fields and consent text as the current form. Not connected to an API yet:
    with an empty data-endpoint the script runs in preview mode and sends nothing."""
    consents = "".join(
        f'<label class="consent"><input type="checkbox" name="{name}" value="yes"><span>{e(text)} {SEE_LEGAL}</span></label>'
        for name, text in CONSENTS
    )
    return f"""
<form class="form" id="{FORM_ID}" novalidate data-contact-form data-endpoint="" data-phone="{PHONE_SHORT}" data-tel="{TEL}">
  <h3 class="form__title">Connect with us</h3>
  <div class="form__alert" data-form-alert hidden tabindex="-1" role="alert"></div>
  <div class="form__grid">
    {field("f-job", "job_title", "What is your job title?", full=True, ghl="6D2PoyFxTST09BCwNkpY", autocomplete="organization-title", maxlength="80")}
    {field("f-first", "first_name", "First name", required=True, autocomplete="given-name", maxlength="60")}
    {field("f-last", "last_name", "Last name", required=True, autocomplete="family-name", maxlength="60")}
    {field("f-phone", "phone", "Phone", type_="tel", required=True, autocomplete="tel", inputmode="tel", maxlength="24")}
    {field("f-email", "email", "Email", type_="email", required=True, autocomplete="email", maxlength="120")}
    {field("f-zip", "zip", "ZIP code", ghl="XHDk5N7KdxAGzKoQE9yX", autocomplete="postal-code", inputmode="numeric", maxlength="10")}
    <div class="field"><label for="f-exp">Over-the-Road driving experience? <span class="opt">(optional)</span></label>
      <select id="f-exp" name="otr_experience" data-ghl="9zCsX3p5J01hf8BS5FoK"><option value="">Select one</option><option>Less than 1 year</option><option>1-2 years</option><option>More than 2 years</option></select></div>
    <fieldset class="field field--full"><legend>Do you have a valid Class A CDL? <span class="opt">(optional)</span></legend>
      <div class="choices"><label class="choice"><input type="radio" name="cdl_class_a" value="Yes" data-ghl="WeIknCSsFKR4GzYIPF8m">Yes</label><label class="choice"><input type="radio" name="cdl_class_a" value="No">No</label></div></fieldset>
  </div>
  <div class="consents">{consents}</div>
  <div class="form__foot">
    <button class="btn btn--primary" type="submit" data-form-submit>Send Message</button>
    <p class="form__links"><a href="privacy-policy.html">Privacy Policy</a> | <a href="terms-of-service.html">Terms of Service</a></p>
  </div>
</form>
<div class="sign form-done" data-form-done hidden tabindex="-1">
  <h3>Message sent</h3>
  <p>We will get back to you shortly.</p>
  <p class="form-done__note" data-form-preview hidden>Preview: the form is not connected yet, so nothing was sent.</p>
  <button class="btn btn--white" type="button" data-form-again>Send another message</button>
</div>"""


def contact():
    rows_ = [
        ("Call Us", f'<a href="{TEL}">{PHONE_SHORT}</a>'),
        ("Email Us", f'<a href="mailto:{EMAIL}">{EMAIL}</a>'),
        ("Visit Us", e(ADDRESS)),
        ("Working Hours", "".join(f"<span>{e(h)}</span>" for h in HOURS)),
    ]
    body = (
        page_hero(clean(S["contact.heroTitle"]), S["contact.heroSubtitle"])
        + f"""
<section class="section">
  <div class="wrap contact-grid">
    <div>
      <h2>{e(S["contact.formTitle"])}</h2>
      <p class="lead lead--gap">{e(S["contact.formSubtitle"])}</p>
      {contact_form()}
    </div>
    <div class="contact-side">
      {mileage(rows_)}
      <div class="hq">
        <h2 class="h3">Our Headquarters</h2>
        <p>{e(ADDRESS)}</p>
      </div>
      <div class="map"><iframe src="{e(MAP_EMBED)}" title="Map showing {e(ADDRESS)}" loading="lazy"></iframe></div>
      {btn(icon("pin") + "Get Directions", MAP_URL, "blue")}
    </div>
  </div>
</section>
"""
    )
    page("contact-us.html", f"Contact — {SITE}", f"Call, email or message {SITE} in Maryland Heights, MO. Open Monday to Saturday.", body, "contact-us.html", cta=False)


# ------------------------------------------------------------------ legal

LINK = re.compile(r"(https?://[^\s<]+)|([\w.+-]+@[\w-]+\.[\w.-]+)")


def linkify(text):
    def sub(m):
        if m.group(1):
            return f'<a href="{m.group(1)}">{m.group(1)}</a>'
        return f'<a href="mailto:{m.group(2)}">{m.group(2)}</a>'

    return LINK.sub(sub, text)


def rich(text):
    """Plain text with blank-line paragraphs and '- ' bullets to HTML."""
    out, para, items = [], [], []

    def flush():
        if para:
            out.append("<p>" + "<br>".join(para) + "</p>")
            para.clear()
        if items:
            out.append("<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>")
            items.clear()

    for line in clean(text).split("\n"):
        line = line.strip()
        if not line:
            flush()
        elif line.startswith("- "):
            if para:
                flush()
            items.append(linkify(e(line[2:])))
        else:
            if items:
                flush()
            para.append(linkify(e(line)))
    flush()
    return "".join(out)


OLD_PHONE = re.compile(r"\+?1?[-.\s]*\(?314\)?[-.\s]*451[-.\s]*1111")


def one_contact(text):
    """Legal pages carried a second phone and email; use the site-wide ones."""
    return OLD_PHONE.sub(PHONE, text).replace(EMAIL_HR, EMAIL)


def legal(file, title, key):
    sections = json.loads(S[f"legal.{key}.sections"])
    for s in sections:
        s["content"] = one_contact(s["content"])
    toc = "".join(f'<li><a href="#s{i}">{e(s["title"])}</a></li>' for i, s in enumerate(sections, 1))
    prose = "".join(f'<h2 id="s{i}">{i}. {e(s["title"])}</h2>{rich(s["content"])}' for i, s in enumerate(sections, 1))
    body = (
        page_hero(title, f'Effective Date: {clean(S[f"legal.{key}.lastUpdated"])}', buttons=[btn("Back to Home", "index.html", "line")])
        + f"""
<section class="section">
  <div class="wrap legal">
    <nav class="toc" aria-label="On this page"><h2>On this page</h2><ol>{toc}</ol></nav>
    <div class="prose"><p class="intro">{e(S[f"legal.{key}.intro"])}</p>{prose}</div>
  </div>
</section>
"""
    )
    page(file, f"{title} — {SITE}", f"{title} for the {SITE} website and services.", body)


if __name__ == "__main__":
    home()
    why_us()
    services()
    partners()
    reviews()
    contact()
    legal("privacy-policy.html", "Privacy Policy", "privacy")
    legal("terms-of-service.html", "Terms of Service", "terms")
