
data = { 'name': 'Eric',
         'age' : 38,
         'country' : 'NL'}

print ( "%(name)s is %(age)i and lives in %(country)s" % data  )


foo, bar = 'question', 123
print ( "The %(foo)s is %(bar)i." % locals() )

