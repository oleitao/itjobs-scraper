import subprocess
import simplejson as json

try:
    return_code = subprocess.run(
        ["python", "etl/extraction.py"],
        capture_output=True,
        text=True,
        check=True
    )
    print("Exit extraction status code:", return_code)

    extraction_json=return_code.stdout.strip()
    print(extraction_json)

    try:
        return_code = subprocess.run(
            ["python", "etl/transformation.py", extraction_json],
            capture_output=True,
            text=True,
            check=True
        )
        print("Exit transformation status code:", return_code.returncode)

        unique_companies = return_code.stdout.strip()
        # print("Unique companies:", unique_companies)

        try:
            return_code = subprocess.call(["python", "etl/load.py", unique_companies])
            print("Exit load status code:", return_code)
        except subprocess.CalledProcessError as e:
            print(f"Load script failed with return code {e.returncode}")

    except subprocess.CalledProcessError as e:
        print(f"Transformation script failed with return code {e.returncode}")

except subprocess.CalledProcessError as e:
    print(f"Extraction script failed with return code {e.returncode}")
