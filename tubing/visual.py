from tubing.sink import LoopingSink

def dump(source, series, sink):
    _source =  """(##%s##) --> """ % type(source).__name__
    print(_source, end="")
    tube_str_len = 0
    for tube in series:
        _tube = """ |===%s===|  -->""" % tube._name
        if tube == series[-1]:
           if isinstance(sink, LoopingSink):
              print(_tube[:-4], end="")
        else:
              print(_tube, end="")
        tube_str_len += len(_tube)
    if isinstance(sink, LoopingSink):
       print('\n     ^' + ' ' * (tube_str_len - 5) + '||')
       print('     ||' + ' ' * (tube_str_len-6) + '||')
       print('     ||' + int((tube_str_len-len(type(sink).__name__)) / 2 - 1) * '=' + '(' + type(sink).__name__ + ')' + int((tube_str_len-len(type(sink).__name__)) / 3 ) * '=' + '<--||')
    else:
      _source =  """ [##%s##]""" % type(sink).__name__
      print(_source)
