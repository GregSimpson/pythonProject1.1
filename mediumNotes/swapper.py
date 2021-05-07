
a = 100
b = 200
c = 300

a,b,c = c,b,a
print ( "The a=%(a)s is b=%(b)s  c=%(c)s." % locals() )

a,b,c = c,b,a
print ( "The a=%(a)s is b=%(b)s  c=%(c)s." % locals() )

