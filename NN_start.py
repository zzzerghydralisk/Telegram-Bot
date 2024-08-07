from transformers import AutoTokenizer, AutoModelForCausalLM

access_token='XXX'

tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b")
model = AutoModelForCausalLM.from_pretrained("google/gemma-2b", token=access_token)



def main_generate(prompt):
    input_text = prompt
    input_ids = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(**input_ids)
    return(tokenizer.decode(outputs[0]))