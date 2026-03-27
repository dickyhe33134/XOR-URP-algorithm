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

        # Start the timer for this specific test case!
        test_start_time = time.time()

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10000000,
                check=False
            )
            
            # Stop the timer the moment the subprocess finishes
            test_elapsed = time.time() - test_start_time

            if result.returncode == 0:
                success += 1
                print(f"[{i:4d}/{len(input_files)}] ✓ {filename_only} → Success (took {test_elapsed:.4f}s)")
            else:
                failed += 1
                print(f"[{i:4d}/{len(input_files)}] ✗ {filename_only} → Failed (took {test_elapsed:.4f}s)")
                if result.stderr:
                    print("   Error:", result.stderr.strip()[-400:])

        except subprocess.TimeoutExpired:
            test_elapsed = time.time() - test_start_time
            failed += 1
            print(f"[{i:4d}/{len(input_files)}] ✗ {filename_only} → Timeout (took {test_elapsed:.4f}s)")
            
        except Exception as e:
            test_elapsed = time.time() - test_start_time
            failed += 1
            print(f"[{i:4d}/{len(input_files)}] ✗ {filename_only} → Exception: {e} (took {test_elapsed:.4f}s)")

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