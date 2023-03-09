from bbase.hn_type_ladders import *

l=2
mult={(0,2):[2,[[0,1,2],[1,3,3]]],(0,1):[1,[[2,2]]],(1,2):[1,[[4,3]]]}
print(mult[0,1][1])
ans=update_barcode(mult,1,l)
print(ans)
