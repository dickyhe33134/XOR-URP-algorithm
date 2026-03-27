import random
import os
from pathlib import Path

def generate_testcase(var_count, max_cubes):
    """Generate one testcase in the required format"""
    lines = []
    
    # Variable count
    lines.append(str(var_count))
    
    # F cubes
    f_cubes = random.randint(1, max_cubes)
    lines.append(str(f_cubes))
    
    for _ in range(f_cubes):
        cube = [random.choice([0, 1, 2]) for _ in range(var_count)]
        lines.append(''.join(map(str, cube)))
    
    # G cubes
    g_cubes = random.randint(1, max_cubes)
    lines.append(str(g_cubes))
    
    for _ in range(g_cubes):
        cube = [random.choice([0, 1, 2]) for _ in range(var_count)]
        lines.append(''.join(map(str, cube)))
    
    return lines


def main():
    num_testcases = 10
    output_dir = Path("testcase")
    output_dir.mkdir(exist_ok=True)
    
    print(f"Generating {num_testcases} testcases...")
    
    for i in range(num_testcases):
        # Randomly vary number of variables between 3 and 8
        var_count = random.randint(2, 20)
        
        testcase = generate_testcase(var_count=var_count,max_cubes=1000)
        
        filename = output_dir / f"testcase{i+1}in.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(testcase))
        
        if (i + 1) % 100 == 0:
            print(f"Generated {i+1}/{num_testcases} testcases...")
    
    print(f"Done! {num_testcases} testcases generated in folder: {output_dir}")


if __name__ == "__main__":
    main()