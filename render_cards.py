import os,json,html,base64,subprocess,tempfile
from pathlib import Path
from datetime import date,timedelta
from collections import defaultdict,Counter
R=Path(__file__).resolve().parent; O=R/'cards'; STATIC=os.getenv('STATIC')=='1'
D={'name':'Devi Prasad Sundaray','tagline':'I make designs people remember — and build the systems behind them.','brand':{'bg':'#101010','panel':'#181818','text':'#F5F2EA','muted':'#A5A29B','accent':'#D8FF3E','line':'#343434','heat':['#202020','#42501F','#718B2B','#A9D936','#D8FF3E']},'fonts':{'display':'Arial','body':'Arial','mono':'Courier New','files':[]},'portrait':'','tiles':[{'title':'DEVELOPMENT','subtitle':'Systems & software','symbol':'{ }','href':'https://github.com/D3vi7x7'},{'title':'DESIGN','subtitle':'Visuals & experiences','symbol':'✳','href':'https://devi-portfolio-rho.vercel.app/'},{'title':'3D & REALTIME','subtitle':'Unreal · Blender · GPU','symbol':'◈','href':'https://github.com/D3vi7x7'}],'featured_repos':[{'name':'MultiplayerSessions Plugin','description':'A delegate-driven Unreal Engine session system for creating, finding and joining multiplayer sessions.','language':'C++','url':'https://github.com/D3vi7x7/MultiplayerPlugin'},{'name':'More projects','description':'Explore my software, graphics and creative technology experiments.','language':'OPEN SOURCE','url':'https://github.com/D3vi7x7'}]}
def esc(x): return html.escape(str(x if x is not None else ''),quote=True)
def merge(a,b):
 for k,v in b.items():
  if isinstance(v,dict) and isinstance(a.get(k),dict): merge(a[k],v)
  else:a[k]=v
 return a
def read(p,d):return json.loads(p.read_text()) if p.exists() else d
def fontcss(c):
 out=[]
 for f in c['fonts'].get('files',[]):
  p=R/f['path']
  if not p.exists():continue
  try:
   with tempfile.TemporaryDirectory() as td:
    q=Path(td)/'f.woff'
    subprocess.run(['pyftsubset',str(p),f'--output-file={q}','--flavor=woff',"--text=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,:;!?@#%&()[]+-_/—’'→←↑↓"],check=True,capture_output=True)
    out.append("@font-face{font-family:'%s';font-weight:%s;src:url(data:font/woff;base64,%s) format('woff')}"%(esc(f['family']),f.get('weight',400),base64.b64encode(q.read_bytes()).decode()))
  except Exception as ex:print('font subset skipped',ex)
 return ''.join(out)
def css(c,delay):
 b=c['brand'];f=c['fonts']
 motion='' if STATIC else ('.in{animation:rise .8s ease %.2fs both}.fade{animation:fade .9s ease %.2fs both}.bar{transform-box:fill-box;transform-origin:bottom;animation:grow .9s ease %.2fs both}'%(delay,delay+.15,delay+.2)+ '@keyframes rise{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}@keyframes fade{from{opacity:0}to{opacity:1}}@keyframes grow{from{transform:scaleY(.03)}to{transform:scaleY(1)}}')
 static='.in,.fade,.bar{animation:none!important;opacity:1!important;transform:none!important}' if STATIC else ''
 return '<style>'+fontcss(c)+f"text{{font-family:'{esc(f['body'])}',Arial,sans-serif}}.display{{font-family:'{esc(f['display'])}',Arial,sans-serif}}.mono{{font-family:'{esc(f['mono'])}',monospace}}.txt{{fill:{b['text']}}}.muted{{fill:{b['muted']}}}.accent{{fill:{b['accent']}}}.panel{{fill:{b['panel']};stroke:{b['line']};stroke-width:1}}"+motion+static+'@media(prefers-reduced-motion:reduce){.in,.fade,.bar{animation:none!important;opacity:1!important;transform:none!important}.moving{display:none!important}}</style>'
