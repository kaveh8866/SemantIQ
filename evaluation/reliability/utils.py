import pandas as pd
import numpy as np
import hashlib
import json

def load_ratings(file_path):
    """
    Load ratings from CSV and pivot into Subjects x Raters matrix.
    Assumes standard schema: rater_id, run_id, question_id, [criteria...]
    """
    df = pd.read_csv(file_path)
    return df

def create_reliability_matrix(df, criterion='semantic_alignment'):
    """
    Pivot dataframe to create a matrix for reliability calculation.
    Rows: Subjects (run_id + question_id)
    Cols: Raters (rater_id)
    Values: Score for the given criterion
    """
    # Create a unique subject ID
    df['subject_id'] = df['run_id'] + "::" + df['question_id']
    
    # Pivot
    matrix = df.pivot(index='subject_id', columns='rater_id', values=criterion)
    return matrix

def generate_data_manifest(file_paths, version_info):
    """
    Generate a manifest of data files for reproducibility.
    """
    manifest = {
        "timestamp": pd.Timestamp.now().isoformat(),
        "versions": version_info,
        "files": {}
    }
    
    for label, path in file_paths.items():
        try:
            with open(path, 'rb') as f:
                content = f.read()
                file_hash = hashlib.sha256(content).hexdigest()
            manifest["files"][label] = {
                "path": str(path),
                "sha256": file_hash
            }
        except FileNotFoundError:
            manifest["files"][label] = {"error": "File not found"}
            
    return manifest
