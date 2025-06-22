from transformers import pipeline

gen_pipe = pipeline("text2text-generation", model="google/flan-t5-base")

def generate_feedback(journal_text, mood):
    prompt = f"Give an empathetic response to someone feeling {mood} who wrote: {journal_text}"
    result = gen_pipe(prompt, max_length=80, do_sample=True)[0]['generated_text']
    return result
