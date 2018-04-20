# Util functions that are needed but messy.
def remove_none(d: dict): # Made by https://github.com/LewdNeko ;^)
    for item in d.copy():
        if isinstance(d[item], dict):
            if len(d[item]):
                d[item] = none_remover(d[item])
            else:
                del d[item]
        elif d[item] is None:
            del d[item]
    return d
