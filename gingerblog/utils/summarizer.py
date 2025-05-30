from transformers import pipeline

# Cache the summarizer instance
_summarizer = None

def summarize_text(text, max_length=120, min_length=30):
    """
    Summarize a blog post text using Hugging Face transformer.
    Lazy-loads and reuses the summarizer pipeline.
    """
    global _summarizer

    if len(text.split()) < 50:
        return text  # just return the text since its too short to summerize

    if _summarizer is None:
        _summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    summary = _summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

