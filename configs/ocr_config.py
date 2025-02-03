"""
Config for OCR Benchmarking

"""

COLLECTION_ID = "c-c0a2c223-e377-4625-94bf-910501c2a31c" # VideoDB's OCR Benchmark Dataset Public Collection

# Data
VIDEO_IDS = {
    "legal_document_01": "m-z-0194c270-bbfb-7dd2-aaec-62d909b97b32",
    "react_05": "m-z-0194c272-dd5c-7a62-8d86-a47e3c4e4670",
    "react_03": "m-z-0194c27c-894f-7e11-beac-6da09861f796",
    "css_02": "m-z-0194c27c-aebe-75d0-812f-06fbeb60b7d6",
    "react_01": "m-z-0194c27c-d107-7030-b990-0b5cc62f514a",
    "stock_market_ticker_01": "m-z-0194c27c-f30c-7803-b2ca-8f1026c940a2",
    "CNBC_01": "m-z-0194c27d-10a6-7531-9aaf-d7940a9469b1",
    "legal_document_03": "m-z-0194c27d-2e68-7e63-b44e-5abbe36938df",
    "new_paper_reading_04": "m-z-0194c27d-50bc-7c22-9d73-3756717196d5",
    "white_board_music_theory_01": "m-z-0194c27d-71a3-72c2-9710-773f6f6b80b5",
    "handwriting_analysis_02": "m-z-0194c27d-98b2-75c0-afff-77c8b24515bc",
    "react_animation_02": "m-z-0194c27d-b22a-7982-a796-e332a82d5596",
    "film_analysis_02": "m-z-0194c27d-d8d7-73b3-b136-1f4af218cb12",
    "billboard_pederstian": "m-z-0194c27d-f7f8-7d03-b053-7f0e75498476",
    "CNBC_04": "m-z-0194c27e-19c0-7270-9b2e-d467ff30fd1a",
    "cursive_writing_whiteboard": "m-z-0194c27e-408d-73b1-b550-5bf76fb0339d",
    "legal_document_05": "m-z-0194c27e-5dcf-73b3-a129-e9217d8e611f",
    "react_animation_01": "m-z-0194c27e-99ce-7fc0-867f-9bc8358d3388",
    "stock_market_ticker_02": "m-z-0194c27e-fe96-7403-a0d8-17a033e5f595",
    "walk_sign": "m-z-0194c27f-2095-76a3-bc26-96f1167e2526",
    "white_board_music_theory_02": "m-z-0194c27f-60d8-74e2-b777-bfed7d9b49d4",
    "handwriting_analysis_01": "m-z-0194c27f-836c-72f2-8c43-2eeedd6dbc2b",
    "css_01": "m-z-0194c27f-a202-7f00-80a9-3bb8a3bf257d",
    "cursive_handwriting_01": "m-z-0194c27f-e828-7f43-be2e-7fa19bc39dd4",
    "calculus_limits_01": "m-z-0194c280-0778-7b52-8268-c6f1d00dbd52",
}

# Save Directories
OPENAI_RESULTS_DIR = "ocr_results/gpt_results"
ANTHROPIC_RESULTS_DIR = "ocr_results/claude_results"
GOOGLE_RESULTS_DIR = "ocr_results/gemini_results"
MOONDREAM_RESULTS_DIR = "results/moondream_results"
OCR_RESULTS_DIR = "ocr_results/CV_results"

OPENAI_EVALUATION_DIR = "ocr_evaluation/gpt_evaluation"
ANTHROPIC_EVALUATION_DIR = "ocr_evaluation/claude_evaluation"
GOOGLE_EVALUATION_DIR = "ocr_evaluation/gemini_evaluation"
MOONDREAM_EVALUATION_DIR = "ocr_evaluation/moondream_evaluation"
OCR_EVALUATION_DIR = "ocr_evaluation/CV_evaluation"

# Path to the ground truth text directory
OCR_GROUND_TRUTH_DIR = "ocr_ground_truths"
