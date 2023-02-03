import sys, time
import boto3, botocore

from pprint import pprint as pp
e=sys.exit



    
    
def list_s3_files(bucket_name, prefix, MaxItems=100, PageSize=100):
    out={}
    dppl = boto3.client('s3')

    
    marker = None
    pid=0
    while True:
        paginator = dppl.get_paginator('list_objects')
        response_iterator = paginator.paginate( Bucket=bucket_name, Prefix= prefix,
            PaginationConfig={
                'MaxItems':MaxItems,
                'PageSize':PageSize,
                'StartingToken': marker})
        for page in response_iterator:
            #pp(page)
            #e()
            print(pid, len(out))
            plist = page['Contents']
            for ppl in plist:
                out[ppl['Key']]=ppl
            pid +=1
        try:

            if 'hasMoreResults' in page and page['hasMoreResults']:
                print('more...')
                marker = response_iterator
            
            else:
                print('breaking')
                break
        except:
            raise
    
    return out
    

def list_s3_files_gen(bucket_name, prefix, MaxItems=1000, PageSize=1000):
    
    dppl = boto3.client('s3')

    
    marker = None
    pid=0
    while True:
        paginator = dppl.get_paginator('list_objects')
        response_iterator = paginator.paginate( Bucket=bucket_name, Prefix= prefix,
            PaginationConfig={
                'MaxItems':MaxItems,
                'PageSize':PageSize,
                
                'StartingToken': marker})
        for page in response_iterator:
            out={}

            plist = page['Contents']
     
            for ppl in plist:
                out[ppl['Key']]=ppl
            pid +=1
            yield out
        try:

            if 'hasMoreResults' in page and page['hasMoreResults']:
                print('more...')
                marker = response_iterator
            
            else:
                print('breaking')
                break
        except:
            raise
    
    return out
def list_s3_files_gen_v2(bucket_name, prefix,   MaxKeys=1000, plimit=1):
    
    dppl = boto3.client('s3')

    
    marker = None
    pid=0
    while True:
        paginator = dppl.get_paginator('list_objects_v2')
        response_iterator = paginator.paginate( Bucket=bucket_name, Prefix= prefix, MaxKeys=MaxKeys,
            PaginationConfig={
                #'MaxItems':MaxItems,
                #'PageSize':PageSize,
                #'StartAfter':start_after,
                'ContinuationToken': marker})
        for page in response_iterator:
            out={}
            if pid>=plimit: break
            #print(pid, len(out))
            plist = page['Contents']
            #print(333333333,len(plist))
            for ppl in plist:
                out[ppl['Key']]=ppl
            pid +=1
            yield out
            
            
        try:

            if 'NextContinuationToken' in page and page['NextContinuationToken']:
                print('more...')
                marker = page['NextContinuationToken']
            
            else:
                print('breaking')
                break
        except:
            raise
        if pid>=plimit: break
    return out
    
def list_s3_files_gen_start_after(bucket_name, prefix,  start_after, MaxItems=1000, PageSize=1000):
    
    dppl = boto3.client('s3')

    
    marker = None
    pid=0
    while True:
        paginator = dppl.get_paginator('list_objects_v2')
        response_iterator = paginator.paginate( Bucket=bucket_name, Prefix= prefix, StartAfter = 'k9-feed-doc-lims/rqid_A*',MaxKeys=10000,
            PaginationConfig={
                #'MaxItems':MaxItems,
                #'PageSize':PageSize,
                #'StartAfter':start_after,
                'ContinuationToken': marker})
        for page in response_iterator:
            out={}

            #print(pid, len(out))
            plist = page['Contents']
            #print(333333333,len(plist))
            for ppl in plist:
                out[ppl['Key']]=ppl
            pid +=1
            yield out
            
        try:

            if 'NextContinuationToken' in page and page['NextContinuationToken']:
                print('more...')
                marker = page['NextContinuationToken']
            
            else:
                print('breaking')
                pp(out)
                break
        except:
            raise
    
    return out
    