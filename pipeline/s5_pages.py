"""Page templates for step 5: the landing page, the brief, the write-up and the data quality report.

Direction: the brief exists to support one decision, how a Local School Board shares out its
Special Education Fund. So the brief opens with the decision, sorts schools by the kind of help
the data points to, and keeps the evidence behind it. Colours follow DBM COMPASS (blue #0038A8,
yellow #FDBD10, slate neutrals) so it can sit beside it. Layout rules after heydamir/unslop (CC BY 4.0).
"""
import zlib
from html import escape as e

from common import LEVELS, LEVEL_LABELS

NAME = "PISARA"                  # product name; change here only
TAGLINE = "School Board Brief"
ACRONYM = [("P", "ublic"), ("I", "nformation for"), ("S", "chool"), ("A", "llocation and"), ("R", "esource"), ("A", "ccountability")]
README_URL = ""                    # full write-up, e.g. a shared Google Doc. Empty: the built-in about.html

LEVEL_COLORS = ["#C2410C", "#EA9A62", "#F3D9A4", "#9DB7E4", "#0038A8"]
LEVEL_INK = ["#fff", "#0F172A", "#0F172A", "#0F172A", "#fff"]
ATTRIBUTION = ("School data: Department of Education, Project Bukas machine-ready files, used under DepEd's Terms of Use "
               "and Fair Use Policy. Tax allotment data: DBM COMPASS public export. Special Education Fund data: "
               "Bureau of Local Government Finance (BLGF), FY2025 preliminary. This is an independent prototype. "
               "It is not produced, reviewed or endorsed by DepEd, DBM or BLGF.")

# BLGF reports SEF spending by office; the brief folds the twelve offices into six plain purposes.
SEF_PURPOSES = [
    ("Elementary schools", ["Elementary School"]),
    ("Secondary schools", ["Secondary School"]),
    ("General administration", ["General Administration"]),
    ("Sports facilities", ["Maintenance Of Sports Center, Athletic Fields, Playground"]),
    ("Other education services", ["Education Subsidiary Services", "Vocational/Technical School",
                                  "University/College Education School", "Adult Education",
                                  "Manpower Development Management Tool", "Others"]),
    ("Debt payments", ["Loan Amortization-Domestic(Debt Service-Principal)",
                       "Interest Payment-Domestic(Debt Service-Interest)"]),
]

ORG_DEPED = ("<abbr class='org deped' title='Department of Education'><svg viewBox='0 0 24 24' fill='none' stroke-width='2' "
             "stroke-linecap='round' stroke-linejoin='round' aria-hidden='true'><path d='M2 5h7a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H2zM22 5h-7a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h8z'/></svg>DepEd</abbr>")
ORG_DBM = ("<abbr class='org dbm' title='Department of Budget and Management'><svg viewBox='0 0 24 24' fill='none' stroke-width='2' "
           "stroke-linecap='round' stroke-linejoin='round' aria-hidden='true'><path d='M3 21h18M5 21V10M10 21V10M14 21V10M19 21V10M2 10l10-6 10 6'/></svg>DBM</abbr>")

ORG_BLGF = ("<abbr class='org dbm' title='Bureau of Local Government Finance'><svg viewBox='0 0 24 24' fill='none' stroke-width='2' "
            "stroke-linecap='round' stroke-linejoin='round' aria-hidden='true'><circle cx='12' cy='12' r='8'/><path d='M12 8v8M9.5 10.5h4a1.5 1.5 0 0 1 0 3h-3'/></svg>BLGF</abbr>")

