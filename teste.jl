x::Int
y::Int
z::String
z = "abc"
x = 1
y = x || (1==1)
println(x+y)