def inject_real_var_names(function):
    from functools import wraps
    import inspect, re
    pattern = r'{}\s*\(([A-Za-z_\s\'\"][A-Za-z0-9_\s,\'\"=]*)\s*\)'
    @wraps(function)
    def function_with_real_vars(*args,**kwargs):
        func_name = function.__name__
        formal_vars = function.__code__.co_varnames[:function.__code__.co_argcount]
        real_vars = ['',]*len(formal_vars)
        realname = {}
        m = None
        
        for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
            m = re.search(pattern.format(func_name), line) or m
        if m:
            real_vars = [v.strip() for v in m.group(1).split(',') if v.find('=')==-1]
            real_vars2 = dict([v.strip().split('=') for v in m.group(1).split(',') if v.find('=')!=-1])

        
        realname = dict(zip(formal_vars ,real_vars))
        function_with_real_vars.__setattr__("_realname",{**realname,**real_vars2})
        
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
def family(father,mother):
    formal_var = get_varname(father)
    real_var = family._realname[formal_var]
    print('The formal parameter "{}"\'s real parameter is "{}", and it\'s value is "{}"!'
          .format(formal_var,real_var,father))


if __name__ == '__main__':
    man = "Ken"
    
    family(man,"Kitty")
    family(mother="Kitty",father=man)
    
