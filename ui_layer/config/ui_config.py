from ui_layer.UiConfig import UiConfig

def init(**kwargs):
    global uic
    uic = UiConfig(**kwargs)
    uic.kwargs=kwargs