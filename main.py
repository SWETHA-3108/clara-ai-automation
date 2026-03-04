import os
import glob
from src.processor import PipelineProcessor

def main():
    print("=== Zero-Cost AI Voice Agent Automation ===")
    
    # 1. Setup mock data directories
    input_dir = "data"
    output_dir = "output"
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    processor = PipelineProcessor(output_dir=output_dir)
    
    # 2. Discover files
    print("\n--- STAGE 1: Processing Demo Calls ---")
    # Looking for demo1.txt, demo2.txt etc.
    demo_files = glob.glob(os.path.join(input_dir, "demo*.txt"))
    for file_path in sorted(demo_files):
        filename = os.path.basename(file_path)
        # Extract ID (e.g., demo1.txt -> 1)
        account_id = filename.replace("demo", "").replace(".txt", "")
        processor.process_demo(file_path, f"account_{account_id}")
        
    print("\n--- STAGE 2: Processing Onboarding Calls ---")
    # Looking for onboarding1.txt, onboarding2.txt etc.
    onboarding_files = glob.glob(os.path.join(input_dir, "onboarding*.txt"))
    for file_path in sorted(onboarding_files):
        filename = os.path.basename(file_path)
        # Extract ID (e.g., onboarding1.txt -> 1)
        account_id = filename.replace("onboarding", "").replace(".txt", "")
        processor.process_onboarding(file_path, f"account_{account_id}")
        
    print("\n=== Automation Complete ===")
    print("Check the 'output' directory for the generated JSON schemas and changelogs.")

if __name__ == "__main__":
    main()