CSS = """
:root{--desk:#F1F5F9;--paper:#fff;--ink:#0F172A;--sec:#334155;--mut:#64748B;--line:#E2E8F0;--soft:#F8FAFC;
--accent:#0038A8;--tint:rgba(0,56,168,.07);--gold:#FDBD10;--goldtint:#FFF7DB;--need:#B42318;
--g0:#C2410C;--g1:#EA9A62;--g2:#F3D9A4;--g3:#9DB7E4;--sel:#2F6BFF;
--sans:"Public Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--head:"Bricolage Grotesque","Public Sans",system-ui,sans-serif}
*{box-sizing:border-box}html{color-scheme:light;scroll-behavior:smooth}
body{margin:0;background:var(--desk);color:var(--ink);font:400 15px/1.6 var(--sans);font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-underline-offset:3px;text-decoration-thickness:1px}a:hover{color:var(--ink)}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:2px}
.in{max-width:1096px;margin:0 auto;padding:0 24px}
.rib{background:var(--accent);color:#fff;border-bottom:4px solid var(--gold)}
.rib .in{padding-top:12px;padding-bottom:12px;display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}
.rib .name{font:600 22px/1 var(--head);color:#fff;text-decoration:none;display:flex;align-items:baseline;gap:12px}
.rib .name span{font:400 14px/1.3 var(--sans);color:rgba(255,255,255,.72)}.rib .name span b{font-weight:600;color:#fff}
.intro h1 em{font-style:italic;color:var(--accent)}
.pitch{margin:0 0 32px;border-top:1px solid var(--line)}
.pitch div{display:grid;grid-template-columns:76px 1fr;gap:0 20px;padding:14px 0;border-bottom:1px solid var(--line)}
.pitch dt{font-weight:600;font-size:14px;line-height:1.75}.pitch dd{margin:0;font-size:16.5px;line-height:1.55;color:var(--sec)}.pitch strong{font-weight:600;color:var(--ink)}
.pitch .p dt{color:var(--g0)}.pitch .d dt{color:var(--mut)}.pitch .s dt{color:var(--accent)}
.org{display:inline-flex;align-items:center;gap:4px;padding:0 7px 0 2px;border-radius:999px;font-weight:600;font-size:.86em;line-height:1.45;vertical-align:middle;margin-top:-.15em;white-space:nowrap;text-decoration:none}
.org svg{width:16px;height:16px;flex:none;border-radius:50%;padding:2.5px}
.org.deped{background:#E6EDFA;color:var(--accent)}.org.deped svg{background:var(--accent);stroke:#fff}
.org.dbm{background:#E8ECF1;color:var(--ink)}.org.dbm svg{background:#334155;stroke:#fff}
.find{margin:0}.find label{display:block;font-weight:600;font-size:15px;color:var(--ink);margin:0 0 10px}
.find .row{display:flex;gap:10px}.find .box{position:relative;flex:1}
.find .box svg{position:absolute;left:14px;top:50%;transform:translateY(-50%);width:18px;height:18px;stroke:var(--mut);pointer-events:none}
.find .field{padding-left:42px;height:52px}.find .btn{height:52px;padding:0 22px;border:0;font:inherit;font-weight:600;cursor:pointer}
.find .cap{font-size:13.5px;color:var(--mut);margin:10px 0 0}
.sug{position:absolute;z-index:20;left:0;right:0;top:calc(100% + 6px);margin:0;padding:6px;list-style:none;background:var(--paper);border:1px solid var(--line);border-radius:10px;box-shadow:0 12px 32px -12px rgba(15,23,42,.3)}
.sug a{display:flex;justify-content:space-between;gap:12px;padding:10px 12px;border-radius:7px;color:var(--ink);text-decoration:none;font-size:15px}
.sug a span{color:var(--mut);font-size:13.5px;text-align:right}.sug a b{font-weight:600}
.sug li.on a,.sug a:hover{background:#E6EDFA}.sug .none{padding:10px 12px;font-size:14.5px;color:var(--sec)}.sug .none b{color:var(--ink);font-weight:600}
.exs{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:22px 0 0;font-size:14.5px;color:var(--sec)}
.exs a{display:inline-flex;align-items:center;height:40px;padding:0 18px;border:1px solid #CBD5E1;border-radius:999px;background:var(--paper);text-decoration:none;font-weight:500;color:var(--accent)}
.exs a:hover{border-color:var(--accent);color:var(--accent)}
.memo{display:grid;grid-template-columns:44px 1fr;gap:3px 12px;font-size:13px;margin:0 0 20px;padding:0 0 16px;border-bottom:1px solid var(--line)}
.memo dt{color:var(--mut)}.memo dd{margin:0;color:var(--sec)}.memo dd b{font-weight:600;color:var(--ink)}
.peek .top{display:flex;justify-content:space-between;align-items:center;margin:0 0 16px}.peek .top .kick{margin:0}
.engine{display:grid;grid-template-columns:1fr 1.15fr;gap:40px;align-items:center;margin:36px 0 0;padding:34px 36px;border-radius:12px;background:var(--accent);color:rgba(255,255,255,.86)}
.engine .k{margin:0 0 8px;font-size:14px;font-weight:600;color:var(--yel,#FDBD10)}
.engine h3{font:600 24px/1.25 var(--head);color:#fff;margin:0 0 12px;text-wrap:balance}.engine p{margin:0;font-size:15.5px}
.engine ul{list-style:none;margin:0;padding:0;display:grid;gap:12px}
.engine li{font-size:15px;padding-left:18px;position:relative}.engine li::before{content:"";position:absolute;left:0;top:.6em;width:7px;height:7px;border-radius:50%;background:#FDBD10}
.engine li b{color:#fff;font-weight:600;margin-right:6px}
.exh{margin:0 0 12px}.exh b{display:block;font:600 19px/1.3 var(--head);color:var(--ink)}.exh span{font-size:14.5px;color:var(--sec)}
.nb{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:var(--accent);color:#fff;font:600 11.5px/1 var(--sans);margin-right:8px;vertical-align:1px}
.prose code,.prose pre{font:13px/1.5 ui-monospace,"Cascadia Mono",Consolas,monospace;background:var(--soft);border:1px solid var(--line);border-radius:4px}
.prose code{padding:1px 5px}.prose pre{padding:12px 16px;overflow-x:auto;max-width:46em}
.prose table{margin-top:12px}.prose td{white-space:normal;text-align:left;color:var(--sec)}.prose th{text-align:left}
.glance{display:grid;grid-template-columns:repeat(4,1fr);margin:32px 0 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.glance div{padding:18px 20px 18px 0}.glance div+div{padding-left:20px;border-left:1px solid var(--line)}.glance b{display:block;font:600 28px/1.1 var(--head);color:var(--accent);margin-bottom:4px}.glance span{font-size:13.5px;color:var(--sec)}
.rib nav{display:flex;gap:4px;font-size:14px}.rib nav a{color:#fff;text-decoration:none;padding:6px 12px;border-radius:6px}
.rib nav a:hover{background:rgba(255,255,255,.14)}
.sheet{max-width:1048px;margin:32px auto 64px;background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:56px 72px 64px;animation:in .28s cubic-bezier(.2,.7,.2,1) both}
.wrap{padding:0 24px}
h1{font:600 40px/1.12 var(--head);letter-spacing:-.015em;margin:0 0 14px;text-wrap:balance;max-width:20em}
.deck{font-size:18px;line-height:1.5;color:var(--sec);margin:0;max-width:40em}
h2{font:600 24px/1.25 var(--head);margin:0 0 6px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
h3{font:600 17px/1.35 var(--sans);margin:0 0 4px}
.sn{flex:none;display:inline-grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--accent);color:#fff;font:600 14px/1 var(--sans)}
.sec{border-top:1px solid var(--line);margin-top:56px;padding-top:44px}
.lead{font-size:16px;color:var(--sec);margin:0 0 20px;max-width:44em}
.note{font-size:13.5px;color:var(--mut);margin:0 0 16px;max-width:52em}
.lbl{font-size:13.5px;font-weight:600;color:var(--ink);margin:0 0 8px}
.kick{font-size:14px;color:var(--sec);margin:0 0 14px}.kick b{color:var(--ink);font-weight:600}
.plan{font:500 12.5px/1 var(--sans);color:var(--accent);background:var(--tint);padding:6px 9px;border-radius:4px;white-space:nowrap}
.btn{display:inline-flex;align-items:center;gap:8px;height:44px;padding:0 18px;border-radius:8px;background:var(--accent);color:#fff;text-decoration:none;font-weight:500;font-size:15px}
.btn:hover{background:#002A80;color:#fff}.btn.ghost{background:var(--paper);color:var(--accent);border:1px solid #CBD5E1}.btn.ghost:hover{border-color:var(--accent);color:var(--accent)}
/* brief top */
.mh{display:grid;grid-template-columns:1fr 1.25fr 1fr;margin:0 0 40px;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.mh div{padding:12px 18px}.mh div+div{border-left:1px solid var(--line)}
.mh dt{font-size:12.5px;color:var(--mut);margin-bottom:2px}.mh dd{margin:0;font-size:14.5px;line-height:1.4;color:var(--ink)}
.mh .dec{background:var(--goldtint);box-shadow:inset 0 3px 0 var(--gold)}.mh .dec dd{font-weight:600}
.bl{font-size:20px;color:var(--ink);font-weight:500;margin-top:4px}
.facts{display:grid;grid-template-columns:repeat(3,1fr);margin:32px 0 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.facts div{padding:20px 24px 20px 0}.facts div+div{padding-left:24px;border-left:1px solid var(--line)}
.facts b{display:block;font:600 34px/1.05 var(--head);color:var(--ink);margin-bottom:6px}.facts div:first-child b{color:var(--g0)}
.facts b small{font:500 16px var(--sans);color:var(--mut)}
.facts span{font-size:14px;color:var(--sec);display:block;max-width:20em}
.meta{font-size:13px;color:var(--mut);margin:14px 0 0}
/* where to act */
.acts{list-style:none;margin:8px 0 0;padding:0;border-top:1px solid var(--line)}
.acts>li{display:grid;grid-template-columns:84px 1fr 150px;gap:0 24px;align-items:start;padding:20px 0;border-bottom:1px solid var(--line);scroll-margin-top:16px}
.acts .cnt{background:var(--k);color:var(--kt);border-radius:8px;padding:12px 0 10px;text-align:center;font-size:12.5px;line-height:1.2;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.acts .cnt b{display:block;font:600 30px/1 var(--head);margin-bottom:3px}
.acts h3{font:600 18px/1.3 var(--head);margin:2px 0 4px}.acts p{margin:0;color:var(--sec);max-width:40em}
.acts .lrn{font-size:12.5px;line-height:1.35;color:var(--mut);text-align:right;padding-top:4px}.acts .lrn b{display:block;font:600 20px/1.2 var(--head);color:var(--ink)}
.acts .zero{opacity:.55}.acts details{margin-top:8px}
/* planned and supporting detail */
.later>p.top .plan{margin-right:10px}
.lat2{display:grid;grid-template-columns:1fr 1fr;gap:24px}.lat2 h3{font:600 16px/1.3 var(--head)}.lat2 p{margin:0;font-size:14.5px;color:var(--sec)}
.supp{margin-top:72px}
h2.div{display:flex;align-items:center;gap:16px;font:600 15px/1 var(--sans);color:var(--mut);margin:0 0 8px}h2.div::after{content:"";flex:1;height:1px;background:#CBD5E1}
.supp .sub h3{font:600 16px/1.35 var(--head);margin-bottom:4px}.supp .sub.first{margin-top:28px}.supp .sub.first .bars{margin-top:12px}
/* five reading levels */
.bars{display:grid;grid-template-columns:132px 1fr;gap:8px 16px;align-items:center}
.bars .who{font-size:13.5px;color:var(--sec)}.bars .who b{font-weight:600;color:var(--ink)}
.bar{display:flex;height:32px;border-radius:4px;overflow:hidden}
.bar span{display:flex;align-items:center;justify-content:center;font-size:12.5px;font-weight:500;min-width:0;overflow:hidden}
.legend{display:flex;flex-wrap:wrap;gap:4px 18px;font-size:12.5px;color:var(--sec);margin:12px 0 0 148px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:7px}
.levels{margin-top:32px}
details{margin-top:14px;font-size:14px}summary{cursor:pointer;color:var(--accent);width:fit-content}
.names{columns:2;column-gap:32px;margin:10px 0 0;padding:0;list-style:none;color:var(--sec);font-size:13.5px}.names li{break-inside:avoid;padding:2px 0}
/* questions */
.ask{list-style:none;margin:8px 0 0;padding:0;counter-reset:q}
.ask li{counter-increment:q;display:grid;grid-template-columns:48px 1fr;gap:0 8px;padding:18px 0;border-top:1px solid var(--line);font-size:17px;line-height:1.5;max-width:52em}
.ask li:last-child{border-bottom:1px solid var(--line)}
.ask li::before{content:counter(q);font:600 22px/1.2 var(--head);color:var(--accent)}.ask b{font-weight:600}
/* planned */
.later{margin-top:56px;border:1px dashed #94A3B8;border-radius:10px;padding:32px 36px;background:var(--soft)}
.later>p.top{margin:0 0 28px;font-size:14px;color:var(--sec)}.later .sec{margin-top:36px;padding-top:32px;border-color:#CBD5E1}.later>.sec:first-of-type{margin-top:0;padding-top:0;border:0}
.later table{background:var(--paper)}
.dots{width:100%;height:auto;display:block;margin-top:8px}.dots text{font:12px var(--sans);fill:var(--mut)}.dots .lab{fill:var(--ink);font-weight:500}
.dots circle{fill:var(--accent);fill-opacity:.28;stroke:var(--accent);stroke-width:1}.dots circle:hover{fill-opacity:.8}
.tw{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:14px}
th,td{padding:8px 12px 8px 0;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap;vertical-align:baseline}
th:last-child,td:last-child{padding-right:0}th:first-child,td:first-child{text-align:left;white-space:normal}
.later td,.later th{padding-left:12px;padding-right:12px}
th{white-space:normal;line-height:1.3;font-weight:500;font-size:13px;color:var(--mut);vertical-align:bottom;border-bottom-color:var(--sec)}
td.me{font-weight:600}.up{color:var(--need)}td.no{color:var(--mut)}tr.grp td{font-weight:600;color:var(--ink);padding-top:20px;text-align:left}
tbody tr:hover td{background:var(--soft)}
.sub{margin-top:44px}
.fine{font-size:13px;color:var(--mut);margin:0;padding-left:16px;max-width:56em}.fine li{margin-bottom:4px}
.sef{margin:8px 0 14px}.sef .tot td{font-weight:600;border-top:1px solid var(--ink)}
.sb{display:inline-block;width:90px;height:8px;background:var(--line);border-radius:2px;margin-right:8px;vertical-align:middle;overflow:hidden}
.sb i{display:block;height:100%;background:#334155}
.sef td:nth-child(2),.sef td:nth-child(3){white-space:nowrap}
@media (max-width:560px){.sb{width:36px;margin-right:6px}.sef th,.sef td{padding-left:6px;padding-right:6px}}
@media print{.sb,.sb i{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.field{font:inherit;font-size:15px;height:48px;padding:0 14px;border:1px solid #CBD5E1;border-radius:8px;background:var(--paper);color:var(--ink);width:100%}
.field:focus{outline:2px solid var(--accent);outline-offset:1px;border-color:var(--accent)}
.tools{display:grid;grid-template-columns:1fr 220px;gap:12px;margin:16px 0 8px;align-items:center}
/* landing */
.intro{display:grid;grid-template-columns:1fr 464px;gap:52px;align-items:start;padding-top:56px;padding-bottom:56px}
.intro h1{font-size:52px;line-height:1.06;margin-bottom:24px;max-width:none}.intro .deck{margin-bottom:28px}.intro .start{font-size:15px;color:var(--sec);margin:14px 0 0}
.name-note{font-size:13px;color:var(--mut);margin:32px 0 0;max-width:34em}.name-note b{color:var(--accent);font-weight:600}
.peek{display:block;background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:28px 30px 24px;color:var(--ink);text-decoration:none;transition:border-color .16s,box-shadow .16s}
.peek:hover{border-color:var(--accent);color:var(--ink);box-shadow:0 8px 24px -12px rgba(15,23,42,.25)}
.peek .ph{font:600 22px/1.2 var(--head);margin:0 0 22px;text-wrap:balance}
.peek .bars{grid-template-columns:112px 1fr;gap:6px 12px}.peek .bar{height:26px}.peek .legend{margin:10px 0 0;font-size:12px;gap:2px 12px}
.peek .ph{margin-bottom:0}.peek .memo{margin-bottom:14px;padding-bottom:14px}
.peek .part+.part{margin-top:22px;padding-top:20px;border-top:1px solid var(--line)}
.peek .go{display:block;margin-top:20px;font-weight:500;color:var(--accent)}
.peek .pbl{margin:8px 0 0;font-size:15px;color:var(--sec)}
.pf{display:grid;grid-template-columns:repeat(3,1fr)}.pf div{padding-right:12px}.pf div+div{padding-left:12px;border-left:1px solid var(--line)}
.pf b{display:block;font:600 24px/1.1 var(--head);margin-bottom:4px}.pf div:first-child b{color:var(--g0)}.pf b small{font:500 13px var(--sans);color:var(--mut)}
.pf span{display:block;font-size:12.5px;line-height:1.35;color:var(--sec)}
.pacts{list-style:none;margin:0;padding:0}.pacts li{display:grid;grid-template-columns:40px 1fr auto;gap:12px;align-items:center;padding:6px 0}
.pacts li+li{border-top:1px solid var(--line)}.pacts .pc{background:var(--k);color:var(--kt);border-radius:6px;text-align:center;font:600 17px/30px var(--head)}
.pacts span{font-size:14.5px;font-weight:500}.pacts small{font-size:12.5px;color:var(--mut)}
.band{background:var(--paper);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:64px 0}
.band h2{font-size:30px;margin-bottom:10px}
.who4{font-size:17px;color:var(--sec);max-width:44em;margin:0}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin:36px 0 0;padding:0;list-style:none;counter-reset:s}
.steps li{counter-increment:s;padding:24px 24px 26px;border:1px solid var(--line);border-radius:10px;color:var(--sec);font-size:15px;background:var(--paper)}
.steps li::before{content:counter(s);display:inline-grid;place-items:center;width:34px;height:34px;border-radius:50%;background:var(--accent);color:#fff;font:600 16px/1 var(--sans);margin-bottom:16px}
.steps b{display:block;font:600 19px/1.3 var(--head);color:var(--ink);margin-bottom:8px}
.cta{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:32px}.cta span{font-size:14px;color:var(--mut)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:20px;padding-top:56px}
.card{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:28px 32px}.card.next{background:transparent;border:1px dashed #94A3B8}
.card h3{font:600 20px/1.3 var(--head);margin-bottom:4px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}.card .note{margin-bottom:12px}
.card ul{margin:0;padding-left:18px;color:var(--sec)}.card li{margin-bottom:8px}
.prose p{max-width:46em;color:var(--sec);margin:8px 0 0}.prose ul,.prose ol{max-width:46em;color:var(--sec);padding-left:20px}.prose li{margin-bottom:6px}.prose h2{margin-top:44px}
.m{display:inline-block;position:relative;width:112px;height:8px;background:var(--line);border-radius:2px;vertical-align:middle;margin-right:12px}
.m i{position:absolute;inset:0 auto 0 0;background:var(--accent);border-radius:2px}.m u{position:absolute;top:-4px;bottom:-4px;width:2px;background:var(--ink)}
.key{font-size:13px;color:var(--mut);margin:0}.key .m{margin:0 8px 0 0}
@keyframes in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
@media (max-width:960px){.intro{grid-template-columns:1fr;gap:36px}.steps,.two{grid-template-columns:1fr}.sheet{padding:44px 40px 48px}
.engine{grid-template-columns:1fr;gap:24px;padding:28px 24px}.glance{grid-template-columns:1fr 1fr}.glance div:nth-child(3){padding-left:0;border-left:0}.glance div:nth-child(n+3){border-top:1px solid var(--line)}}
@media (max-width:700px){.sheet{padding:28px 20px 36px;margin-top:16px;border-radius:8px}.intro{padding-top:32px;padding-bottom:36px}.intro h1{font-size:36px}h1{font-size:28px}
.band{padding:44px 0}.band h2{font-size:24px}.in{padding:0 16px}.wrap{padding:0 12px}
.bars{grid-template-columns:1fr;gap:4px}.bars .who{margin-top:8px}.legend{margin-left:0}.tools{grid-template-columns:1fr}
.facts{grid-template-columns:1fr}.facts div,.facts div+div{padding:14px 0;border-left:0}.facts div+div{border-top:1px solid var(--line)}.facts b{font-size:28px}
.mh{grid-template-columns:1fr;margin-bottom:28px}.mh div+div{border-left:0;border-top:1px solid var(--line)}.mh div{padding:10px 14px}.bl{font-size:18px}
.acts>li{grid-template-columns:60px 1fr;gap:0 14px;padding:16px 0}.acts .cnt b{font-size:24px}.acts .lrn{grid-column:2;text-align:left;padding-top:8px}.acts .lrn b{display:inline;font-size:15px}
.lat2{grid-template-columns:1fr;gap:16px}.supp{margin-top:48px}
.names{columns:1}
.peek .bars{grid-template-columns:1fr;gap:4px}.bar span{font-size:11px}.ask li{grid-template-columns:32px 1fr;font-size:16px}.later{padding:22px 16px}.card{padding:22px 20px}.peek{padding:22px 18px}
.intro h1{margin-bottom:22px;font-size:40px}.br-d{display:none}.pitch div{grid-template-columns:1fr;gap:2px}.pitch dd{font-size:16px}.find .row{flex-direction:column}.find .btn{justify-content:center}.exs a{height:36px;padding:0 14px}
.hide-s{display:none}.rib .name{flex-direction:column;gap:4px}.rib .name span{font-size:11.5px}.rib nav{margin-left:-8px}.rib nav a{padding:6px 8px}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}html{scroll-behavior:auto}}
@media print{.org{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
@media print{body{background:#fff;font-size:11pt}.rib nav,.noprint{display:none!important}.rib,.bar span,.mh .dec{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.wrap{padding:0}.sheet{border:0;max-width:none;margin:0;padding:16pt 0 0;animation:none}
h2{break-after:avoid}table,.dots,.bars,.acts>li,.ask li,.later{break-inside:avoid}.appendix{break-before:page}a{color:inherit;text-decoration:none}summary{display:none}}
"""

