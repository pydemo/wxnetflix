import os
import glob
from os.path import join, basename
from pprint import pprint as pp
git_home = os.sep.join(['..', '..','data-pipelines'])
ppl_dir= os.sep.join(['_deploy','config','v2'])

daily='daily'
hourly='hourly'
monthly='monthly'
def get_pipeline_filenames():
    path =  os.sep.join([git_home, ppl_dir,'**', '*.json'])
    files = glob.glob(path, recursive=True)
    return files


def get_ppl_type(pn):
    if daily.lower() in pn.lower():
        ppl_ptype=daily
    elif hourly.lower() in pn.lower():
        ppl_ptype=hourly
    elif monthly.lower() in pn.lower():
        ppl_ptype=monthly
    else:
        ppl_ptype=''
    return ppl_ptype