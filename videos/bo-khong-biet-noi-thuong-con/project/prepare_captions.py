from pathlib import Path
import json,re,unicodedata,difflib,textwrap
root=Path(__file__).resolve().parent.parent
raw=json.loads((root/'project/transcript-asr.json').read_text())
a=[w for seg in raw for w in seg['words']]
src=(root/'loi-thoai.txt').read_text().split()+['Bố','ra','đón.']
def norm(s):
 s=unicodedata.normalize('NFD',s.lower().replace('đ','d'))
 return re.sub('[^a-z0-9]','', ''.join(c for c in s if not unicodedata.combining(c)))
x=[norm(w) for w in src];y=[norm(w['word']) for w in a]
matcher=difflib.SequenceMatcher(None,x,y,autojunk=False)
times=[None]*len(src);review=[]
for tag,i,j,k,l in matcher.get_opcodes():
 if tag=='equal' or (tag=='replace' and j-i==l-k):
  for si,ai in zip(range(i,j),range(k,l)):times[si]=(a[ai]['start'],a[ai]['end'])
 elif i<j:
  start=a[k]['start'] if k<len(a) else a[-1]['end']
  end=a[l-1]['end'] if l>k else start
  if end<=start:
   end=a[k]['start'] if k<len(a) else start+.1
   start=a[k-1]['end'] if k>0 else 0
  end=max(end,start+.06*(j-i))
  for si in range(i,j):times[si]=(start+(end-start)*(si-i)/(j-i),start+(end-start)*(si-i+1)/(j-i))
 if tag!='equal':review.append({'kind':tag,'script':' '.join(src[i:j]),'asr':' '.join(w['word'].strip() for w in a[k:l]),'start':a[min(k,len(a)-1)]['start']})
words=[{'word':s,'start':round(t[0],3),'end':round(t[1],3)} for s,t in zip(src,times)]
(root/'project/aligned-words.json').write_text(json.dumps(words,ensure_ascii=False,indent=2))
(root/'project/alignment-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2))
# Use local recognized word timings; original script corrects ASR spelling.
cues=[];cur=[]
for w in words:
 if cur and (len(' '.join(t['word'] for t in cur+[w]))>72 or w['end']-cur[0]['start']>4.6 or w['start']-cur[-1]['end']>.65):
  cues.append(cur);cur=[]
 cur.append(w)
 if re.search('[.!?…][”\"]?$',w['word']) and (len(cur)>=4 or w['end']-cur[0]['start']>.7):cues.append(cur);cur=[]
if cur:cues.append(cur)
def stamp(t):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
 return f'{h:02}:{m:02}:{s:02},{ms:03}'
rows=[]
for i,c in enumerate(cues):
 start=c[0]['start'];end=max(c[-1]['end']+.08,start+.55)
 if i+1<len(cues):end=min(end,cues[i+1][0]['start']-.02)
 end=max(end,start+.1)
 txt=' '.join(w['word'] for w in c)
 lines=textwrap.wrap(txt,width=38,break_long_words=False,break_on_hyphens=False)
 if len(lines)>2:
  toks=txt.split();best=min(range(1,len(toks)),key=lambda n:abs(len(' '.join(toks[:n]))-len(' '.join(toks[n:]))));lines=[' '.join(toks[:best]),' '.join(toks[best:])]
 rows.append({'start':start,'end':end,'text':'\n'.join(lines)})
# Merge very short trailing fragments when two readable lines still fit.
for i in range(len(rows)-1,0,-1):
 if rows[i]['end']-rows[i]['start']<.7 and len(rows[i]['text'].split())<=1:
  joined=(rows[i-1]['text']+' '+rows[i]['text']).replace('\n',' ')
  if len(joined)<=78:
   rows[i-1]['end']=rows[i]['end'];rows[i-1]['text']='\n'.join(textwrap.wrap(joined,width=40,break_long_words=False));rows.pop(i)
(root/'subtitles.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(rows))+'\n')
(root/'project/captions.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print('Words:',len(words),'Cues:',len(rows),'Corrections:',len(review))
for r in review:
 if r['kind'] in ['delete','insert'] or len(r['script'].split())>4:print(r)
