import sys, time
import boto3, botocore

from pprint import pprint as pp
e=sys.exit

def list_pipelines():
    out={}
    dppl = boto3.client('datapipeline')

    
    marker = None
    while True:
        paginator = dppl.get_paginator('list_pipelines')
        response_iterator = paginator.paginate( 
            PaginationConfig={
                #'PageSize': 10,
                'StartingToken': marker})
        for page in response_iterator:
            plist = page['pipelineIdList']
            for ppl in plist:
                
                out[ppl['name']]=ppl
    
        try:
            if page['hasMoreResults']:
                marker = response_iterator
            
            else:
                break
        except:
            raise
    
    return out
    
def get_pipeline_definition(ppld, client):
    id, name = ppld['id'], ppld['name']
    try:
        rs= client.get_pipeline_definition(
            pipelineId=id
        
        )
    except botocore.exceptions.ClientError as ex:
        #retry again
        rs= client.get_pipeline_definition(
            pipelineId=id
        
        )
    return rs


    