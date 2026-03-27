# XOR-URP-algorithm


# Part A:Deciding algorithm flow
Firstly we have to know how many variables there is so that our PCN can design correctly.
Input:3
inner loop 3
Secondly we have to know how many cubes there are.
Input:2
outer loop 2
then start reading,
e.g.
3
2
11 01 10
01 10 10
yet in this programe we use 0:10 1:01 2:11
Next we have to find a place to store this cube, either 3x2 2d list?
then it would be
0,0:2 1,0:1 2,0:0
0,1:1 0,2:0 0,3:0
this is the F function another function G needs a thrid layer of loop.
so let F= first 2d list
       G= second 2d list
then we have to do a splitting unate complement function.
If a cofactor of F such as F(x=1)=222 or F(x=1)=011, then we terminate the function and return 0 or 1(value)
else just keep dividing.
But we have to check which column has the binate var, and lowest diff of 1,0.

E.G. F=[111,212,001]
then we check column 1, counter for non 2, start result in a max var. after loop all columns, split at the max non 2 column.
now split at second column, F(y=1), have to set all 1 to 2, and row having 0 gone(remove that 1d list in 2d list for F(y=1)). opp for F(y=0).
F(y=1)=[121,222], since we are checking each element and correct it, at the same time make a counter to count 2 in a row, 3:since there is a line full of 222 this is our termination. F(y=1)=0.
F(y=0)=[021], now keep spliting at x,,
Fybar(x=1)=[], return 1,
Fybar(x=0)=[221].
fybarxbar(z=1)=[222] return 0
fybarxbar(z=0)=[] return 1.

recursive, if F is not 0/1, compcof(F)=(split column)*compcof(F_cof+)+(split column) *compcof(negF_cof-)

Maybe this cofactor process can be also wrap into a function taking column num to know where to split.

# Part B: Testcase generation
Each time generate 10 files of testcase_num.txt in testcase folder.
For each F and G,
random generate a num for var number 1-20 and 1-1000 cubes.
and then go into a 2 layer looping to assign each element 0/1/2

# Part C: XOR algorithm output flow
if F or G not those critiria, then go to part A and check again with a smaller XOR problem. 