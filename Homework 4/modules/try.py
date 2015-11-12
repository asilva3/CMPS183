function_list = []
for i in range(5):
    def f(x=i):
        return x
    function_list.append(f)

print i
for f in function_list:
    print f()
