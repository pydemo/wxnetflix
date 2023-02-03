import os, sys
import copy, inspect

from pydispatch import dispatcher

from pprint import pprint as pp
import traceback
try:
    import cStringIO
except ImportError:
    import io as cStringIO
    
from traceback import print_exc	




def reciever(f):
    def wrapper(*args, **kwargs):
        #debug('SIGNAL: %s->%s: [%s] [%s]' % (kwargs['sender'].cn, args[0].cn, kwargs['signal'], kwargs['message']))
        return f(*args, **kwargs)
    return wrapper
    
    
class Base(object):
    def __init__(self, parent=None):
        self.parent=parent
        self.keep_alive=False
        self.cn = self.__class__.__name__
        self.sub('Ctrl_L')
    @reciever
    def Ctrl_L(self, message, arg2=None, **kwargs):
        sender=message
        if self.__class__.__name__ == sender.Parent.__class__.__name__:
            print('Ctrl_L', self.__class__.__name__,sender.Parent.__class__.__name__)
            if (self.Id==sender.Parent.Id):
                
                print('id', self.Id,sender.Parent.Id)
                self.send("previewLayout",())
        
    def getParents(self):
        obj=self
        yield obj
        while obj:
            parent = obj.GetParent()
            if parent:
                yield parent
            obj=parent

    def sub(self, signal):
        #debug('SUB: %s: %s' % (self.cn,signal))
        assert hasattr(self, signal)
        dispatcher.connect(getattr(self, signal), signal=signal, sender=dispatcher.Any)
    def send(self, sig, msg):
        #debug('SEND: %s: %s [%s]' % (self.cn,sig, msg))
        dispatcher.send(sig, message=msg, sender=self)
    def flog(self, msg):
        self.send('filterlog', msg)
    def slog(self, msg):
        self.send('navlog', msg)
    def gen_bind(self, type, instance, handler, *args, **kwargs):
        
        self.Bind(type, lambda event: handler(event, *args, **kwargs), instance)

    def copy(self, ref):
        return copy.deepcopy(ref)
        
    def getEditPath(self, gs):
        obj= gs[self.__class__.__name__]
        path=None
        try:
            
            path = inspect.getfile(obj)	
            
        except Exception as ex:
            extype = type(ex).__name__
            if extype == 'TypeError':
                if 0:
                    err_log = cStringIO.StringIO()
                    traceback.print_exc(file=err_log)
                    err = err_log.getvalue()
                    error(err)
                if 1:
                    import sys, os
                    home=os.path.abspath(sys.modules[self.__class__.__module__].__file__)
                    path = os.path.join(home, self.__class__.__module__)
                

            else:
                raise

            if 0:
                print_exc()
                print ('type is:', e.__class__.__name__)
                print(type(e).__name__)
                print(e.args)
                pp(e)

            if 0:
                tb = sys.exc_info()
                print(e.with_traceback(tb[2]))
            
            if 0:
                type1, val, tb = sys.exc_info()
                print(type1, val, tb)
            
            if 0:
                err_log = cStringIO.StringIO()
                traceback.print_exc(file=err_log)
                err = err_log.getvalue()
                
            
                error(err)
                pp(err_log)
        return 	path

    def getEditConfigPath(self, gs):
        obj= gs[self.__class__.__name__]
        fn=None
        try:
            fn = inspect.getfile(obj)	
        except:
            pass
        if fn:		
            name, ext = os.path.splitext(fn)
            return '%sConfig%s' % (name, ext)	
        else:
            return False

        
        


