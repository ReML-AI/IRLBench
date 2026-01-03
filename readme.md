## IRLBench: A Multi-modal, Culturally Grounded, Parallel Irish-English Benchmark for Open-Ended LLM Reasoning Evaluation
Khanh-Tung Tran, Duc-Hai Nguyen, Barry O'Sullivan, Hoang D. Nguyen

*Accepted to KDD 2026*

### Overview
> Recent advances in Large Language Models (LLMs) have demonstrated promising knowledge and reasoning abilities, yet their performance in multilingual and low-resource settings remains underexplored. Existing benchmarks often exhibit cultural bias, restrict evaluation to text-only, rely on multiple-choice formats, and, more importantly, are limited for extremely low-resource languages. To address these gaps, we introduce IRLBench, presented in parallel English and Irish, which is considered definitely endangered by UNESCO. Our benchmark consists of 12 representative subjects developed from the 2024 Irish Leaving Certificate exams, enabling fine-grained analysis of model capabilities across domains. By framing the task as long-form generation and leveraging the official marking scheme, it does not only support a comprehensive evaluation of correctness but also language fidelity. Our extensive experiments of leading closed-source and open-source LLMs reveal a persistent performance gap between English and Irish and critical insights, in which models produce valid Irish responses less than 80% of the time, and answer correctly 55.8% of the time compared to 76.2% in English for the best-performing model. We release IRLBench and an accompanying evaluation codebase to enable future research on robust, culturally aware multilingual AI development.

### Directory Structure

- `extract_problems_marking_scheme.py`: Pipeline to extract data from PDF images of the Irish Leaving Certificate examination.
- `generate_response.py`: Generates LLMs outputs for exam questions.
- `generate_judgement.py`: Evaluates model responses using judge models
- `get_results.py`: Functions for data loading and results processing
- `run_analysis.py`: Main script for running analysis and generating visualizations
- `visualize_results.py`: Functions for creating various visualization types

### Getting Started
1. Clone this repository
2. Installed required dependencies
3. Set up your API keys in a `.env` file

### Usage
Run `python extract_problems_marking_scheme.py` to perform the data colletion pipeline. Here, as we have collected and processed the dataset, we can use IRLBench directly:
```python
from datasets import load_dataset
ds = load_dataset("ReliableAI/IRLBench")
```

To generate responses from candidate model:
```bash
python generate_response.py --model MODEL_NAME
```

Using LLM-as-a-judge to generate judgement:
```bash
python generate_judgement.py --student_model MODEL_NAME --judge_model JUDGE_MODEL
```

To run a analysis of the raw results:

```bash
python run_analysis.py --model MODEL_NAME --judge_model JUDGE_MODEL --judgements_dir ./judgements --responses_dir ./responses
```

Where:
- `MODEL_NAME`: The model to be evaluated (e.g., "gemini-2.0-flash", "o4-mini")
- `JUDGE_MODEL`: The model used to judge answers (e.g., "gemini-2.5-flash")

Then, the raw results should be added to the function `prepare_visualization_data` in `visualize_results.py` before running visualization:
```bash
python visualize_results.py
```

### Citation
TBU
