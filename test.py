
import requests
import time
import warnings
clus = 'xir-dcstdot'
svm = 'xir-tvst2ns01'
vol = 'test_oct_srini7'
aggr = 'N01_T3_DSAT01'
policy = 'rw_all'
size = 10737418240
snappolicy = 'Tier2-1'

comment = 'BKP:None,OWNER:marisri,MGR:jjadhav,DEPT:1204,TYPE:Test_APP,APP:TestApp,APPGRP:bssa_storage'
type = 'rw'
tieringpolicy = 'none'
encryption = 'False'
is_clone = 'False'
dedupe = 'none'
#change in prod to inline
cs_dedupe = 'none'
compaction = 'none'
style = 'unix'
space_guarantee ='none'

data = {'svm.name': svm, 'name': vol, 'aggregates.name': [aggr], 'comment': comment, 'tiering.policy': tieringpolicy, 'type': type, 'encryption.enabled': encryption, 'clone.is_flexclone': is_clone, 'efficiency.dedupe': dedupe, 'efficiency.cross_volume_dedupe': cs_dedupe, 'efficiency.compaction': compaction, 'nas.security_style': style, 'nas.export_policy.name': policy, 'space.size': size, 'guarantee.type': space_guarantee, 'snapshot_policy.name': snappolicy }

response3 = requests.post(f"https://{clus}/api/storage/volumes", auth=('apiadminn', 'netapp123'), json=data, verify=False)
#print(response3.text)
print(response3.status_code)
#print(response3.headers.items())
#print(response3.links)
print(response3.reason)
#print(response3.content)
print(response3.url)
print(response3.json())
r = response3.json() 
if response3.status_code < 200 or response3.status_code > 202:
   print(r['error']['message'])
else:
   uuid = r['job']['uuid']
   print(uuid)
   response4 = requests.get(f"https://{clus}/api/cluster/jobs/{uuid}", auth=('apiadminn', 'netapp123'), verify=False)
   r = response4.json()
   print(r['state'])
   time.sleep(1)
   response5 = requests.get(f"https://{clus}/api/cluster/jobs/{uuid}", auth=('apiadminn', 'netapp123'), verify=False)
   r = response5.json()
   print(r['state'])
   if r['state'] == 'success':
      print("volume created")
   elif r['state'] == 'failure':
      print(r['message'])
   elif r['state'] == 'running':
      print("Operation is still running, run below command to know status with uuid as "+ uuid)
      print("curl -ik --cert cert_user.crt --key cert_user.key https://xir-dcstdot/api/cluster/jobs/<uuid>")
