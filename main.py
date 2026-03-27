import subprocess
from pathlib import Path
import time

def main():
    input_dir = Path("testcase")
    output_dir = Path("testcaseoutput")
    output_dir.mkdir(exist_ok=True)

    input_files = sorted(input_dir.glob("*in.txt"))

    print(f"Found {len(input_files)} test cases.\n")
    start_time = time.time()

    success = 0
    failed = 0

    for i, input_file in enumerate(input_files, 1):
        # Use only the filename (not full path), because xor.py adds the folder itself
        filename_only = input_file.name
        
        # Create output filename
        num_str = filename_only.replace("testcase", "").replace("in.txt", "")
        output_file = output_dir / f"testcase{num_str}out.txt"

        # Show the exact command that will be executed (for debugging)
        cmd = ["python", "xor.py", filename_only, str(output_file.name)]
        print(f"[{i:4d}/{len(input_files)}] Running: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=20,
                check=False
            )

            if result.returncode == 0:
                success += 1
                print(f"[{i:4d}/{len(input_files)}] ✓ {filename_only} → Success")
            else:
                failed += 1
                print(f"[{i:4d}/{len(input_files)}] ✗ {filename_only} → Failed")
                if result.stderr:
                    print("   Error:", result.stderr.strip()[-400:])

        except subprocess.TimeoutExpired:
            failed += 1
            print(f"[{i:4d}/{len(input_files)}] ✗ {filename_only} → Timeout")
        except Exception as e:
            failed += 1
            print(f"[{i:4d}/{len(input_files)}] ✗ {filename_only} → Exception: {e}")

        if i % 50 == 0:
            print(f"--- Progress: {i}/{len(input_files)} completed ---\n")

    total_time = time.time() - start_time

    print("\n" + "="*70)
    print("BATCH PROCESSING COMPLETED")
    print("="*70)
    print(f"Total test cases : {len(input_files)}")
    print(f"Successful       : {success}")
    print(f"Failed           : {failed}")
    print(f"Total time       : {total_time:.2f} seconds")


if __name__ == "__main__":
    main()