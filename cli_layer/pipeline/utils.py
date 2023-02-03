import os
from os.path import split, join, isdir, basename, isfile, dirname
from cli_layer.fmt import  pfmt, pfmtv, pfmtd, psql

def save_file(fn, data):

    dn= dirname(fn)
    if not isdir(dn):
        os.makedirs(dn,exist_ok=True)
    with open(fn, 'w') as fh:
        fh.write(data)
        pfmt([[f'Saved to: {fn}']],['File saved'])

def check_pcount(params,pcount):
    
    if pcount == 1:
        assert params, 'Empty params.'
        assert type(params) in [str], params
        return
    
    assert len(params)==pcount, '%d - wrong parameter count (expecting %d)' % (len(params),pcount)

def get_params(**kwargs):
    params = kwargs['params']
    assert params, params
    cp=dict()
    if type(params) in [tuple]:
    
        cp = {pid:p for pid,p in enumerate(params)}
    else:
        assert type(params) in [str]
        cp[0]=params

    return cp, params