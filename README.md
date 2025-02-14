# Benchmarking Vision-Language Models on Optical Character Recognition in Dynamic Video Environments

This repository contains a benchmarking framework for evaluating OCR (Optical Character Recognition) performance using multiple vision-language models (VLMs) and OCR engines. The framework is designed to work with [VideoDB public collections](https://docs.videodb.io/public-collections-102) and supports several models including OpenAI, Google Gemini, Anthropic Claude, Moondream, EasyOCR, and RapidOCR.

For detailed methodology and analysis, please refer to our paper: [Benchmarking Vision-Language Models on Optical Character Recognition in Dynamic Video Environments](https://arxiv.org/abs/2502.06445)

## Table of Contents
- [Overview](#overview)
- [Benchmark Results](#benchmark-results)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Running OCR Benchmark](#running-ocr-benchmark)
- [Dataset](#dataset)
- [Results](#results)
- [Preparing Your Own Ground Truth](#preparing-your-own-ground-truth)

## Overview

This project benchmarks OCR performance across different models by:
- Extracting scenes from videos using [VideoDB](https://videodb.io).
- Running OCR on the extracted frames using various models.
- Comparing OCR outputs against ground truth to compute error metrics such as Character Error Rate (CER) and Word Error Rate (WER).

The modular design allows you to easily extend the framework by adding new models or other vision tasks.

### Benchmark Results

Our comprehensive evaluation shows that Vision-Language Models (VLMs) significantly outperform traditional OCR systems:

| Model | Character Error Rate (CER) | Word Error Rate (WER) | Average Accuracy (%) |
|-------|---------------------------|----------------------|-------------------|
| RapidOCR | 0.4302 | 0.7620 | 56.98 (↓19.24) |
| EasyOCR | 0.5070 | 0.8262 | 49.30 (↓26.92) |
| Claude-3.5 Sonnet | 0.3229 | 0.4663 | 67.71 (↓8.51) |
| Gemini-1.5 Pro | 0.2387 | 0.2385 | 76.13 (↓0.09) |
| GPT-4o | 0.2378 | 0.5117 | 76.22 |


## Installation 

1. Clone this repository:
    ```bash
    git clone https://github.com/video-db/ocr-benchmark.git
    cd ocr-benchmark 
    ```

2. Set up the environment:

   **Option A: Using `uv`**
   ```bash
   # Skip this step if you are using `uv`
   ```

   **Option B: Using standard Python virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
  
## Configuration

- **Environment Variables:**  
  Create a `.env` file in the root directory with the following variables (update with your API keys):

  ```env
  VIDEO_DB_API_KEY=sk-****-****
  GEMINI_API_KEY=your_gemini_api_key
  OPENAI_API_KEY=your_openai_api_key
  ANTHROPIC_API_KEY=your_anthropic_api_key
  PREP_GROUND_TRUTH_COLLECTION_ID=your_collection_id  # (Optional) For preparing ground truth
  ```

## Usage

### Running OCR Benchmark

**Quick Test (1 video):**
```bash
uv run run.py --model benchmark --num_vids 1
```

**Full Run (using uv):**
```bash
uv run run.py --model benchmark
```

**Full Run (using standard Python):**
```bash
python run.py --model benchmark
```

## Dataset

The dataset is based on [VideoDB's public collection](https://docs.videodb.io/public-collections-102). This public collection provides open access to a curated set of videos along with their pre-defined scene indexes. Anyone with the VideoDB ID can access these videos and read their corresponding indexes. This feature facilitates easy benchmarking and reproducibility.

Here are the videos of VideoDB's OCR Benchmark Public Collection (`c-c0a2c223-e377-4625-94bf-910501c2a31c`)

| **Video Name**                 | **Category**                        | **Video ID**                                    |
|--------------------------------|-------------------------------------|-------------------------------------------------|
| Stock Market Ticker 01         | Finance/Business/News Text          | m-z-0194c27c-f30c-7803-b2ca-8f1026c940a2         |
| CNBC 01                        | Finance/Business/News Text          | m-z-0194c27d-10a6-7531-9aaf-d7940a9469b1         |
| CNBC 04                        | Finance/Business/News Text          | m-z-0194c27e-19c0-7270-9b2e-d467ff30fd1a         |
| New Paper Reading 04           | Finance/Business/News Text          | m-z-0194c27d-50bc-7c22-9d73-3756717196d5         |
| Stock Market Ticker 02         | Finance/Business/News Text          | m-z-0194c27e-fe96-7403-a0d8-17a033e5f595         |
| Legal Document 01              | Legal/Educational Text              | m-z-0194c270-bbfb-7dd2-aaec-62d909b97b32         |
| Legal Document 03              | Legal/Educational Text              | m-z-0194c27d-2e68-7e63-b44e-5abbe36938df         |
| Legal Document 05              | Legal/Educational Text              | m-z-0194c27e-5dcf-73b3-a129-e9217d8e611f         |
| White Board Music Theory 01    | Legal/Educational Text              | m-z-0194c27d-71a3-72c2-9710-773f6f6b80b5         |
| White Board Music Theory 02    | Legal/Educational Text              | m-z-0194c27f-60d8-74e2-b777-bfed7d9b49d4         |
| Calculus Limits 01             | Legal/Educational Text              | m-z-0194c280-0778-7b52-8268-c6f1d00dbd52         |
| React 01                       | Software/Web Development/UI/UX Text | m-z-0194c27c-d107-7030-b990-0b5cc62f514a         |
| React 03                       | Software/Web Development/UI/UX Text | m-z-0194c27c-894f-7e11-beac-6da09861f796         |
| React 05                       | Software/Web Development/UI/UX Text | m-z-0194c272-dd5c-7a62-8d86-a47e3c4e4670         |
| CSS 02                         | Software/Web Development/UI/UX Text | m-z-0194c27c-aebe-75d0-812f-06fbeb60b7d6         |
| React Animation 01             | Software/Web Development/UI/UX Text | m-z-0194c27e-99ce-7fc0-867f-9bc8358d3388         |
| React Animation 02             | Software/Web Development/UI/UX Text | m-z-0194c27d-b22a-7982-a796-e332a82d5596         |
| CSS 01                         | Software/Web Development/UI/UX Text | m-z-0194c27f-a202-7f00-80a9-3bb8a3bf257d         |
| Handwriting Analysis 01        | Handwritten Text                    | m-z-0194c27f-836c-72f2-8c43-2eeedd6dbc2b         |
| Handwriting Analysis 02        | Handwritten Text                    | m-z-0194c27d-98b2-75c0-afff-77c8b24515bc         |
| Cursive Writing Whiteboard     | Handwritten Text                    | m-z-0194c27e-408d-73b1-b550-5bf76fb0339d         |
| Cursive Handwriting 01         | Handwritten Text                    | m-z-0194c27f-e828-7f43-be2e-7fa19bc39dd4         |
| Film Analysis 02               | Miscellaneous/Other Text            | m-z-0194c27d-d8d7-73b3-b136-1f4af218cb12         |
| Billboard Pederstian           | Miscellaneous/Other Text            | m-z-0194c27d-f7f8-7d03-b053-7f0e75498476         |
| Walk Sign                      | Miscellaneous/Other Text            | m-z-0194c27f-2095-76a3-bc26-96f1167e2526         |



## Results

The benchmarking framework organizes outputs and logs in a structured directory hierarchy to help you review and interpret the performance of each model. Below is a sample directory tree for an OpenAI run (e.g., using GPT-4O) that illustrates how the results are organized:

```
gpt_results/
└── gpt-4o/
    └── ocr_2025-02-06_16-32-48/
        ├── evaluations/
        │   └── m-z-0194c270-bbfb-7dd2-aaec-62d909b97b32.json
        ├── logfile.log
        └── m-z-0194c270-bbfb-7dd2-aaec-62d909b97b32_output.json

evaluation_summary/
└── ocr_2025-02-06_16-32-48.json
```

### Key Components

- **Model-Specific Folders:**  
  In the above example, results for the OpenAI model (e.g., GPT-4O) are stored under `gpt_results/gpt-4o/`. Each run is organized into a timestamped folder (e.g., `ocr_2025-02-06_16-32-48`).

- **Output Files:**  
  Within the run folder, the output JSON file (e.g., `m-z-0194c270-bbfb-7dd2-aaec-62d909b97b32_output.json`) contains the OCR predictions for a given video. This file includes details such as:
  - The video ID.
  - Scene start and end times.
  - Processing time.
  - Image URLs.
  - The OCR text output generated by the model.

- **Evaluation Files:**  
  In the `evaluations` subfolder, JSON files (e.g., `m-z-0194c270-bbfb-7dd2-aaec-62d909b97b32.json`) contain quantitative metrics calculated by comparing the model's OCR output against the ground truth. These metrics include:
  - Character Error Rate (CER)
  - Word Error Rate (WER)
  - Accuracy
  - Order-Agnostic Accuracy

- **Log Files:**  
  The `logfile.log` file records detailed processing information, including timestamps and status messages, which are useful for debugging and verifying that each run executed as expected.

- **Evaluation Summary:**  
  Aggregated summary files in the `evaluation_summary` folder provide an overview of performance metrics across different runs and models, facilitating high-level comparisons of model performance.

### Interpreting the Results

- **Output Files (Predictions):**  
  The JSON output files present the raw OCR text generated by the model for each scene. By comparing this output with the ground truth (referenced in the evaluation files), you can visually assess the accuracy of the OCR process.

- **Evaluation Metrics:**  
  The evaluation files quantify performance using:
  - **CER (Character Error Rate):** Lower CER indicates a higher precision at the character level.
  - **WER (Word Error Rate):** Lower WER indicates fewer mistakes in recognizing words.
  - **Accuracy:** A higher percentage represents better overall text recognition.
  - **Order-Agnostic Accuracy:** Useful for understanding text recognition performance independent of word order.

- **Log Files:**  
  The logs provide a narrative of the processing events, including any errors or warnings that occurred during the run.

This structure allows you to systematically access and evaluate the OCR outputs and associated metrics for models, ensuring that you can effectively compare performance and diagnose any issues.

## Preparing Your Own Ground Truth

```bash
uv run ground_truth_preparation/create_videodb_collection.py
```
This script will prompt for collection details and allow you to upload videos either from files or by specifying a JSON file containing video URLs. The collection will be created as a [VideoDB public collection](https://docs.videodb.io/public-collections-102) for easy sharing and reproducibility.

```bash
uv run ground_truth_preparation/prepare_ground_truth.py
```
This script extracts frames from videos, performs OCR, and stores the ground truth in the ocr_ground_truths directory to get you started, you can then manually inspect and refine the data.

<!-- TODO: Add Customization

Changing Collection
Changing Prompt

-->