FONTS = ("<link rel='preconnect' href='https://fonts.googleapis.com'><link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>"
         "<link href='https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600&family=Public+Sans:wght@400;500;600&display=swap' rel='stylesheet'>")


def readme_link(root=""):
    return README_URL or f"{root}about.html"


def acronym():
    return " ".join(f"<b>{a}</b>{rest}" for a, rest in ACRONYM)


def page(title, body, root=""):
    top = (f"<header class='rib'><div class='in'><a class='name' href='{root}index.html' aria-label='{NAME} home'>{NAME}<span>{acronym()}</span></a>"
           f"<nav><a href='{root}index.html#how'>How it works</a><a href='{root}index.html#find'>Find a locality</a>"
           f"<a href='{readme_link(root)}'>Technical write-up</a></nav></div></header>")
    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width,initial-scale=1'><title>{e(title)}</title>{FONTS}"
            f"<style>{CSS}</style></head><body>{top}{body}</body></html>")


def fmt(v, kind):
    if v is None:
        return "n/a"
    return f"{v * 100:.1f}%" if kind == "percent" else f"{v:.0f}"


def peso(v):
    if v >= 1e9:
        return f"₱{v / 1e9:,.2f} billion"
    return f"₱{v / 1e6:,.1f} million" if v >= 1e6 else f"₱{v:,.0f}"


