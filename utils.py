import os
from typing import List
import logging
import json

def create_directories(args) -> List[str]:
    """
    Create directories for storing model results based on the selected models.
    
    Args:
        args: Arguments containing model selection and base directory paths
    
    Returns:
        List[str]: List of full directory paths that were created or processed
    """
    # Define model groups
    model_groups = {
        'openai': {
            'base_dir': args.openai_results_dir,
            'models': ['gpt-4o', 'gpt-4o-mini', 'chatgpt-4o-latest', 'gpt-4-turbo']
        },
        'anthropic': {
            'base_dir': args.anthropic_results_dir,
            'models': ['claude-3-5-sonnet-latest']
        },
        'google': {
            'base_dir': args.google_results_dir,
            'models': ['gemini-1.5-flash', 'gemini-1.5-flash-8b', "gemini-1.5-pro"]
        },
    }
    
    
    model_groups.update({
        'ocr': {
            'base_dir': args.ocr_results_dir,
            'models': ['rapidocr', 'easyocr']
        }
    })
    
    processed_paths = []
    
    def create_model_dir(base_dir: str, model: str) -> None:
        """Helper function to create directory for a single model"""
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
            print(f"Created base directory: {base_dir}")
            
        model_dir = os.path.join(base_dir, model)
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
            print(f"Created model directory: {model_dir}")
        else:
            print(f"Directory already exists: {model_dir}")
        processed_paths.append(model_dir)
    
    def process_model(model_name: str) -> bool:
        """Process a single model or group name, return True if found"""
        # Check if it's "all"
        if model_name.lower() == "all":
            for group in model_groups.values():
                for model in group['models']:
                    create_model_dir(group['base_dir'], model)
            return True
        
         # Check if it's "benchmark"
        if model_name.lower() == "benchmark":
            for group in model_groups.values():
                for model in group['models']:
                    if model in ["gpt-4o","gemini-1.5-pro", "claude-3-5-sonnet-latest", "easyocr", "rapidocr"]:
                        create_model_dir(group['base_dir'], model)
            return True
            

        # Check if it's a group name
        if model_name.lower() in model_groups:
            group_info = model_groups[model_name.lower()]
            for model in group_info['models']:
                create_model_dir(group_info['base_dir'], model)
            return True
            
        # Check if it's a specific model name
        for group_info in model_groups.values():
            if model_name.lower() in [m.lower() for m in group_info['models']]:
                create_model_dir(group_info['base_dir'], model_name)
                return True
                
        return False

    # Handle single model or list of models
    selected_models = args.model if isinstance(args.model, list) else [args.model]
    
    for model in selected_models:
        if not process_model(model):
            print(f"Warning: No matching model or group found for '{model}'")
            continue
    
    if not processed_paths:
        print("No valid models were processed")
        import sys
        sys.exit(1)
    
    return processed_paths

def setup_logging(path: str, current_run: str) -> logging.Logger:
    """
    Set up logging for each model directory with separate loggers.
    """
    model_name = os.path.basename(path)
    current_run_dir = os.path.join(path, current_run)
    os.makedirs(current_run_dir, exist_ok=True)
    
    logger = logging.getLogger(model_name)
    logger.setLevel(logging.INFO)
    
    if logger.hasHandlers():
        for handler in logger.handlers[:]:  # Copy to avoid modifying during iteration
            handler.close()  # Close handlers before clearing
            logger.removeHandler(handler)
            
    logfile = os.path.join(current_run_dir, "logfile.log")
    fh = logging.FileHandler(logfile, "w")
    ch = logging.StreamHandler()
    
    formatter = logging.Formatter("%(asctime)s %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger, current_run_dir
        
        
        
def save_summary(current_run):
    os.makedirs("evaluation_summary",exist_ok=True)
    summary = []
    
    for model_result in os.listdir("ocr_results"):
        for model in os.listdir(os.path.join("ocr_results",model_result)):
            cer = 0
            wer = 0
            acc = 0
            order_agnostic_acc = 0
            total_frames = 0
            total_vids = 0
        
            for run in os.listdir(os.path.join("ocr_results",model_result, model)):
                
                if current_run in run:
                    for evals in os.listdir(os.path.join("ocr_results",model_result, model,run,"evaluations")):
                        total_vids+=1
                        
                        json_path = os.path.join("ocr_results",model_result, model,run,"evaluations",evals)
                        
                        with open(json_path,"r") as f:
                            json_data = json.load(f)
                            
                        for entry in json_data:
                            cer+=entry["cer"]
                            wer+=entry["wer"]
                            acc+=entry["accuracy"]
                            order_agnostic_acc+=entry["order_agnostic_accuray"]
                            total_frames+=1
                            
            if total_vids!=0:
                summary.append(
                    {
                        "model" : model,
                        "total_vids" : total_vids,
                        "total_frames" : total_frames,
                        "avg_cer" : cer/total_frames,
                        "avg_wer" : wer/total_frames,
                        "avg_acc" : acc/total_frames,
                        "avg_order_agnostic_acc" : order_agnostic_acc/total_frames                    
                        
                    }
                )
            
    with open(os.path.join("evaluation_summary",f"{current_run}.json"), "w") as f:
        
        json.dump(summary,f)
            
        
                            
                                
                            
        
    