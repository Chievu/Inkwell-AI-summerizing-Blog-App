from transformers import pipeline

# Load summarization pipeline once
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text, max_length=120, min_length=30):
    """
    Summarize a blog post text using Hugging Face transformer.
    
    Args:
        text (str): The full blog post text to summarize.
        max_length (int): Maximum number of tokens in the summary.
        min_length (int): Minimum number of tokens in the summary.
    
    Returns:
        str: Summarized text.
    """
    if len(text.split()) < 50:
        return text  # Text is too short, no need to summarize
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']
