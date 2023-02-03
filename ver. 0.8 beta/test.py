class a:
    def __init__(self,b,c):
        self.b = b
        self.c = c

d=a(1,2)
e=a(4,3)
f=[d,e]

z=f.index(a(1,2))
print(z)