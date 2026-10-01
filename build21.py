import re,json,base64,io
from PIL import Image
s=open('shada-v21-template.html',encoding='utf-8').read()
uris=json.load(open('shada-assets/uris.json')); small=json.load(open('shada-assets/small.json'))
m={'nutricare':'Shada Nutricare Hand Feeding','eggfood':'Shada Avian Eggfood','herbs':'Shada Avian Herbs','spirulina':'Shada Avian Spirulina','moringa':'Shada Moringa Leaf Powder','beetroot':'Shada Beetroot Powder'}
t=s
for k,alt in m.items(): t=t.replace('@JL_%s@'%k,uris[alt]).replace('@JS_%s@'%k,small[k])
for n in ['lovebird','budgerigar','cockatiel','conure','ringneck','rosella']:
    im=Image.open(f'birds/{n}.png').convert('RGBA'); im.thumbnail((360,360)); o=io.BytesIO(); im.save(o,'WEBP',quality=82,method=6)
    t=t.replace('@B_%s@'%n,'data:image/webp;base64,'+base64.b64encode(o.getvalue()).decode())
ph=Image.open('ref/breeder.png').convert('RGB'); ph=ph.resize((1200,900)); o=io.BytesIO(); ph.save(o,'WEBP',quality=80,method=6)
t=t.replace('@PHOTO_breeder@','data:image/webp;base64,'+base64.b64encode(o.getvalue()).decode())
white=open('shada-assets/logo-white.svg',encoding='utf-8').read(); white=re.sub(r'<\?xml[^>]*\?>','',white).strip(); white=re.sub(r'\s(width|height)="[^"]*"','',white,count=2)
t=t.replace('@LOGO_DARK@',white.replace('rgb(100%, 100%, 100%)','#1D1D1F'))
t=t.replace('@BDMAP@',open('/tmp/bdmap.svg',encoding='utf-8').read())
assert not re.findall(r'@[A-Z_a-z]+@',t), re.findall(r'@[A-Z_a-z]+@',t)
open('shada-home-v21-preview.html','w',encoding='utf-8').write(t)
fonts=open('/tmp/wf/fonts-inline.css').read()
keep=[b for b in fonts.split('\n') if "'Plus Jakarta Sans'" in b or "'Hind Siliguri'" in b]
a=t.replace('<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Hind+Siliguri:wght@400;500;600;700&display=swap" rel="stylesheet">','<style>:root{color-scheme:light}\n'+"\n".join(keep)+'</style>')
a=a.replace('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>','')
open('shada-v21-artifact.html','w',encoding='utf-8').write(a)
print("preview",round(len(t)/1024),"KB | artifact",round(len(a)/1024),"KB")
