import os
from .schemas import AccountMemo, AgentSpec
from .llm_service import MockLLMService
from .storage import save_version, generate_changelog, load_version

class PipelineProcessor:
    def __init__(self, output_dir: str = "output"):
         self.llm = MockLLMService()
         self.output_dir = output_dir
         
    def process_demo(self, file_path: str, account_id: str):
        """Stage 1: Process Demo Call into v1"""
        print(f"[{account_id}] Processing Demo (v1)...")
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            
        # 1. Extract v1 via LLM
        v1_memo, v1_spec = self.llm.extract_demo_v1(text, account_id)
        
        # 2. Save v1
        save_version(account_id, "v1", v1_memo, v1_spec, self.output_dir)
        print(f"[{account_id}] Saved v1 successfully.")
        
    def process_onboarding(self, file_path: str, account_id: str):
         """Stage 2: Process Onboarding Call into v2 and generate Diff"""
         print(f"[{account_id}] Processing Onboarding (v2)...")
         with open(file_path, "r", encoding="utf-8") as f:
             text = f.read()
             
         # 1. Load v1
         try:
             v1_memo, v1_spec = load_version(account_id, "v1", self.output_dir)
         except FileNotFoundError:
             print(f"[{account_id}] Error: v1 not found. Must run demo first.")
             return
             
         # 2. Extract v2 via LLM based on v1 base
         v2_memo, v2_spec = self.llm.extract_onboarding_v2(text, v1_memo, v1_spec)
         
         # 3. Save v2
         save_version(account_id, "v2", v2_memo, v2_spec, self.output_dir)
         
         # 4. Generate Diff
         generate_changelog(account_id, v1_memo, v2_memo, self.output_dir)
         print(f"[{account_id}] Saved v2 and changelog successfully.")
