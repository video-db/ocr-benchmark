# Benchmarking Vision-Language Models on Optical Character Recognition in Dynamic Video Environments

## Installation 

1. Clone this repository:
```bash
git clone https://github.com/video-db/ocr-benchmark.git
cd ocr-benchmark 
```

2. Set up the environment:

   **Option A: Using `uv`**
   ```bash
   # Skip to step 3 if using uv
   ```

   **Option B: Using standard Python virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure API Keys:
   - Copy `.env.sample` to `.env`
   - Add your API keys in the `.env` file

## Usage

### Running Benchmarks

**Using uv:**
```bash
uv run run.py --model benchmark
```

**Using standard Python:**
```bash
python run.py --model benchmark
```

**Quick Test (1 video):**
```bash
uv run run.py --model benchmark --num_vids 1
```