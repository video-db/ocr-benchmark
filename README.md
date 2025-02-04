# Benchmarking Vision-Language Models on Optical Character Recognition in Dynamic Video Environments

## Installation 
1. Clone this repository:
```bash
git clone https://github.com/yourusername/vision_benchmark.git
cd vision_benchmark
```
2. Set up a virtual environment:
```python
python -m venv vision_benchmark_env
```
```bash
source vision_benchmark_env/bin/activate  # On Windows, use `vision_benchmark_env\Scripts\activate`
```
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Main Script  

The main script to run the project is `run.py`. You can execute the script with various arguments to customize the behavior of the program.  

### Command-Line Arguments  

Here are the arguments you can use when running the script:  

- **`--task`**: Specifies the task to be performed.  
  - Default: `"scene_description"`  
  - Choices: `"scene_description"`, `"ocr"`  

- **`--model`**: Selects the model(s) to use.  
  - Default: `"gpt-4o"`  
  - Choices:  
    - General Models: `"all"`, `"openai"`, `"google"`, `"anthropic"`  
    - Scene Description Models: `"gpt-4o"`, `"gpt-4o-mini"`, `"chatgpt-4o-latest"`, `"gpt-4-turbo"`, `"gemini-1.5-flash"`, `"gemini-1.5-flash-8b"`, `"claude-3-5-sonnet-latest"`  
    - CV Models: `"easyocr"`, `"rapidocr"`  

- **`--prompt_name`**: Specifies the type of prompt to use.  
  - Default: `"landscape"`  
  - Choices: `"landscape"`, `"action"`, `"emotion"`, `"medical"`, `"ocr"`, `"describe"`  

- **`--num_vids`**: Specifies the number of videos to process.  
  - Default: `100`  

- **`--num_frames`**: Specifies the number of frames to process per video.  
  - Default: `2`  

**Note**: When the `--task` is set to `"ocr"`, the number of frames (`--num_frames`) will always be **1**, regardless of the value provided.  

---

## Configuration  

To get started, you need to configure the necessary API keys and paths.  

1. **API Keys**:  
   - Navigate to the `configs` folder.  
   - Open `api_keys.py` and add the required API keys for the models you intend to use.  

2. **Results Directory**:  
   - For each task (`scene_description` or `ocr`), you may need to change the paths for storing results.  
   - Locate the configuration files in the `configs` folder for the respective tasks to update the results directory paths.  

---

## Ground Truth  

- The ground truth data for OCR tasks is present in the `ocr_ground_truth` directory.   

---

## Running the Script  

To run the script, use the following command format:  

```bash
python run.py --task <task_name> --model <model_name> --num_vids <number_of_videos> --num_frames <number_of_frames> --prompt_name <prompt_type>
