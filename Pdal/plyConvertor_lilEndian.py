import os
import json
import subprocess

# Directory containing .las files
las_dir = os.path.expanduser("~/Open3D/Pdal/soal-3-lidar")
output_dir = os.path.expanduser("~/Open3D/Pdal/ply_output")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get all .las files in the directory
las_files = [f for f in os.listdir(las_dir) if f.endswith('.las')]

for las_file in las_files:
    # Create the pipeline JSON for each file
    pipeline = {
        "pipeline": [
            {
                "type": "readers.las",
                "filename": os.path.join(las_dir, las_file)
            },
            {
                "type": "writers.ply",
                "filename": os.path.join(output_dir, las_file.replace('.las', '.ply')),
                "storage_mode": "little endian"  # Changed from "binary" to "default"
            }
        ]
    }

    # Write the pipeline to a temporary file
    pipeline_file = os.path.join(output_dir, f"pipeline_{las_file}.json")
    with open(pipeline_file, 'w') as f:
        json.dump(pipeline, f, indent=2)

    # Execute PDAL pipeline
    subprocess.run(["pdal", "pipeline", pipeline_file])
    print(f"Converted {las_file} to PLY format")