def sef_purposes(sef):
    """(purpose, amount, share of spending) for each purpose with spending, in SEF_PURPOSES order."""
    out = []
    for label, offices in SEF_PURPOSES:
        amt = sum(sef["by_office"].get(o, 0) for o in offices)
        if amt > 0:
            out.append((label, amt, amt / sef["spent"]))
    return out


def sef_section(b, num):
    """What the fund was spent on last year: town-wide, as reported to BLGF. Describes; does not judge."""
    sef, name = b["money"]["special_education_fund"], e(b["name"])
    head = f"<section class='sec'><h2><span class='sn'>{num}</span>What the fund paid for in 2025</h2>"
    fine = ("<ul class='fine'><li>Town-wide totals from the local treasurer's Statement of Receipts and Expenditures, as reported to "
            "the Bureau of Local Government Finance (BLGF). FY2025, preliminary. They do not show which school received what.</li>"
            "<li>The purposes are the offices the treasurer charged. General administration can include costs that support schools.</li>"
            "<li>The province keeps its own share of the fund for schools across the province. That share is not shown here.</li></ul>")
    if not sef:
        return head + f"<p class='lead'>{name} is not yet matched to BLGF's Special Education Fund data.</p></section>"
    if not sef["spent"]:
        got = f"collected <b>{peso(sef['collected'])}</b> for the fund in 2025 but " if sef["collected"] else ""
        return (head + f"<p class='lead'>{name} {got}reported no spending from it to BLGF. This may mean the report was "
                f"not filed in time, not that nothing was spent. Ask the treasurer for the year's figures.</p>{fine}</section>")
    rows = "".join(
        f"<tr><td>{p}</td><td>{peso(a)}</td><td><span class='sb'><i style='width:{s * 100:.1f}%'></i></span>{s * 100:.0f}%</td></tr>"
        for p, a, s in sef_purposes(sef))
    lead = (f"{name} collected <b>{peso(sef['collected'])}</b> for the Special Education Fund from property tax in 2025 "
            f"and reported spending <b>{peso(sef['spent'])}</b> from it. This is what that spending was charged to.")
    return (head + f"<p class='lead'>{lead}</p><div class='tw'><table class='sef'><thead><tr><th>Purpose</th><th>Spent</th>"
            f"<th>Share of spending</th></tr></thead><tbody>{rows}<tr class='tot'><td>Total</td><td>{peso(sef['spent'])}</td>"
            f"<td>100%</td></tr></tbody></table></div>{fine}</section>")


def more_need(ind, val, ref):
    if val is None or ref is None:
        return False
    return (val > ref) if ind["higher_means"] == "more need" else (val < ref)


def bar(levels):
    cells = []
    for i, lv in enumerate(LEVELS):
        p = levels[lv] * 100
        cells.append(f"<span style='width:{p:.2f}%;background:{LEVEL_COLORS[i]};color:{LEVEL_INK[i]}' "
                     f"title='{LEVEL_LABELS[i]}: {p:.1f}%'>{f'{p:.0f}%' if p >= 7 else ''}</span>")
    return f"<div class='bar' role='img' aria-label='Share of learners at each reading level'>{''.join(cells)}</div>"


def level_bars(b):
    legend = "".join(f"<span><i style='background:{c}'></i>{l}</span>" for c, l in zip(LEVEL_COLORS, LEVEL_LABELS))
    return (f"<div class='bars'><div class='who'><b>{e(b['name'])}</b></div>{bar(b['values']['levels'])}"
            f"<div class='who'>{e(b['region'])}</div>{bar(b['benchmarks']['region']['levels'])}</div>"
            f"<div class='legend'>{legend}</div>")


def low(r, head):
    return r["values"][head] * r["learners_assessed"]


def groups(b, head):
    """Sort schools by the kind of help the two measures point to. Alphabetical inside each group, never ranked."""
    region = b["region"]
    spec = [
        ("Reading help and more room", True, True,
         f"More learners at the lowest reading level than {region}, and more learners per classroom.",
         "Put these schools first when the fund pays for classrooms or repairs, and send reading support with it."),
        ("Reading help", True, False,
         f"More learners at the lowest reading level than {region}. Classrooms are at or under the regional figure.",
         "Space is not the pressure here. Look at reading materials, teacher training and remedial sessions."),
        ("More room", False, True,
         f"Reading is at or better than {region}, but there are more learners per classroom.",
         "Consider these schools for classroom works, and ask what keeps their reading up."),
        ("Neither", False, False,
         f"At or better than {region} on both measures.",
         "Keep current support. These schools may have practice worth sharing with the others."),
    ]
    out = []
    for title, rd, room, why, do in spec:
        rows = [r for r in b["schools"] if bool(r["more_need_than_region"][head]) == rd
                and bool(r["more_need_than_region"].get("learners_per_classroom")) == room]
        out.append({"title": title, "why": why, "do": do, "schools": rows, "low": sum(low(r, head) for r in rows)})
    return out


def act_rows(gs):
    """One row per group: how many schools, what the board could do, and the learners involved."""
    html = ""
    for i, g in enumerate(gs):
        n = len(g["schools"])
        word = "school" if n == 1 else "schools"
        names = "".join(f"<li>{e(r['school_name'])}</li>" for r in g["schools"])
        html += (f"<li class='{'' if n else 'zero'}' id='g{i + 1}' style='--k:var(--g{i});--kt:{'#fff' if i == 0 else 'var(--ink)'}'>"
                 f"<div class='cnt'><b>{n}</b>{word}</div>"
                 f"<div><h3>{g['title']}</h3><p>{g['do'] if n else 'No schools in this group.'}</p>"
                 + (f"<details><summary>Show the {n} {word}</summary><ul class='names'>{names}</ul></details>" if n else "")
                 + f"</div><div class='lrn'><b>{g['low']:,.0f}</b> learners at the lowest reading level</div></li>")
    return html


def bottom_line(b, gs):
    """One sentence on where to start: the first non-empty group that needs reading help."""
    for i, rest in ((0, "both reading help and more room"), (1, "reading help")):
        n = len(gs[i]["schools"])
        if n:
            return f"Start with the {n} {'school that needs' if n == 1 else 'schools that need'} {rest}."
    return f"No school in {e(b['name'])} has more learners at the lowest reading level than {e(b['region'])}."


def dots(b, head):
    """One circle per school along the share-at-lowest-level axis. A distribution, not a ranked list."""
    W, L, R, mid = 760, 16, 16, 62
    x = lambda v: L + v * (W - L - R)
    top = max(r["learners_assessed"] for r in b["schools"])
    marks = []
    for r in sorted(b["schools"], key=lambda r: -r["learners_assessed"]):
        v = r["values"][head]
        jitter = (zlib.crc32(r["school_id"].encode()) % 1000 / 1000 - .5) * 68
        rad = 3 + 9 * (r["learners_assessed"] / top) ** .5
        marks.append(f"<circle cx='{x(v):.1f}' cy='{mid + jitter:.1f}' r='{rad:.1f}'><title>{e(r['school_name'])}: "
                     f"{v * 100:.0f}% of {r['learners_assessed']:,.0f} learners</title></circle>")
    ticks = "".join(f"<line x1='{x(t):.1f}' x2='{x(t):.1f}' y1='112' y2='116' stroke='#64748B'/>"
                    f"<text x='{x(t):.1f}' y='130' text-anchor='middle'>{t * 100:.0f}%</text>" for t in (0, .25, .5, .75, 1))
    rv = b["benchmarks"]["region"][head]
    anchor, dx = ("start", 6) if rv < .7 else ("end", -6)
    return (f"<svg class='dots' viewBox='0 0 {W} 136' role='img' aria-label='Each school by its share of learners at the lowest reading level'>"
            f"<line x1='{L}' x2='{W - R}' y1='112' y2='112' stroke='#64748B'/>{ticks}"
            f"<line x1='{x(rv):.1f}' x2='{x(rv):.1f}' y1='4' y2='112' stroke='#0F172A' stroke-dasharray='3 3'/>"
            f"<text class='lab' x='{x(rv) + dx:.1f}' y='14' text-anchor='{anchor}'>{e(b['region'])}, {rv * 100:.1f}%</text>"
            f"{''.join(marks)}</svg>")


