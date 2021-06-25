# inject_real_var_names

```
@inject_real_var_names
def foo(a,b):
    formal_var = get_varname(a)
    real_var = foo._realname[formal_var]
    print('''The formal parameter "{}"\'s 
           real parameter is "{}", 
           and it\'s value is "{}"!'''
          .format(formal_var,real_var,a))


if __name__ == '__main__':
    jacob = 233
    
    foo(jacob,"hello")
    foo(b="hello",a=jacob)
```
The output of the above script is as follows:
>The formal parameter "a"'s real parameter is "jacob", and it's value is "233"!
>
>The formal parameter "a"'s real parameter is "jacob", and it's value is "233"!

Are you interested in?
