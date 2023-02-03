from ui_layer.UiLayout import UiLayout


def init(**kwargs):
    global  uilyt
    pipeline=kwargs['pipeline']
    uilyt = UiLayout(pipeline)

    