def brief_html(b, indicators, head):
    v, reg = b["values"], b["benchmarks"]["region"]
    allp, div = b["benchmarks"]["all_published"], b["benchmarks"]["division"]
    name, region = e(b["name"]), e(b["region"])
    n = len(b["schools"])
    gs = groups(b, head)
    low_all = v[head] * v["learners_assessed"]

    nta = b["money"]["national_tax_allotment"]
    if nta and nta.get("FY 2027"):
        change = ""
        if nta.get("FY 2026"):
            d = (nta["FY 2027"] / nta["FY 2026"] - 1) * 100
            change = f", {'up' if d >= 0 else 'down'} {abs(d):.1f}% from 2026"
        nta_line = (f"For scale, {name}'s National Tax Allotment for 2027 is <b>{peso(nta['FY 2027'])}</b>{change}. "
                    f"That is the main national transfer to the locality and is not specific to education.")
    else:
        nta_line = f"{name} is not yet matched by name to DBM COMPASS, so its National Tax Allotment is not shown."

    a, bb, cc = gs[0], gs[1], gs[2]
    asks = []
    if a["schools"]:
        asks.append(f"<b>{len(a['schools'])} schools</b> need both reading help and more room. Are they first in line for next year's classroom and repair works?")
    if bb["schools"]:
        asks.append(f"<b>{len(bb['schools'])} schools</b> need reading help but are not crowded. What does the fund pay for there now: materials, training, or remedial sessions?")
    if cc["schools"]:
        asks.append(f"<b>{len(cc['schools'])} schools</b> read well but are crowded. Can classroom works there wait a year, or not?")
    sef = b["money"]["special_education_fund"]
    if sef and sef["spent"]:
        share = {p: s for p, _, s in sef_purposes(sef)}
        pct = lambda x: "less than 1%" if 0 < x < 0.005 else f"{x * 100:.0f}%"
        asks.append(f"<b>{low_all:,.0f} learners</b> are at the lowest reading level. In 2025, {pct(share.get('Elementary schools', 0))} of the fund's reported "
                    f"spending was charged to elementary schools and {pct(share.get('General administration', 0))} to general administration (section 3). "
                    f"How much of next year's fund goes to learning support, compared with buildings and operations?")
    else:
        asks.append(f"<b>{low_all:,.0f} learners</b> are at the lowest reading level. How much of the fund goes to learning support, compared with buildings and operations?")

    cols = [(b["name"], v, True), (b["region"], reg, False)]
    if div:
        cols.append((f"{div['name']} division", div, False))
    cols.append(("All published schools", allp, False))
    rows = ""
    for ind in indicators:
        cells = ""
        for _, vals, me in cols:
            up = me and more_need(ind, vals[ind["id"]], reg[ind["id"]])
            cells += f"<td class='{'me' if me else ''}{' up' if up else ''}'>{fmt(vals[ind['id']], ind['format'])}</td>"
        rows += f"<tr><td>{e(ind['label'])}</td>{cells}</tr>"
    compare = (f"<div class='tw'><table><thead><tr><th>Measure</th>{''.join(f'<th>{e(c)}</th>' for c, _, _ in cols)}</tr></thead>"
               f"<tbody>{rows}</tbody></table></div>")

    def school_rows(group):
        return "".join(
            f"<tr><td>{e(r['school_name'])}{'&nbsp;&dagger;' if r['small_group'] else ''}</td><td>{r['learners_assessed']:,.0f}</td>"
            f"<td>{low(r, head):,.0f}</td><td>{fmt(r['values']['reading_lowest'], 'percent')}</td>"
            f"<td>{fmt(r['values']['reading_grade_level'], 'percent')}</td>"
            f"<td>{fmt(r['values']['learners_per_teacher'], 'ratio')}</td>"
            f"<td>{fmt(r['values']['learners_per_classroom'], 'ratio')}</td></tr>" for r in group)

    all_rows = "".join(f"<tr class='grp'><td colspan='7'>{g['title']}, {len(g['schools'])} schools</td></tr>{school_rows(g['schools'])}"
                       for g in gs if g["schools"])
    appendix = (f"<input id='f' class='field noprint' type='search' placeholder='Filter schools' aria-label='Filter schools' style='max-width:320px;margin:12px 0 4px' "
                f"oninput=\"for(const tr of document.querySelectorAll('#all tr:not(.grp)'))"
                f"tr.hidden=!tr.cells[0].textContent.toLowerCase().includes(this.value.toLowerCase())\">"
                f"<div class='tw'><table><thead><tr><th>School</th><th>Learners assessed</th><th>At lowest level</th><th>Share at lowest level</th>"
                f"<th>At grade level</th><th>Learners per teacher</th><th>Learners per classroom</th></tr></thead>"
                f"<tbody id='all'>{all_rows}</tbody></table></div>")

    above = sum(1 for r in b["schools"] if r["more_need_than_region"][head])
    crowded = sum(1 for r in b["schools"] if r["more_need_than_region"].get("learners_per_classroom"))
    facts = (f"<div class='facts'><div><b>{v[head] * 100:.0f}%</b><span>of Grades 1 to 3 learners are at the lowest reading level. {region}: {reg[head] * 100:.0f}%</span></div>"
             f"<div><b>{above} <small>of {n}</small></b><span>schools have more of these learners than {region}</span></div>"
             f"<div><b>{crowded} <small>of {n}</small></b><span>schools have more learners per classroom than {region}</span></div></div>")

    body = f"""<div class='wrap'><main class='sheet'>
<dl class='mh'><div><dt>For</dt><dd>Local School Board of {name}, {e(b['province'])}</dd></div>
<div class='dec'><dt>Decision</dt><dd>How to share next year's Special Education Fund</dd></div>
<div><dt>Data</dt><dd>School year 2025&ndash;26, {b['schools_with_reading']} of {b['public_elementary_schools']} public elementary schools</dd></div></dl>
<h1>{low_all:,.0f} early-grade learners in {name} need the most help with reading</h1>
<p class='deck bl'>{bottom_line(b, gs)}</p>
{facts}

<section class='sec'><h2><span class='sn'>1</span>Where to act</h2>
<p class='lead'>Each school is compared with {region} on reading and on learners per classroom, then placed in one of four groups. Schools are grouped, never ranked.</p>
<ol class='acts'>{act_rows(gs)}</ol></section>

<section class='sec'><h2><span class='sn'>2</span>Questions for the meeting</h2>
<p class='lead'>Settle these before the fund is shared. The board knows conditions the data does not.</p>
<ol class='ask'>{''.join(f'<li><span>{q}</span></li>' for q in asks)}</ol></section>

{sef_section(b, 3)}

<div class='later'><p class='top'><span class='plan'>Planned for the fellowship</span>Empty until real figures are connected. Nothing here is estimated.</p>
<div class='lat2'><div><h3>Where the fund goes, school by school</h3><p>Which schools {name}'s fund reached and for what, from the quarterly SEF report, beside the groups above.</p></div>
<div><h3>After the meeting</h3><p>What the board decided for each group, the amount set aside, and whether it was spent.</p></div></div></div>

<section class='supp appendix'><h2 class='div'>Supporting detail</h2>
<p class='note'>The figures behind the groups, for anyone who wants to check them.</p>
<div class='sub first'><h3>How its learners read, against the region</h3>{level_bars(b)}
<p class='meta'>Reading: school year 2025&ndash;26. Teachers and classrooms: 2023&ndash;24. {v['learners_assessed']:,.0f} learners assessed.</p></div>
<div class='sub'><h3>How the schools are spread</h3><p class='note'>Each circle is one school, placed by its share of learners at the lowest level. Larger circles assessed more learners. Hover for the school</p>
{dots(b, head)}</div>
<div class='sub'><h3>{name} beside its region</h3><p class='note'>Figures in red show more need than {region}</p>{compare}</div>
<div class='sub'><h3>All {n} schools</h3><p class='note'>Alphabetical within each group</p>{appendix}</div>
<div class='sub'><h3>For scale</h3><p class='note'>{nta_line}</p></div>
<div class='sub'><h3>How to read this brief</h3>
<ul class='fine'><li>Schools are compared with a regional figure, not ranked. Schools work in different conditions, and DepEd's terms of use do not allow ranking.</li>
<li>The groups point to a kind of help to look into. They do not show that crowding causes low reading, or that spending will fix it.</li>
<li>Reading results are for school year 2025-26 only and are not compared across years. Classroom counts are from 2023-24; a school with no classroom count is treated as not crowded.</li>
<li>Regional figures cover the schools in DepEd's public reading file: five regions, {allp['schools']:,} schools.</li>
<li>&dagger; Fewer than 20 learners assessed. Percentages for small groups move a lot with one or two learners.</li>
<li>{ATTRIBUTION}</li></ul></div>
<p class='note noprint' style='margin-top:28px'><a href='javascript:print()'>Print this brief</a> &nbsp; <a href='../api/localities/{b['locality_id']}.json'>Download its data</a> &nbsp; <a href='{readme_link('../')}'>Technical write-up</a></p></section>
</main></div>
<script>addEventListener('beforeprint',()=>document.querySelectorAll('details').forEach(d=>d.open=true))</script>"""
    return page(f"{b['name']}, {b['province']} | {NAME}", body, "../")


