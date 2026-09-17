import json, os
from pathlib import Path

role=os.environ['ROLE']
model=os.environ['MODEL']
focus=os.environ['FOCUS']
out=Path('results'); out.mkdir(exist_ok=True)
record={'role':role,'model':model,'focus':focus,'status':'UNREVIEWED_EXTERNAL_AGENT_OUTPUT','inference_success':False}
try:
    from hf_gradio import GradioClient
    c=GradioClient(model)
    prompt=f'''You are {role} in CEREBRON Ω Farm 27 Agriculture Food. Focus: {focus}.
Rules: REALITY>COHERENCE; CLAIM<=EVIDENCE; distinguish established/supported/plausible/speculative/conflicted/unknown; state assumptions, region, season, crop/species, data limits, uncertainty, transfer limits, safety and falsification criteria. Do not treat model output as field evidence. Produce concise structured analysis with claims, evidence needed, risks, unknowns and tests.'''
    ans=c.predict(message=prompt,api_name='/chat')
    record['inference_success']=True
    record['response']=ans
except Exception as e:
    record['error']=repr(e)
(out/f'{role}.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
