import pandas as pd
import torch

from typing import Tuple
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

model_name_cls = "sdbrgo/roberta-tagalog-sentiment-multiclass-classifier"
model_name_reg = "sdbrgo/roberta-tagalog-sentiment-intensity-regressor"

tokenizer = AutoTokenizer.from_pretrained(model_name_cls)

model_cls = AutoModelForSequenceClassification.from_pretrained(model_name_cls)
model_reg = AutoModelForSequenceClassification.from_pretrained(model_name_reg)

clf_pipeline = pipeline(
    "text-classification",
    model=model_cls,
    tokenizer=tokenizer,
    return_all_scores=False
)

reg_pipeline = pipeline(
    "text-classification",   # still this, but we interpret logits manually
    model=model_reg,
    tokenizer=tokenizer,
    function_to_apply="none"  # VERY IMPORTANT for regression
)

def transform_sentiments(df):
    processed_df = df.copy()
    texts = processed_df["text"].tolist()

    # --- sentiment classification ---
    cls_outputs = clf_pipeline(texts)
    processed_df["label"] = [o["label"] for o in cls_outputs]
    processed_df["sentiment_confidence"] = [o["score"] for o in cls_outputs]

    # --- sentiment intensity regression ---
    reg_outputs = reg_pipeline(texts)

    # each output looks like: [{'score': tensor([[value]])}]
    processed_df["intensity"] = [
        float(o["score"]) for o in reg_outputs
    ]

    return processed_df

def compute_sentiment_metrics(processed_df, feedback_volume, multiplier_cap=0.7):
    if feedback_volume == 0:
        return {
            "w_pos": 0.0,
            "w_neg": 0.0,
            "w_neu": 0.0
        }
    
    df = processed_df.copy()

    LABEL_MAP = {
        0: "neg",
        1: "neu",
        2: "pos"
    }
    df["label"] = df["label"].map(LABEL_MAP)

    # ----- 1. get ratio of pos, neg, neu labels -----
    label_counts = df["label"].value_counts()
    
    # ===== DEBUGGING =====
    label_dtype = df["label"].dtype
    print(label_dtype)
    # =====================

    raw_sentiment_ratios = {
        label: label_counts.get(label, 0) / feedback_volume
        for label in ["neg", "neu", "pos"]
    }

    # ----- 2. get sum of intensity scores per label -----
    intensity_sums = df.groupby("label")["intensity"].sum().to_dict()

    # ensure all labels exist
    intensity_sums = {
        label: intensity_sums.get(label, 0.0)
        for label in ["neg", "neu", "pos"]
    }

    # ----- 3. compute multiplier per label -----
    total_intensity = sum(intensity_sums.values())

    if total_intensity == 0:
        weight_multipliers = {label: 1.0 for label in intensity_sums}
    else:
        weight_multipliers = {
            label: 1.0 + multiplier_cap * (intensity_sums[label] / total_intensity)
            for label in intensity_sums
        }

    # ----- 4. compute weighted sentiment ratio (WSR) -----
    w_pos = raw_sentiment_ratios["pos"] * weight_multipliers["pos"]
    w_neg = raw_sentiment_ratios["neg"] * weight_multipliers["neg"]
    w_neu = raw_sentiment_ratios["neu"] * weight_multipliers["neu"]

    return {
        "w_pos": w_pos,
        "w_neg": w_neg,
        "w_neu": w_neu,
        "raw_sentiment_ratio": raw_sentiment_ratios,
    }