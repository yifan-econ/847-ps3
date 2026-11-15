"""Run eight independent specifications, with two local estimation processes at most.
Ctrl-C terminates this runner's children and cancels queued specifications.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import subprocess,sys,itertools,json,os,threading
ROOT=Path(__file__).resolve().parents[1]
active={};lock=threading.Lock();stop=threading.Event()
def run(task):
 sample,demo,iv=task;label=f'{sample}__{demo}__{iv}'
 if stop.is_set():return dict(model=label,exit_code=-1,cancelled=True)
 if (ROOT/f'results/{label}/summary.json').exists() and (ROOT/f'results/{label}/pyblp_results.pkl.gz').exists():return dict(model=label,exit_code=0,cached=True)
 print('START',label,flush=True)
 with open(ROOT/f'results/{label}.log','w') as log:
  with lock:
   if stop.is_set():return dict(model=label,exit_code=-1,cancelled=True)
   p=subprocess.Popen([sys.executable,'-u',str(ROOT/'src/run_mixed.py'),'--sample',sample,'--demographic',demo,'--iv',iv,'--income-order','15'],stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'})
   active[label]=p
  code=p.wait()
  with lock:active.pop(label,None)
 print('END',label,code,flush=True)
 return dict(model=label,exit_code=code,cached=False)
status=[];pool=ThreadPoolExecutor(max_workers=2)
futures=[pool.submit(run,t) for t in itertools.product(['all_packs','multi_packs'],['household','income'],['aac','other_zone'])]
try:
 for f in as_completed(futures):
  status.append(f.result());(ROOT/'results/batch_status.json').write_text(json.dumps(status,indent=2))
except KeyboardInterrupt:
 stop.set()
 with lock:
  for p in active.values():p.terminate()
 for f in futures:f.cancel()
 raise
finally:pool.shutdown(wait=True,cancel_futures=True)
