import json,time,os
from faster_whisper import WhisperModel
from pathlib import Path
out=Path(__file__).resolve().parent
out.mkdir(exist_ok=True)
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,download_root=os.environ.get('WHISPER_CACHE_DIR', '/tmp/faster-whisper-cache'))
segments,info=model.transcribe(str(out.parent / 'audio-goc.mp3'),language='vi',word_timestamps=True,beam_size=5,vad_filter=True,initial_prompt='Bố không biết nói thương con. Lời kể của người con về bố, mẹ, đi học, sửa xe máy, mất việc, tiền phòng, về nhà và đưa bố đi khám.')
rows=[]
for s in segments:
 rows.append({'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'word':w.word,'probability':w.probability} for w in s.words]})
 print(f'{s.start:.1f}-{s.end:.1f}: {s.text}',flush=True)
 (out/'transcript-asr.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print('DONE',len(rows),info.duration,flush=True)