def start(w,h,c,d=0):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'+css(c,d)+f'<rect width="100%" height="100%" rx="22" fill="{c["brand"]["bg"]}"/>'
def save(n,s):(O/n).write_text(s+'</svg>',encoding='utf8')
def render(c,days):
 b=c['brand'];O.mkdir(exist_ok=True)
 # Hero
 p=''
 if c.get('portrait'):
  q=R/c['portrait']
  if q.exists():
   mime='image/png' if q.suffix.lower()=='.png' else 'image/jpeg'
   p=f'<image href="data:{mime};base64,{base64.b64encode(q.read_bytes()).decode()}" x="765" y="50" width="130" height="130" preserveAspectRatio="xMidYMid slice"/>'
 s=start(960,230,c,0)+f'<rect x="1" y="1" width="958" height="228" rx="22" class="panel"/><circle cx="910" cy="0" r="170" fill="{b["accent"]}" opacity=".05"/><g class="in"><text x="42" y="48" class="mono muted" font-size="12" letter-spacing="3">D3VI® / DEVELOPER & CREATIVE TECHNOLOGIST</text><text x="40" y="119" class="display txt" font-size="52" font-weight="800">{esc(c["name"])}</text><text x="43" y="160" class="txt" font-size="17">{esc(c["tagline"])}</text><text x="43" y="198" class="mono accent" font-size="12">SOFTWARE · DESIGN · 3D · REALTIME</text></g>{p}<g class="moving"><circle cx="830" cy="115" r="79" fill="none" stroke="{b["accent"]}" stroke-dasharray="4 8"><animateTransform attributeName="transform" type="rotate" from="0 830 115" to="360 830 115" dur="24s" repeatCount="indefinite"/></circle></g>'
 save('hero.svg',s)
 # Three linked tiles
 for i,t in enumerate(c['tiles'][:3]):
  s=start(310,148,c,.7+i*.2)+f'<rect x="1" y="1" width="308" height="146" rx="18" class="panel"/><g class="in"><text x="22" y="34" class="mono muted" font-size="10">0{i+1} / WHAT I DO</text><text x="22" y="87" class="display accent" font-size="35">{esc(t.get("symbol","↗"))}</text><text x="86" y="76" class="display txt" font-size="17" font-weight="700">{esc(t["title"])}</text><text x="86" y="100" class="muted" font-size="12">{esc(t["subtitle"])}</text><path d="M260 118h22m-8 -8 8 8 -8 8" stroke="{b["accent"]}" fill="none"/></g>'
  save(f'tile-{i+1}.svg',s)
 # Stats/monthly data
 bym=defaultdict(int); wd=Counter(); lookup={}
 for x in days:
  d=date.fromisoformat(x['date']);n=x['count'];lookup[x['date']]=n;bym[d.strftime('%Y-%m')]+=n
  if n:wd[d.strftime('%A')]+=n
 now=date.today();first=(now.replace(day=1)-timedelta(days=365)).replace(day=1); months=[]
 for i in range(12):
  y=first.year+(first.month-1+i)//12;m=(first.month-1+i)%12+1;d=date(y,m,1);months.append((d.strftime('%b'),bym[d.strftime('%Y-%m')]))
 mx=max([v for _,v in months]+[1]);bars=''
 for i,(lab,v) in enumerate(months):
  x=48+i*66;h=max(4,75*v/mx);bars+=f'<rect class="bar" x="{x}" y="{138-h:.1f}" width="34" height="{h:.1f}" rx="5" fill="{b["accent"]}"/><text x="{x+17}" y="157" text-anchor="middle" class="mono muted" font-size="9">{lab}</text>'
 cur=now if lookup.get(now.isoformat(),0) else now-timedelta(days=1);streak=0
 while lookup.get(cur.isoformat(),0):streak+=1;cur-=timedelta(days=1)
 active=sum(v>0 for v in lookup.values());busy=wd.most_common(1)[0][0] if wd else '—'
 s=start(960,220,c,1.5)+f'<rect x="1" y="1" width="958" height="218" rx="22" class="panel"/><g class="in"><text x="30" y="34" class="mono muted" font-size="11">CONTRIBUTION PULSE / MONTHLY</text><text x="30" y="83" class="display txt" font-size="34">{sum(lookup.values()):,}</text><text x="32" y="103" class="muted" font-size="11">total contributions in available data</text>{bars}<text x="900" y="76" text-anchor="end" class="display accent" font-size="30">{streak}</text><text x="900" y="93" text-anchor="end" class="mono muted" font-size="9">DAY STREAK</text><text x="900" y="123" text-anchor="end" class="display txt" font-size="21">{active}</text><text x="900" y="139" text-anchor="end" class="mono muted" font-size="9">ACTIVE DAYS</text><text x="900" y="187" text-anchor="end" class="mono accent" font-size="11">BUSIEST: {esc(busy.upper())}</text></g>'
 save('activity.svg',s)
 # Featured repo cards
 for i,r in enumerate(c['featured_repos']):
  s=start(960,132,c,2+i*.2)+f'<rect x="1" y="1" width="958" height="130" rx="19" class="panel"/><g class="in"><text x="28" y="30" class="mono accent" font-size="10">SELECTED WORK / 0{i+1}</text><text x="28" y="68" class="display txt" font-size="24" font-weight="700">{esc(r["name"])}</text><text x="28" y="96" class="muted" font-size="13">{esc(r["description"])}</text><text x="28" y="117" class="mono muted" font-size="10">{esc(r.get("language","PROJECT"))}</text><path d="M900 65h22m-8 -8 8 8 -8 8" stroke="{b["accent"]}" fill="none" stroke-width="2"/></g>'
  save(f'repo-{i+1}.svg',s)
 # 52-week contribution heatmap
 end=now;begin_date=end-timedelta(days=363);begin_date-=timedelta(days=(begin_date.weekday()+1)%7);cells=''
 for i in range(364):
  d=begin_date+timedelta(days=i)
  if d>end:break
  n=lookup.get(d.isoformat(),0);lv=0 if n==0 else 1 if n<=2 else 2 if n<=5 else 3 if n<=9 else 4
  cells+=f'<rect x="{38+(i//7)*16}" y="{49+(i%7)*16}" width="11" height="11" rx="3" fill="{b["heat"][lv]}"><title>{d.isoformat()}: {n}</title></rect>'
 legend=''.join(f'<rect x="{78+j*17}" y="160" width="11" height="11" rx="3" fill="{b["heat"][j]}"/>' for j in range(5))
 s=start(960,184,c,2.7)+f'<rect x="1" y="1" width="958" height="182" rx="22" class="panel"/><g class="in"><text x="30" y="29" class="mono muted" font-size="11">THE LONG GAME / CONTRIBUTION GRAPH</text>{cells}<text x="42" y="169" class="mono muted" font-size="9">LESS</text>{legend}<text x="168" y="169" class="mono muted" font-size="9">MORE</text><text x="920" y="169" text-anchor="end" class="mono accent" font-size="10">{sum(lookup.values()):,} CONTRIBUTIONS</text></g>'
 save('contributions.svg',s)
def main():
 c=merge(json.loads(json.dumps(D)),read(R/'profile.json',{}));raw=read(R/'data/contributions.json',{'days':[]})
 if 'days' in raw:src=raw['days']
 else:
  try:src=[d for w in raw['data']['user']['contributionsCollection']['contributionCalendar']['weeks'] for d in w['contributionDays']]
  except (KeyError,TypeError):src=[]
 days=[{'date':x['date'],'count':int(x.get('count',x.get('contributionCount',0)) or 0)} for x in src if x.get('date')]
 render(c,days);print('Generated SVG cards; STATIC='+str(int(STATIC)))
if __name__=='__main__':main()
