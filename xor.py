from pathlib import Path
import sys
from copy import deepcopy

if len(sys.argv) != 3:
    print("Usage: python xor.py <input_file.txt> <output_file.txt>")
    print("Example: python xor.py f.txt result.txt")
    sys.exit(1)

input_file = sys.argv[1]   # First argument after xor.py
output_file = sys.argv[2]  # Second argument


inBase_folder='testcase'
outBase_folder='testcaseoutput'
def read_text_file(filename):
    file_path = Path(inBase_folder) / filename
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None


text = read_text_file(input_file)

if text is None or len(text) < 4:
    print(f"Failed to read or parse {input_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("ERROR: Could not read input file\n")
    sys.exit(1)

# Safe parsing
try:
    vars_num = int(text[0])
    F_cubes = int(text[1])
    length = vars_num

    F = []
    for i in range(F_cubes):
        row = [int(char) for char in text[2 + i] if char.isdigit()]
        F.append(row)

    G_cubes = int(text[2 + F_cubes])
    G = []
    for i in range(G_cubes):
        row = [int(char) for char in text[3 + F_cubes + i] if char.isdigit()]
        G.append(row)

except Exception as e:
    print(f"Parsing error in {input_file}: {e}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("ERROR: Parsing failed\n")
    sys.exit(1)
## G and F cubelists are formed

def cofactor(M,var,polarity):
    length=len(M)
    P=deepcopy(M)
    for i in range(length):
        if M[i] != [] :
            if M[i][var]==polarity:
                P[i][var]=2
            elif M[i][var]==(1-polarity):
                P[i]=[]
        else :
            continue
    return P
## finish defying cofactor

def intersact(M,P):
    ##print(f"Here is the left part:\n'{M}'\n")
    ##print(f"Here is the right part:\n'{P}'\n")
    out=[]
    if not M or not P:
        return []
    for k in range(len(P)):    
        for j in range(len(M)):
            line=[]
            for i in range(length):
                if M[j][i]==P[k][i]:
                    line.append(M[j][i])
                elif M[j][i] ==2:
                    line.append(P[k][i])
                elif P[k][i] ==2:
                    line.append(M[j][i])
                else:
                    line.append(3)
            if 3 in line:
                continue
            else:
                out.append(line)
    print(f"Here is the out:'{out}'")
    return out

def union(M,P):
    result=deepcopy(P)
    for cube in M:
        if cube not in result:
            result.append(cube)
    return result

def duplicate(K):
    for x in K:
        seen=[]
        duplicate=[]
        if x not in seen:
            seen.append(x)
        else:
            duplicate.append(x)
    return [seen,duplicate]     
def simplified(M):
    not_dul=duplicate(M)[0]
    var_length=len(not_dul[0])
    cube_length=len(not_dul)
    for j in range(var_length):
        marker0=[]
        marker1=[]
        marker2=[]
        for i in range(cube_length):
            match M[i][j]:
                case 1:
                    marker1.append([i,j])
                case 2:
                    marker2.append([i,j])
                case 0:
                    marker0.append([i,j])
    if len(marker1)>1:
        counter=0
        for cube in marker1:
            if counter==0:
                not_dul[cube[0]]=[1]*var_length
                for element in range(var_length):
                    if element!=cube[1]:
                        not_dul[cube[0]][element]=2
            else:
                del not_dul[cube[0]]
            counter=counter+1
    

def split_var_cube(var,polarity):
    split_var_cube=[]
    for j in range(length):
        if j==var and polarity==1:
            split_var_cube.append(1)
        elif j==var and polarity==0:
            split_var_cube.append(0)
        else:
            split_var_cube.append(2)
    return split_var_cube


def complement(M,depth=0):
    print(f"Depth {depth}: Entering complement with M = {M}")
    mini=[10000,0,0]
    if [[]]*len(M) == M:                                   
        return [length * [2]]
    
    # Check if it contains the universal cube
    universal = [2] * length
    if universal in M:
        return []

    for j in range(length):
        counter0=0
        counter1=0
        for i in range(len(M)):
            if M[i]!=[]:
                match M[i][j]:
                    case 1:
                        counter1=counter1+1
                    case 0:
                        counter0=counter0+1
        if counter1 or counter0:
            print("counters of this column is:",counter1,counter0)
            print("column is:",j)
            if mini[0]>abs(counter1-counter0) or mini[2]<(counter1+counter0):
                mini[0]=abs(counter1-counter0)
                mini[2]=counter1+counter0
                mini[1]=j
                ## print(mini[1])
            else:
                continue
    print(mini[1])        
    cof_1=cofactor(M,mini[1],1)
    cof_0=cofactor(M,mini[1],0)
    if len(cof_1)>=1:
        cof_1=complement(cof_1,depth+1)
    if len(cof_0)>=1:
        cof_0=complement(cof_0,depth+1)   
    left=deepcopy(cof_1)
    if left==[length*[2]]:
        left=[split_var_cube(mini[1],1)]
    elif left==[]:
        left=[]
    else:
        left=intersact(left,[split_var_cube(mini[1],1)])
    right=deepcopy(cof_0)
    if right==[length*[2]]:
        right=[split_var_cube(mini[1],0)]
    elif right==[]:
        right=[]
    else:
        right=intersact(right,[split_var_cube(mini[1],0)])
    print("DEBUG - left  before intersact:", left)
    print("DEBUG - right before intersact:", right)
    result= union(left,right)
    print("union result is:",result)
    return result

# Compute complements
F_comp = complement(F)
G_comp = complement(G)

# F XOR G = (F · ~G) + (~F · G)
term1 = intersact(F, G_comp)
term2 = intersact(F_comp, G)
xor_result = union(term1, term2)

# Output
def output_files(file):
    file_path=Path(outBase_folder)/file
    print("Final XOR result:", xor_result)
    with open(file_path, 'w', encoding='utf-8') as f:
        if xor_result!=[]:
            f.write('variable length: '+str(len(xor_result[0]))+'\n')
            f.write('cube length: '+str(len(xor_result))+'\n')
            f.write('XOR output cubelist: \n')
            for cube in xor_result:
                f.write(' '.join(map(str, cube)) + '\n')
        else:
            f.write('empty list, they are identical.\n'+str(xor_result))
    print(f"Success! Result written to {output_file}")
output_files(output_file)
            
        
