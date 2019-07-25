func_names = ['update_instance_dates.py',
              'update_instance_hidden.py']

for i in func_names:
    exec(open(i).read())