def index_html(briefs, quality, manifest, featured):
    head = "reading_lowest"
    feats = [b for b in briefs if b["locality_id"] in featured]
    start = "".join(f"<a href='briefs/{b['locality_id']}.html'>{e(b['name'])}, {e(b['province'])}</a>" for b in feats)
    f0 = feats[0] if feats else briefs[0]
    f0_low = f0["values"][head] * f0["values"]["learners_assessed"]
    nb = lambda i, t: f"<p class='lbl'><span class='nb'>{i}</span>{t}</p>"
    # The example mirrors the brief's own order: bottom line, key figures, where to act.
    g0, v0, r0, n0 = groups(f0, head), f0["values"], f0["benchmarks"]["region"], len(f0["schools"])
    above0 = sum(1 for r in f0["schools"] if r["more_need_than_region"][head])
    crowd0 = sum(1 for r in f0["schools"] if r["more_need_than_region"].get("learners_per_classroom"))
    prows = "".join(
        f"<li style='--k:var(--g{i});--kt:{'#fff' if i == 0 else 'var(--ink)'}'><b class='pc'>{len(g['schools'])}</b>"
        f"<span>{g['title']}</span><small>{g['low']:,.0f} learners</small></li>" for i, g in enumerate(g0))
    peek = (f"<div class='exw'><p class='exh'><b>What every board gets</b>"
            f"<span>A one-page brief for its own city or town, built from public data.</span></p>"
            f"<a class='peek' href='briefs/{f0['locality_id']}.html' aria-label='Open the example brief for {e(f0['name'])}'>"
            f"<div class='part'>{nb(1, 'Who it is for, and the decision')}"
            f"<dl class='memo'><dt>To</dt><dd><b>Local School Board, {e(f0['name'])}, {e(f0['province'])}</b></dd>"
            f"<dt>Re</dt><dd>How to share next year's Special Education Fund</dd></dl>"
            f"<p class='ph'>{f0_low:,.0f} early-grade learners need the most help with reading</p>"
            f"<p class='pbl'>{bottom_line(f0, g0)}</p></div>"
            f"<div class='part'>{nb(2, 'What the data shows')}<div class='pf'>"
            f"<div><b>{v0[head] * 100:.0f}%</b><span>at the lowest reading level. {e(f0['region'])}: {r0[head] * 100:.0f}%</span></div>"
            f"<div><b>{above0} <small>of {n0}</small></b><span>schools behind the region on reading</span></div>"
            f"<div><b>{crowd0} <small>of {n0}</small></b><span>schools more crowded than the region</span></div></div></div>"
            f"<div class='part'>{nb(3, 'Where the board could act')}<ul class='pacts'>{prows}</ul></div>"
            f"<span class='go'>Open the full brief &rarr;</span></a></div>")

    rows = ""
    for b in sorted(briefs, key=lambda b: (b["region"], b["province"], b["name"])):
        val, rv = b["values"][head], b["benchmarks"]["region"][head]
        rows += (f"<tr data-n='{e((b['name'] + ' ' + b['province']).lower())}' data-r='{e(b['region'])}'>"
                 f"<td><a href='briefs/{b['locality_id']}.html'>{e(b['name'])}</a></td><td class='hide-s' style='text-align:left'>{e(b['province'])}</td>"
                 f"<td class='hide-s' style='text-align:left'>{e(b['region'])}</td><td>{len(b['schools'])}</td>"
                 f"<td class='hide-s'>{b['values']['learners_assessed']:,.0f}</td>"
                 f"<td><span class='m hide-s'><i style='width:{val * 100:.1f}%'></i><u style='left:{rv * 100:.1f}%'></u></span>{val * 100:.1f}%</td></tr>")
    regions = "".join(f"<option>{e(r)}</option>" for r in sorted({b["region"] for b in briefs}))
    schools = sum(len(b["schools"]) for b in briefs)

    n_src = sum(1 for m in manifest if m["status"] == "connected")
    body = f"""<section class='in intro'><div>
<h1>Where do our schools<br class='br-d'> need <em>help the most?</em></h1>
<dl class='pitch'>
<div class='p'><dt>Problem</dt><dd>School boards spend the Special Education Fund <strong>without seeing which schools need help.</strong></dd></div>
<div class='d'><dt>Data</dt><dd>The evidence is <strong>already public</strong>, split across {ORG_DEPED}, {ORG_DBM} and {ORG_BLGF} files never joined.</dd></div>
<div class='s'><dt>{NAME}</dt><dd>Joins them school by school and shows every board <strong>which schools need what, on one page.</strong></dd></div></dl>
<form class='find' onsubmit='return pick()'><label for='q'>Find your city or municipality</label>
<div class='row'><div class='box'><svg viewBox='0 0 24 24' fill='none' stroke-width='2' stroke-linecap='round'><circle cx='11' cy='11' r='7'/><path d='m20 20-3.5-3.5'/></svg>
<input id='q' class='field' type='search' autocomplete='off' placeholder='e.g. {e(f0['name'])}' role='combobox' aria-autocomplete='list' aria-expanded='false' aria-controls='sug'>
<ul id='sug' class='sug' role='listbox' hidden></ul></div><button class='btn' type='submit'>Get the brief</button></div>
<p class='cap'>Covers {len(briefs)} cities and municipalities, school year 2025&ndash;26</p></form>
<p class='exs'>Or see an example: {start}</p></div>{peek}</section>

<section class='band' id='how'><div class='in'>
<h2>How it works</h2>
<p class='who4'>For the Local School Board: the mayor, the schools division superintendent and the other members who decide how the Special Education Fund is shared.</p>
<div class='engine'><div><p class='k'>Behind the scenes</p><h3>{NAME} does the groundwork no board has time for</h3>
<p>Every brief starts from data the government already publishes. {NAME} turns it into something a board can act on, and keeps it current.</p></div>
<ul><li><b>Gathers</b>the public files from DepEd, DBM and BLGF, so no one has to hunt for them</li>
<li><b>Connects</b>every school's reading results, enrolment, teachers and classrooms into one record</li>
<li><b>Compares</b>each school with others in its region, fairly and without ranking</li>
<li><b>Explains</b>what it finds in plain language, and rebuilds whenever new data is out</li></ul></div>
<ol class='steps'>
<li><b>Open your city or town's brief</b>Search above. Each brief covers every public elementary school in the place.</li>
<li><b>See which schools need what</b>Every school sits in one of four groups: reading help, more classrooms, both, or neither, with what the board could do for each.</li>
<li><b>Settle the questions</b>The brief ends with the questions to settle before the fund is split, so the discussion starts from the same facts.</li></ol>
<div class='cta'><a class='btn' href='{readme_link()}'>Read the technical write-up</a><a class='btn ghost' href='quality.html'>Data quality report</a>
<span>Sources, joins, formulas and limits, in full.</span></div>
</div></section>

<div class='in two'>
<div class='card'><h3>Works today</h3><p class='note'>Built and checked against published data</p>
<ul><li>A brief for {len(briefs)} cities and municipalities in five regions, covering {schools:,} public elementary schools</li>
<li>Four groups of schools, with what the board could do for each and the questions to settle</li>
<li>What each city or town collected for its Special Education Fund in 2025, and what the spending was charged to</li>
<li>Every brief rebuilt from the published files with one command</li>
<li>The same content as open data: <a href='data/schools.csv'>schools</a>, <a href='data/localities.csv'>localities</a>, <a href='api/index.json'>JSON</a>, <a href='data/DATA_DICTIONARY.md'>dictionary</a></li></ul></div>
<div class='card next'><h3>Next, during the fellowship<span class='plan'>Planned</span></h3><p class='note'>December 2026 to March 2027</p>
<ul><li>Where the Special Education Fund goes school by school, from a pilot locality's quarterly reports</li>
<li>A record of what each board decided, and whether the money was spent</li>
<li>Location codes and DepEd spending straight from the COMPASS API</li>
<li>More regions and grade levels as DepEd publishes them, and briefs in Filipino</li></ul></div></div>

<div class='wrap'><main class='sheet' id='find' style='margin-top:20px'>
<h2>{len(briefs)} cities and municipalities with a brief</h2>
<p class='note'>DepEd's public reading file covers five regions. A locality has a brief when at least 90% of its public elementary schools are in it</p>
<div class='tools noprint'><span class='key'><span class='m'><i style='width:40%'></i><u style='left:60%'></u></span>Bar: learners at the lowest reading level. Line: the region</span>
<select id='r' class='field' aria-label='Region'><option value=''>All regions</option>{regions}</select></div>
<div class='tw'><table><thead><tr><th>Locality</th><th class='hide-s' style='text-align:left'>Province</th><th class='hide-s' style='text-align:left'>Region</th>
<th>Schools</th><th class='hide-s'>Learners assessed</th><th>At lowest reading level</th></tr></thead><tbody id='t'>{rows}</tbody></table></div>
<p id='none' class='note' hidden style='margin-top:16px'>No brief for that place yet. The public reading data covers five regions</p>
<p class='note' style='margin-top:32px'>{ATTRIBUTION}</p>
</main></div>
<script>
const q=document.getElementById('q'),r=document.getElementById('r'),t=document.getElementById('t'),none=document.getElementById('none');
function go(){{let n=0;for(const tr of t.rows){{const ok=!r.value||tr.dataset.r===r.value;tr.hidden=!ok;n+=ok}}none.hidden=n>0}}
r.addEventListener('change',go);
const sug=document.getElementById('sug'),norm=s=>s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
const all=[...t.rows].map(tr=>({{n:tr.cells[0].textContent,p:tr.cells[1].textContent,h:tr.querySelector('a').href}}));
let hits=[],cur=-1;
function hideSug(){{sug.hidden=true;q.setAttribute('aria-expanded','false')}}
function mark(){{[...sug.children].forEach((li,i)=>li.classList.toggle('on',i===cur))}}
function show(){{const s=norm(q.value.trim());cur=-1;sug.textContent='';if(!s)return hideSug();
hits=all.filter(x=>norm(x.n+' '+x.p).includes(s)).sort((a,b)=>norm(b.n).startsWith(s)-norm(a.n).startsWith(s)).slice(0,6);
if(hits.length)for(const x of hits){{const li=document.createElement('li'),a=document.createElement('a'),b=document.createElement('b'),sp=document.createElement('span');
li.setAttribute('role','option');a.href=x.h;b.textContent=x.n;sp.textContent=x.p;a.append(b,sp);li.append(a);sug.append(li)}}
else{{const li=document.createElement('li'),b=document.createElement('b');li.className='none';b.textContent=q.value.trim();
li.append(b,' is not in the data yet. Briefs cover {len(briefs)} cities and municipalities in five regions.');sug.append(li)}}
sug.hidden=false;q.setAttribute('aria-expanded','true')}}
q.addEventListener('input',show);q.addEventListener('focus',()=>q.value&&show());
q.addEventListener('keydown',ev=>{{if(sug.hidden||!hits.length)return;if(ev.key==='ArrowDown'||ev.key==='ArrowUp'){{ev.preventDefault();
cur=(cur+(ev.key==='ArrowDown'?1:-1)+hits.length)%hits.length;mark()}}else if(ev.key==='Escape')hideSug()}});
document.addEventListener('click',ev=>{{if(!ev.target.closest('.find'))hideSug()}});
function pick(){{show();const x=hits[cur<0?0:cur];if(q.value.trim()&&x)location.href=x.h;else q.focus();return false}}
</script>"""
    return page(f"{NAME} | {TAGLINE}", body)


