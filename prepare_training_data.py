import json

def convert_to_jsonl(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    with open(output_file, 'w') as f_out:
        count = 0
        for entry in data:
            product = entry.get('product', 'Unknown Vendor')
            mappings = entry.get('mappings', [])

            for m in mappings:
                # Constructing a clear, instructional prompt
                prompt = f"Map the following {product} log field to its Google UDM equivalent: {m['log_field']}"
                
                # The expected completion (the UDM path)
                completion = m['udm_field']

                # Standard OpenAI/Vertex AI fine-tuning structure
                # Note: You can adjust these keys based on your specific LLM provider
                json_line = {
                    "prompt": prompt,
                    "completion": f" {completion}" # Leading space is a common LLM tokenization best practice
                }
                
                f_out.write(json.dumps(json_line) + '\n')
                count += 1
        
        print(f"Successfully converted {count} mapping pairs to {output_file}")

if __name__ == "__main__":
    convert_to_jsonl('udm_training_corpus.json', 'udm_fine_tuning.jsonl')
