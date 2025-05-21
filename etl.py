import subprocess

try:
    # subprocess.run(["python", "extractions.py"], check=True)
    return_code = subprocess.call(["python", "extraction.py"])
    print("Exit extraction status code:", return_code)
    
    try:
        # subprocess.run(["python", "transformation.py"], check=True)
        return_code = subprocess.call(["python", "transformation.py"])
        print("Exit transformation status code:", return_code)
    except subprocess.CalledProcessError as e:
        print(f"Transformation script failed with return code {e.returncode}")

except subprocess.CalledProcessError as e:
    print(f"Extraction script failed with return code {e.returncode}")


