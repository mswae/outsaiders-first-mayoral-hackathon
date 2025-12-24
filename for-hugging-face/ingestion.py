import pandas as pd
import os
import warnings

def ingest_feedback(file):
    feedback_df = pd.read_csv(file)
    feedback_volume = feedback_df.shape[0]

    return feedback_volume, feedback_volume

def ingest_adoption(file):

    # --- Validation ---
    if file is None or file == "":
        warnings.warn("Adoption file is empty; participants_by_group will be empty")
        return {}
    
    if not os.path.exists(file):
        warnings.warn("Adoption file is empty; participants_by_group will be empty")
        return {}
    
    adoption_df = pd.read_csv(file)

    if adoption_df.empty:
        warnings.warn("Adoption file is empty; participants_by_group will be empty")
        return {}
    
    # handle missing required column
    if "barangay" not in adoption_df.columns:
        raise ValueError("Adoption data must contain \"barangay\" column.")

    participants_by_group = adoption_df.groupby("barangay").size().to_dict()

    return participants_by_group