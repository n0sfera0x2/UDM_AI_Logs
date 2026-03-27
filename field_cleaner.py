import json
import re

def clean_udm_field(raw_udm):
    # Fix the "doubled up" issue (target.iptarget.asset.ip -> target.ip)
    # This regex looks for a second 'target.' or 'metadata.' etc. starting mid-string
    prefixes = ['metadata', 'principal', 'target', 'observer', 'network', 'about', 'security_result']
    pattern = f"(.+?)({'|'.join(prefixes)})\\."
    match = re.search(pattern, raw_udm)
    
    if match:
        return match.group(1).strip()
    return raw_udm.strip()

def convert_to_clean_jsonl(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    with open(output_file, 'w') as f_out:
        for entry in data:
            product = entry.get('product', 'Unknown').replace('收集 ', '').replace(' 日志', '')
            mappings = entry.get('mappings', [])

            for m in mappings:
                raw_fld = m['log_field']
                # Clean the UDM field using our helper
                clean_udm = clean_udm_field(m['udm_field'])
                
                if not clean_udm or clean_udm.lower() == "n/a":
                    continue

                # Compact, high-signal format
                # Using '###' as a block separator is common in fine-tuning
                formatted_line = {
                    "text": f"### VDR: {product} | SRC: {raw_fld} | UDM: {clean_udm} <|endoftext|>"
                }
                
                f_out.write(json.dumps(formatted_line) + '\n')

if __name__ == "__main__":
    convert_to_clean_jsonl('udm_training_corpus.json', 'udm_clean_train.jsonl')
      
