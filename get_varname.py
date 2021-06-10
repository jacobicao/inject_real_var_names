def inject_real_var_names(function):
    from functools import wraps
    import inspect, re
    pattern = r'{}\s*\(([A-Za-z_\s\'\"][A-Za-z0-9_\s,\'\"=]*)\s*\)'
    @wraps(function)
    def function_with_real_vars(*args,**kwargs):
        func_name = function.__name__
        formal_vars = function.__code__.co_varnames
        real_vars = ['',]*len(formal_vars)
        realname = {}
        m = None
        
        for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
            m = re.search(pattern.format(func_name), line) or m
        if m:
            real_vars = [v.strip().split('=')[-1] for v in m.group(1).split(',')]
        
        realname = dict(zip(formal_vars ,real_vars))
        function_with_real_vars.__setattr__("_realname",realname)
        
        result = function(*args,**kwargs)
        return result
        
    return function_with_real_vars


def get_varname(p):
    '''Do not use it two times in same line.'''
    import inspect, re
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'get_varname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
    if m:
        return m.group(1)


@inject_real_var_names
def foo(a,b):
    formal_var = get_varname(a)
    real_var = foo._realname[formal_var]
    print('The formal parameter "{}"\'s real parameter is "{}", and it\'s value is "{}"!'
          .format(formal_var,real_var,a))


if __name__ == '__main__':
    jacob = 233
    
    #  函数内获取实参名
    foo(jacob,"hello")
    foo(a=jacob,b="hello")
    