def about_html(quality, briefs, manifest, indicators, rules):
    schools = sum(len(b["schools"]) for b in briefs)
    learners = sum(b["values"]["learners_assessed"] for b in briefs)
    conn = [m for m in manifest if m["status"] == "connected"]
    plan = [m for m in manifest if m["status"] != "connected"]
    joined = quality["reading_schools_matched"] / quality["reading_file_schools"]
    src_rows = "".join(
        f"<tr><td><b>{e(m['title'])}</b><br>{e(m['publisher'])}</td><td>{e(m['period'])}</td><td>{e(m.get('key') or '')}</td>"
        f"<td>{'Connected' if m['status'] == 'connected' else 'Planned: ' + e(m.get('needs') or '')}</td></tr>" for m in manifest)
    ind_rows = "".join(
        f"<tr><td><b>{e(i['label'])}</b><br><code>{e(i['id'])}</code></td><td><code>{e(i['numerator'])}</code> / <code>{e(i['denominator'])}</code><br>{e(i['note'])}</td>"
        f"<td>{'Higher' if i['higher_means'] == 'more need' else 'Lower'} means more need</td></tr>" for i in indicators)
    body = f"""<div class='wrap'><main class='sheet prose'>
<h1>Technical write-up</h1>
<p class='deck'>How {NAME} turns {len(conn)} public files into {len(briefs)} decision briefs, and what every number in a brief means. Written for reviewers, engineers and analysts.</p>
<div class='glance'><div><b>{len(conn)}</b><span>public sources connected, {len(plan)} more planned</span></div>
<div><b>{quality['public_elementary_schools']:,}</b><span>public elementary schools lined up</span></div>
<div><b>{joined:.1%}</b><span>of reading results joined by School ID</span></div>
<div><b>{len(briefs)}</b><span>briefs, {schools:,} schools, {learners:,.0f} learners</span></div></div>

<h2>1. The problem</h2>
<p>Every city and municipality has a Local School Board that budgets the Special Education Fund (SEF), an extra 1% tax on real property, each year.
Boards decide with little school-by-school evidence. The evidence is public, but it sits in separate DepEd files from different years,
and the money sits with DBM and BLGF. Nobody on a board has time to join them.</p>
<p>{NAME} is that join, done once, the same way for every locality, and turned into the one thing a board uses: a short brief that sorts its schools
by the kind of help the data points to.</p>

<h2>2. Architecture</h2>
<p>A five-step batch pipeline in Python, standard library only. Each step reads the previous step's output from <code>build/</code> and writes its own,
so any step can be rerun and inspected alone. Indicators, brief rules and sources are settings files (<code>indicators.json</code>, <code>sources.json</code>), not code.</p>
<pre>python pipeline/run.py --accept-deped-terms</pre>
<div class='tw'><table><thead><tr><th style='min-width:6.5em'>Step</th><th>Script</th><th>Does</th><th>Writes</th></tr></thead><tbody>
<tr><td>1 Collect</td><td><code>s1_collect.py</code></td><td>Downloads each connected source once, unzips safely, records file size, SHA-256 and retrieval date</td><td><code>1_manifest.json</code></td></tr>
<tr><td>2 Line up</td><td><code>s2_lineup.py</code></td><td>One record per public elementary school, keyed by DepEd School ID; one record per city or municipality, matched to COMPASS and BLGF</td><td><code>2_schools.json</code>, <code>2_localities.json</code>, <code>2_quality.json</code></td></tr>
<tr><td>3 Measure</td><td><code>s3_measure.py</code></td><td>Every indicator for every school, and learner-weighted benchmarks for each region, division and the whole file</td><td><code>3_measures.json</code></td></tr>
<tr><td>4 Group</td><td><code>s4_group.py</code></td><td>Applies the coverage rule, compares each school with its region, attaches the locality's money fields</td><td><code>4_briefs.json</code></td></tr>
<tr><td>5 Publish</td><td><code>s5_publish.py</code></td><td>Brief pages, JSON API, CSV extracts, data dictionary, this write-up and the data quality report</td><td><code>site/</code></td></tr>
</tbody></table></div>

<h2>3. Sources</h2>
<p>Each connected file's checksum is listed in the <a href='quality.html'>data quality report</a>, so anyone can confirm they are working from the same files.</p>
<div class='tw'><table><thead><tr><th>Source</th><th>Period</th><th>Join key</th><th>Status</th></tr></thead><tbody>{src_rows}</tbody></table></div>

<h2>4. Joining the data</h2>
<ul><li><b>Schools.</b> The enrolment file defines the universe: public schools offering elementary grades, {quality['public_elementary_schools']:,} in all. Reading results, personnel and facilities join on the six-digit School ID.
{quality['reading_schools_matched']:,} of {quality['reading_file_schools']:,} schools in the reading file joined ({joined:.2%}); {quality['reading_schools_unmatched']} did not. Personnel and facilities joined for {quality['schools_with_personnel']:,} schools.</li>
<li><b>Localities.</b> Schools roll up to a city or municipality by province and municipality name. Names are normalised (accents, case, “City of”, text in brackets removed) and matched to the COMPASS export. Where a city and a municipality share a name, DepEd's own wording decides.
{quality['localities_matched_to_compass']:,} of {quality['localities']:,} localities matched. Name matching is a stopgap: the COMPASS API carries ten-digit PSGC codes, which replace it once a key is issued.</li>
<li><b>Special Education Fund.</b> The same province and name match links each locality to BLGF's FY2025 SEF workbook: property-tax income, and spending by the office it was charged to.
{quality['localities_matched_to_sef']:,} of {quality['localities']:,} localities matched, and every locality with a brief. The brief folds BLGF's twelve offices into six purposes and shows them as reported, without judging them.</li>
<li><b>Eligibility.</b> DepEd's public reading file covers five regions. A locality gets a brief only when at least {rules['min_coverage']:.0%} of its public elementary schools are in that file and it has at least {rules['min_schools']} such schools, so a brief never speaks for schools it cannot see.</li></ul>

<h2>5. Measures</h2>
<p>Every measure is a ratio of two school fields, defined in <code>indicators.json</code>. A group's value (a city, a division, a region) is the sum of numerators over the sum of denominators,
so each school counts in proportion to its learners. Benchmarks use only schools with published reading results, so a school is compared with schools measured the same way.</p>
<div class='tw'><table><thead><tr><th>Measure</th><th>Formula and source</th><th>Direction</th></tr></thead><tbody>{ind_rows}</tbody></table></div>

<h2>6. From measures to groups</h2>
<p>Each school is checked against its regional benchmark on two questions. Is its share of learners at the lowest reading level (Low Emerging) higher than the region's?
Are its learners per classroom higher than the region's? The two answers give four groups:</p>
<div class='tw'><table><thead><tr><th></th><th>More learners per classroom</th><th>At or under the region</th></tr></thead><tbody>
<tr><td><b>More at the lowest reading level</b></td><td>Reading help and more room</td><td>Reading help</td></tr>
<tr><td><b>At or under the region</b></td><td>More room</td><td>Neither</td></tr></tbody></table></div>
<ul><li>Each group carries a kind of help to look into, written into the brief. The board decides; the brief does not allocate money.</li>
<li>Schools are listed alphabetically inside a group. No score, rank or league table is produced anywhere in the pipeline.</li>
<li>Schools with fewer than {rules['small_group']} learners assessed are marked, because one or two learners move their percentages a lot.</li>
<li>A school with no classroom count is treated as not crowded rather than guessed.</li></ul>

<h2>7. Outputs</h2>
<ul><li><b>Briefs:</b> <code>briefs/&lt;locality_id&gt;.html</code>, one per locality, printable.</li>
<li><b>JSON API:</b> <a href='api/index.json'><code>api/index.json</code></a> lists every locality; <code>api/localities/&lt;locality_id&gt;.json</code> holds a brief's full content, with benchmarks and every school.</li>
<li><b>CSV:</b> <a href='data/schools.csv'><code>schools.csv</code></a> and <a href='data/localities.csv'><code>localities.csv</code></a>, described in the <a href='data/DATA_DICTIONARY.md'>data dictionary</a>.</li>
<li>A static site: no server, no database, no accounts. It can be hosted anywhere, including GitHub Pages.</li></ul>

<h2>8. Known limits</h2>
<ul><li>Reading results are school year 2025-26; teachers and classrooms are 2023-24, the latest DepEd has published. Crowding is enrolment over classrooms across those years.</li>
<li>The public reading file covers Regions I, III, VIII, IX and CAR only.</li>
<li>SEF figures are FY2025 and preliminary. They are town-wide totals by office, not by school, and leave out the province's share of the fund. A locality that reported no spending may simply not have filed.</li>
<li>The National Tax Allotment is shown for scale only; it is not education money.</li>
<li>The groups describe where need shows up. They do not show that crowding causes low reading, or that spending will fix it.</li></ul>

<h2>9. Roadmap for the fellowship</h2>
<ul><li><b>SEF by school.</b> BLGF's figures stop at the town level. Local governments also file a quarterly Report of SEF Utilization under the Full Disclosure Policy. A parser for a pilot locality's report shows which schools the fund reached, beside the groups of schools.</li>
<li><b>COMPASS API.</b> PSGC codes replace name matching; DepEd regional appropriations, allotments and disbursements add the national side of the money.</li>
<li><b>Decision records.</b> A small record per meeting: group, amount set aside, status. The next brief reports whether it was spent, so a board's commitment can be followed.</li>
<li><b>Coverage.</b> New regions and grade levels as DepEd publishes them, by rerunning the pipeline. Briefs in Filipino.</li></ul>

<h2>10. Rules it follows</h2>
<ul><li>Schools are never ranked, and test results are not compared across school years, as DepEd's terms of use require.</li>
<li>Derived data is shared under the same terms as DepEd's files, with credit to DepEd. No DepEd, DBM or BLGF logo, no implied endorsement.</li>
<li>BLGF figures appear inside each brief and its JSON with credit to BLGF. The full BLGF workbook is not republished; get it from <a href='https://blgf.gov.ph/lgu-fiscal-data/'>BLGF's LGU fiscal data page</a>.</li>
<li>No figure is estimated or invented. Planned parts of a brief stay empty and labelled until a real source is connected.</li>
<li>{ATTRIBUTION}</li></ul>
</main></div>"""
    return page(f"Technical write-up | {NAME}", body)

