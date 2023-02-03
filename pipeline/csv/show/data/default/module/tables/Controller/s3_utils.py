    

async def dump_S3ChunkToFile():
    print('dump_S3ChunkToFile')
    
    if 0:
        bucket_name= 'gh-package-pdf'
        bucket_name= 'k9-filestore'
        prefix='k9-feed-doc-lims/'
        #chunk = S3U.list_s3_files_gen_start_after(bucket_name, prefix, start_after='A010281301.FINAL_v1_report.pdf')
        chunk = S3U.list_s3_files_gen_v2(bucket_name, prefix, MaxKeys=CHUNK_SIZE, plimit= 1_000_000)
        from csv import writer
        
        from pathlib import Path
        import platform
        import tempfile
        from random import sample
        from string import digits, ascii_letters
        cid=0
        temp_dir = Path("/tmp" if platform.system() == "Darwin" else tempfile.gettempdir())
        ext_dir  = join(temp_dir, 's3_extract_%s' % ''.join(sample(ascii_letters + digits, 10)))
        if not isdir(ext_dir):
            os.makedirs(ext_dir)
        
        #Download from S3
        gid=0
        for cid, pd in enumerate(chunk):
            rows={}
            print('dump_S3ChunkToFile:', cid,len(pd))
            fname= join(ext_dir, f'{cid}.csv')
            with open(fname, 'a', newline='') as fh:
                writer_object = writer(fh)
                header = ['Id', 'Bucket','Key', 'Size']
                writer_object.writerow(header)
                
                for pid, ppl in enumerate(pd):
                    #pp(ppl)
                    #e()
                    #row = (gid, f'{bucket_name}/{prefix}',pd[ppl]['Key'].lstrip(prefix),pd[ppl]['Size'])
                    writer_object.writerow((cid, f'{bucket_name}/{prefix}',pd[ppl]['Key'].lstrip(prefix),pd[ppl]['Size']))
                    gid +=1
            print(f'Extracted to {fname}')
            yield header, fname
            cid +=1
            
def get_S3_File_List(bucket_name, prefix):
    #bucket_name= 'gh-package-pdf'
    #bucket_name= 'k9-filestore'
    #prefix='k9-feed-doc-lims/'
    chunk = S3U.list_s3_files_gen(bucket_name, prefix, 1000, 100)
    #header
    #print('source,pipeline_name')
    rows={}
    for cid, pd in enumerate(chunk):
        for pid, ppl in enumerate(pd):
            #pp(ppl)
            #e()
            rows[pid] =(pid, f'{bucket_name}/{prefix}',pd[ppl]['Key'].lstrip(prefix),pd[ppl]['Size'])
    header = ['Id', 'Bucket','Key', 'Size']
    print('Got ', len(rows))
    return header, rows

def get_S3_File_List_gen(bucket_name, prefix):
    #bucket_name= 'gh-package-pdf'
    #bucket_name= 'k9-filestore'
    #prefix='k9-feed-doc-lims/'
    #chunk = S3U.list_s3_files_gen_start_after(bucket_name, prefix, start_after='A010281301.FINAL_v1_report.pdf')
    chunk = S3U.list_s3_files_gen_v2(bucket_name, prefix, MaxKeys=CHUNK_SIZE, plimit= 1_000_000)
    
    #header
    #print('source,pipeline_name')
    header = ['Id', 'Bucket','Key', 'Size']
    gid=0
    for cid, pd in enumerate(chunk):
        rows={}
        print(cid,len(pd))
        for pid, ppl in enumerate(pd):
            #pp(ppl)
            #e()
            rows[gid] =(gid, f'{bucket_name}/{prefix}',pd[ppl]['Key'].lstrip(prefix),pd[ppl]['Size'])
            gid +=1
        #print('Got ', len(rows))
        yield header, rows

    return header, rows