import gradio as gr

from phase.ingestion import ingest_feedback, ingest_adoption
from phase.sentiment_modeling import transform_sentiments, compute_sentiment_metrics
from phase.compute import ParticipationAdoptionIndex
from phase.interpret import assign_typology

def run_app(feedback_file, adoption_file, num_participants, target_population, high_th, th):
    # ----- input validation -----
    if high_th <= th:
        raise ValueError("High impact threshold must be greater than medium impact threshold.") 
    
    # Step 1: Ingest data
    df, feedback_volume = ingest_feedback(feedback_file)
    participants_by_group = ingest_adoption(adoption_file)

    # Step 2: Sentiment modeling
    processed_df = transform_sentiments(df)
    sentiment_metrics = compute_sentiment_metrics(processed_df, feedback_volume)

    w_pos = sentiment_metrics["w_pos"]
    w_neg = sentiment_metrics["w_neg"]

    # Step 3: Compute Participation Adoption Index (PAI)
    pai_calculator = ParticipationAdoptionIndex(
        num_participants=num_participants,
        target_population=target_population,
        feedback_volume=feedback_volume,
        w_pos=w_pos,
        w_neg=w_neg
    )

    pai = pai_calculator.compute_pai(participants_by_group)

    # Step 4: Interpret results
    typology = assign_typology(pai, high_th, th)

    return sentiment_metrics, typology

# ========== GRADIO INTERFACE ==========
with gr.Blocks() as demo:
    gr.Markdown("# Peopulse: Citizen Feedback Intelligence System")

    # ----- INPUTS -----
    feedback_file_input = gr.File(label="Upload Feedback Data (CSV)")
    adoption_file_input = gr.File(label="Upload Adoption Data (CSV)")
    num_participants_input = gr.Number(
        label="Number of Participants",
        value=1000,
        minimum=0,
        maximum=1e9,
        step=1,
        precision=0
    )
    target_population_input = gr.Number(
        label="Target Population Size",
        value=10000,
        minimum=1,
        maximum=1e10,
        step=1,
        precision=0
    )
    high_th_input = gr.Number(
        label="High Impact Threshold",
        value=0.4,
        minimum=0.0,
        maximum=1.0,
        step=0.01,
        precision=2
    )
    th_input = gr.Number(
        label="Medium Impact Threshold",
        value=0.2,
        minimum=0.0,
        maximum=1.0,
        step=0.01,
        precision=2
    )
    btn = gr.Button("Run Evaluation")

    # ----- OUTPUTS -----
    gr.Markdown("## Results")
    sentiment_metrics_output = gr.JSON(label="Sentiment Metrics")

    gr.Markdown("## Program Diagnosis")
    typology_output = gr.JSON(label="Typology Assignment")

    btn.click(
        fn=run_app,
        inputs=[feedback_file_input, adoption_file_input, num_participants_input, target_population_input, high_th_input, th_input],
        outputs=["sentiment_metrics_output", "typology_output"]
    )
