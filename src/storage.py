import json
import os
from deepdiff import DeepDiff
from .schemas import AccountMemo, AgentSpec

# Saves versioned configurations to the output directory
def save_version(account_id: str, version: str, memo: AccountMemo, spec: AgentSpec, output_dir: str = "output"):
    base_path = os.path.join(output_dir, account_id, version)
    os.makedirs(base_path, exist_ok=True)
    
    with open(os.path.join(base_path, "account_memo.json"), "w") as f:
        json.dump(memo.model_dump(), f, indent=4)
        
    with open(os.path.join(base_path, "agent_spec.json"), "w") as f:
        json.dump(spec.model_dump(), f, indent=4)

# Loads a specific version of a configuration
def load_version(account_id: str, version: str, output_dir: str = "output") -> tuple[AccountMemo, AgentSpec]:
    base_path = os.path.join(output_dir, account_id, version)
    
    with open(os.path.join(base_path, "account_memo.json"), "r") as f:
        memo_data = json.load(f)
        
    with open(os.path.join(base_path, "agent_spec.json"), "r") as f:
        spec_data = json.load(f)
        
    return AccountMemo(**memo_data), AgentSpec(**spec_data)

# Compares v1 and v2 to generate a human-readable changelog
def generate_changelog(account_id: str, v1_memo: AccountMemo, v2_memo: AccountMemo, output_dir: str = "output"):
    diff = DeepDiff(v1_memo.model_dump(), v2_memo.model_dump(), ignore_order=True)
    
    changelog_path = os.path.join(output_dir, account_id, "changelog.txt")
    
    with open(changelog_path, "w") as f:
        f.write("=== CHANGELOG (v1 -> v2) ===\n\n")
        
        if not diff:
            f.write("No changes detected.\n")
            return
            
        if 'values_changed' in diff:
            f.write("--- Values Changed ---\n")
            for path, change in diff['values_changed'].items():
                clean_path = path.replace("root['", "").replace("']", "")
                f.write(f"- {clean_path}:\n")
                f.write(f"    From: {change['old_value']}\n")
                f.write(f"    To:   {change['new_value']}\n\n")
                
        if 'dictionary_item_added' in diff:
            f.write("--- Items Added ---\n")
            for item in diff['dictionary_item_added']:
                f.write(f"- {item}\n")
                
        if 'dictionary_item_removed' in diff:
            f.write("--- Items Removed ---\n")
            for item in diff['dictionary_item_removed']:
                f.write(f"- {item}\n")
        
        if 'iterable_item_added' in diff:
            f.write("--- List Items Added ---\n")
            for path, item in diff['iterable_item_added'].items():
                f.write(f"- {path}: {item}\n")
                
        if 'iterable_item_removed' in diff:
            f.write("--- List Items Removed ---\n")
            for path, item in diff['iterable_item_removed'].items():
                 f.write(f"- {path}: {item}\n")
