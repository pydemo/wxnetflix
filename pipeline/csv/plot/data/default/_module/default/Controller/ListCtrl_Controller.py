import wx
import sys, time, boto3
from pprint import pprint as pp
from ui_layer.Base import Base, reciever

import ui_layer.config.ui_config as ui_config
uic = ui_config.uic
from cli_layer.utils import  cli_exception
import cli_layer.s3_utils  as S3U

MAXINT = 99999999
CHUNK_SIZE = 30 

import traceback
def format_stacktrace():
    parts = ["Traceback (most recent call last):\n"]
    parts.extend(traceback.format_stack(limit=50)[:-2])
    parts.extend(traceback.format_exception(*sys.exc_info())[1:])
    return "".join(parts)

#----------------------------------------------------------------------
class ListCtrl_Controller(Base):
    def __init__(self):
        self.pid=0 
        #self.slog('Start')
        self.sub('scanS3')
        self.header = ['Id', 'Date','Key', 'Size']
    def setPage(self):
        eid = CHUNK_SIZE*(self.pid+1)
        if len(self.data) < eid:
            eid = len(self.data)
        self.itemDataMap = {x:self.data[x] for x in range(CHUNK_SIZE*self.pid, eid)}
    @reciever
    def firstPage(self, message, arg2=None, **kwargs):
        self.slog('firstPage')
        try:
            with wx.WindowDisabler():
                uic.info = wx.BusyInfo(
                     wx.BusyInfoFlags()
                         .Parent(self)
                         .Icon(wx.ArtProvider.GetIcon(wx.ART_FIND,
                                                      wx.ART_OTHER, wx.Size(128, 128)))
                         .Title("<b>First</b>")
                         .Text("Please wait...")
                         .Foreground(wx.WHITE)
                         .Background(wx.BLACK)
                         .Transparency( wx.ALPHA_OPAQUE/2)
                 )

                wx.GetApp().Yield()  
                self.pid =0
                
                self.slog('ListCtrl_Controller: firstPage: %s ' %  self.pid)
                self.setPage()
                self.Refresh()
            self.del_busy()
        except:
            self.del_busy()
            raise
    @reciever
    def prevPage(self, message, arg2=None, **kwargs):
        if self.pid:
            try:
                with wx.WindowDisabler():
                    uic.info = wx.BusyInfo(
                         wx.BusyInfoFlags()
                             .Parent(self)
                             .Icon(wx.ArtProvider.GetIcon(wx.ART_FIND,
                                                          wx.ART_OTHER, wx.Size(128, 128)))
                             .Title("<b>Previous</b>")
                             .Text("Please wait...")
                             .Foreground(wx.WHITE)
                             .Background(wx.BLACK)
                             .Transparency( wx.ALPHA_OPAQUE/2)
                     )

                    wx.GetApp().Yield()  
                    self.pid -=1
                    
                    self.slog('ListCtrl_Controller: prevPage: %s ' %  self.pid)
                    self.setPage()
                    self.Refresh()
                self.del_busy()
            except:
                self.del_busy()
                raise
        else:
            self.slog('ListCtrl_Controller: prevPage: PASS ')
    @reciever
    def nextPage(self, message, arg2=None, **kwargs):
    
        try:
            with wx.WindowDisabler():
                uic.info = wx.BusyInfo(
                     wx.BusyInfoFlags()
                         .Parent(self)
                         .Icon(wx.ArtProvider.GetIcon(wx.ART_FIND,
                                                      wx.ART_OTHER, wx.Size(128, 128)))
                         .Title("<b>Next</b>")
                         .Text("Please wait...")
                         .Foreground(wx.WHITE)
                         .Background(wx.BLACK)
                         .Transparency( wx.ALPHA_OPAQUE/2)
                 )

                wx.GetApp().Yield()  
                self.pid +=1
                self.slog('ListCtrl_Controller: nextPage: %s , count: %s' %  (self.pid, len(self.data)))
                self.setData()
                self.Refresh()
            self.del_busy()
        except:
            self.del_busy()
            raise
    @reciever
    def lastPage(self, message, arg2=None, **kwargs):
        
        try:
            with wx.WindowDisabler():
                uic.info = wx.BusyInfo(
                     wx.BusyInfoFlags()
                         .Parent(self)
                         .Icon(wx.ArtProvider.GetIcon(wx.ART_FIND,
                                                      wx.ART_OTHER, wx.Size(128, 128)))
                         .Title("<b>Last</b>")
                         .Text("Please wait...")
                         .Foreground(wx.WHITE)
                         .Background(wx.BLACK)
                         .Transparency( wx.ALPHA_OPAQUE/2)
                 )

                wx.GetApp().Yield()  
                
                self.slog('ListCtrl_Controller: lastPage: %s ' %  self.pid)
                if not self.is_full:
                    
                    self.getAllData()
                    self.itemDataMap = {x:self.data[x] for x in range(CHUNK_SIZE*(self.pid), len(self.data))}
                    self.Refresh()
                    self.is_full=True
                    self.last_pid=self.pid
                else:
                    self.pid = self.last_pid
                    self.Refresh()
            self.del_busy()
        except:
            self.del_busy()
            raise
    def del_busy(self):
        if hasattr(uic, 'info'):
            del uic.info
    @reciever
    def scanS3(self,message, arg2=None, **kwargs):
        obj, changed = message
        
        text = f"""--------------------
        scanS3 (changed: {changed}):
        {obj.id}, {obj.bucket_name}, {obj.prefix}, {obj.profile}

        --------------------------"""
                
        print(text)
        self.bucket_name = obj.bucket_name
        self.prefix = obj.prefix
        self.file_prefix = self.getFilePrefix(self.prefix)

        
        with wx.WindowDisabler():
            uic.info = wx.BusyInfo(
                 wx.BusyInfoFlags()
                     .Parent(self)
                     .Icon(wx.ArtProvider.GetIcon(wx.ART_FIND,
                                                  wx.ART_OTHER, wx.Size(128, 128)))
                     .Title("<b>Scanning</b>")
                     .Text("Please wait...")
                     .Foreground(wx.WHITE)
                     .Background(wx.BLACK)
                     .Transparency( wx.ALPHA_OPAQUE/2)
             )

            wx.GetApp().Yield()  
            try:
                
                self.initList()
            except:
                self.del_busy()
                raise
        self.del_busy()
        if 1:
            self.send('scanS3_done', message)
            self.slog('send->scanS3_done' )
        #self.scanS3_done(message)
        #if changed:
        #    self.saveScanStr(obj)
    def scanS3_done(self, message):
        self.send('scanS3_done', message)
        self.slog('send->scanS3_done')
    def getFilePrefix(self, prefix):
        #if prefix.endswith('/'):
        #    return ''
        if ':' in prefix:
            return prefix.split(':')[-1].strip().split('/')[-1]
        else:
            return prefix.split('/')[-1]
    def getPrefix(self):
        #if prefix.endswith('/'):
        #    return ''
        prefix=self.prefix
        if ':' in prefix:
            return '/'.join(prefix.split(':')[-1].strip().split('/')[1:])
        else:
            return prefix
            
    @cli_exception
    def initList(self):
        self.slog('ListCtrl_Controller: initList: %s ' %  self.pid)
        self.DeleteAllItems()
        #self.Freeze()
        if 0:
            try:

                self.row_gen=self.get_S3_File_Chunk_gen()
                #self.file_gen=dump_S3ChunkToFile()
                self.data={}
                self.cid=0
                self.pid=0
                self.last_pid=0
                self.is_full=False
                self.ctrl_down = False
                self.setData()
                if 0:
                    for header, rows in row_gen:
                        self.data.update(rows)
                    self.itemDataMap = self.data
                

                for col in self.header:
                    self.InsertColumn(MAXINT, col)
                #self.InsertColumn(maxint, "Zahl")
                #self.InsertColumn(maxint, "Datum")
                if 0:
                    # Daten in ListCtrl schreiben
                    for key in sorted(self.data.keys()):
                        char_value, number_value, date_value = self.data[key]
                        index = self.InsertStringItem(MAXINT, char_value)
                        self.SetItemData(index, key) #muss sein
                        self.SetStringItem(index, 1, str(number_value))
                        self.SetStringItem(index, 2, date_value.strftime("%d.%m.%Y"))
                        self.SetColumnWidth(2, wx.LIST_AUTOSIZE)

                self.Refresh()
                print('Done.')
            except Exception as ex:
                self.del_busy()
                #self.show_msg()
                raise
    def getS3Client(self):

        session = boto3.Session()
              
        s3 = session.client('s3')
        return s3
    def download_file(self, bucket_name, s3_key, local_fn):
        try:
            with wx.WindowDisabler():
                uic.info = wx.BusyInfo(
                     wx.BusyInfoFlags()
                         .Parent(self)
                         .Icon(wx.ArtProvider.GetIcon(wx.ART_FIND,
                                                      wx.ART_OTHER, wx.Size(128, 128)))
                         .Title("<b>Downloading</b>")
                         .Text("Please wait...")
                         .Foreground(wx.WHITE)
                         .Background(wx.BLACK)
                         .Transparency( wx.ALPHA_OPAQUE/2)
                 )

                wx.GetApp().Yield()  
                s3= self.getS3Client()
                
                
                status=s3.download_file(bucket_name,s3_key, local_fn)
                print('Downloaded to ', local_fn, status)
                
        except:
            self.del_busy()
            #self.show_msg()
            raise
        self.del_busy()
        return status
    def _show_msg(self):
        dlg = wx.MessageDialog(self, format_stacktrace(), "Error",
                               wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
    def setData(self):
        self.header, rows = next(self.row_gen)
        #pp(rows)
        self.data.update(rows)
        pstart=CHUNK_SIZE*self.pid
        rcnt=len(rows)        
        self.itemDataMap = {x:self.data[x] for x in range(pstart, pstart+rcnt)}
        #pp(self.itemDataMap)
    def get_S3_File_Chunk_gen(self):
        gid=0
        chunk = self.list_s3_files_gen_v2(self.bucket_name,  MaxKeys=CHUNK_SIZE, plimit= 1_000_000)
        header = ['Id', 'Date','Key', 'Size']
        for cid, pd in enumerate(chunk):
            rows={}
            #gid=self.get_data(gid, pd, rows)
            for pid, ppl in enumerate(pd):
                #pp(ppl)
                #e()
                rows[gid] =(gid, pd[ppl]['LastModified'].strftime("%Y:%m:%d"), self.file_prefix+pd[ppl]['Key'].lstrip(self.prefix),pd[ppl]['Size'])
                gid +=1
            
            yield header, rows

    def list_s3_files_gen_v2(self, bucket_name,  MaxKeys=1000, plimit=1):
        dppl = boto3.client('s3')
        marker = None
        pid=0
        prefix=self.getPrefix()
        while True:
            paginator = dppl.get_paginator('list_objects_v2')
            response_iterator = paginator.paginate( Bucket=bucket_name, Prefix= prefix, MaxKeys=MaxKeys,
                PaginationConfig={
                    'ContinuationToken': marker})
            try:
                for page in response_iterator:
                          
                    out={}
                    if pid>=plimit: break
                    if 'Contents' in page:
                        plist = page['Contents']
                        for ppl in plist:
                            out[ppl['Key']]=ppl
                            #pp(ppl)
                            #e()
                        pid +=1
                    
                        yield out
                    else:
                        print(bucket_name, prefix)
                        #raise Exception(f'{bucket_name}, {prefix}')
                        yield out
            except Exception as ex:
               
                raise
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