def quality_html(quality, manifest, briefs):
    checks = [
        ("Public elementary schools in the enrolment file", f"{quality['public_elementary_schools']:,}"),
        ("Schools in the reading file", f"{quality['reading_file_schools']:,}"),
        ("Reading-file schools joined by School ID", f"{quality['reading_schools_matched']:,} "
         f"({quality['reading_schools_matched'] / quality['reading_file_schools']:.1%})"),
        ("Reading-file schools not joined", f"{quality['reading_schools_unmatched']:,}"),
        ("Schools with personnel data", f"{quality['schools_with_personnel']:,}"),
        ("Schools with facilities data", f"{quality['schools_with_facilities']:,}"),
        ("Localities in the enrolment file", f"{quality['localities']:,}"),
        ("Localities matched by name to DBM COMPASS", f"{quality['localities_matched_to_compass']:,} "
         f"({quality['localities_matched_to_compass'] / quality['localities']:.1%})"),
        ("Localities matched by name to BLGF Special Education Fund data", f"{quality['localities_matched_to_sef']:,} "
         f"({quality['localities_matched_to_sef'] / quality['localities']:.1%})"),
        ("Localities that qualify for a brief", f"{len(briefs)}"),
        ("Briefs with SEF figures", f"{sum(1 for b in briefs if b['money']['special_education_fund'])}"),
        ("Briefs where the locality reported no SEF spending for FY2025",
         f"{sum(1 for b in briefs if b['money']['special_education_fund'] and not b['money']['special_education_fund']['spent'])}"),
        ("Qualifying localities not matched to COMPASS",
         "; ".join(f"{b['name']}, {b['province']}" for b in briefs if not b["compass_matched"]) or "none"),
    ]
    src = "".join(
        f"<tr><td>{e(m['title'])}<br><span style='color:var(--mut);font-size:13px'>{e(m['publisher'])}</span></td>"
        f"<td style='text-align:left'>{e(m['period'])}</td>"
        f"<td style='text-align:left;white-space:normal'>{'Connected' if m['status'] == 'connected' else 'Planned, needs ' + e(m.get('needs') or '')}</td>"
        f"<td>{e(m.get('retrieved') or '')}</td><td class='hide-s'>{e((m.get('sha256') or '')[:12])}</td></tr>" for m in manifest)
    body = f"""<div class='wrap'><main class='sheet'>
<h1>Data quality</h1><p class='deck'>How well the sources line up and where each one comes from. Written by the pipeline on every run</p>
<section class='sec' style='margin-top:40px;padding-top:32px'><h2>Join checks</h2><div class='tw'><table><tbody>
{''.join(f"<tr><td>{e(a)}</td><td style='white-space:normal'>{e(b)}</td></tr>" for a, b in checks)}</tbody></table></div></section>
<section class='sec' style='margin-top:40px;padding-top:32px'><h2>Sources</h2><div class='tw'><table><thead><tr><th>Source</th><th style='text-align:left'>Period</th><th style='text-align:left'>Status</th>
<th>Retrieved</th><th class='hide-s'>SHA-256</th></tr></thead><tbody>{src}</tbody></table></div></section>
<section class='sec' style='margin-top:40px;padding-top:32px'><h2>Known gaps</h2><ul class='fine' style='margin-top:12px'>
<li>Location codes (PSGC) are not in DepEd's files or the public COMPASS export. Localities are matched by province and name until a COMPASS API key is available.</li>
<li>{len(quality['localities_unmatched'])} localities nationwide are not matched by name, mostly renamed or newly created local governments and Metro Manila districts.</li>
<li>{ATTRIBUTION}</li></ul></section></main></div>"""
    return page(f"Data quality | {NAME}", body)
