import json
import sys

def transform_json(input_file, output_file):
    """
    Transforms the JSON structure by extracting the 'code' fields from each 'instance'
    into a 'code' list. Handles cases where instances may be plain strings or objects.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    transformed_data = []
    for module in data:
        # Copy all keys except 'instances'
        new_module = {k: v for k, v in module.items() if k != "code"}
        codes = []
        for inst in module.get("code", []):
            if isinstance(inst, dict) and "code" in inst:
                codes.append(inst["code"])
            elif isinstance(inst, str):
                # If instance is already a code string
                codes.append(inst)
            else:
                # Unexpected format; skip
                continue
        new_module["code"] = codes
        transformed_data.append(new_module)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transformed_data, f, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert.py <input_json> <output_json>")
        sys.exit(1)

    input_json = sys.argv[1]
    output_json = sys.argv[2]
    transform_json(input_json, output_json)
    print(f"Transformed JSON saved to {output_json}")
