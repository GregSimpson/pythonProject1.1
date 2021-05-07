score=325
wickets=7
catch=4
list_cond=[score>320,
           wickets<8,
           catch>3]
if(all(list_cond)):
    print(" all cond's passed")
else:
    print("at least 1 condition Failed")
