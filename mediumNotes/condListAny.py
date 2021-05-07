
score=120
wickets=7
catch=2
list_cond=[score>320,
           wickets<8,
           catch>3]
if(any(list_cond)):
    print("At least 1 cond passed")
else:
    print("all conds failed")
