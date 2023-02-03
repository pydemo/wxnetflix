from cli_layer.AppConfig import AppConfig

def init(**kwargs):
    global apc
    apc = AppConfig(**kwargs)