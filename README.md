# Evaluating LLM Judgment on Latvian and Lithuanian Short Answer Matching

This repository contains code, data, and evaluation tools developed for the paper:

> **The Veln(ia)s is in the Details: Evaluating LLM Judgment on Latvian and Lithuanian Short Answer Matching**
> *Accepted for NB-REAL 2025 Workshop*  

## Overview

This work introduces and evaluates a framework for **Short Answer Matching (SAM)** in **Latvian** and **Lithuanian**, focusing on how **Large Language Models (LLMs)** judge the correctness of student answers compared to reference answers.  
Our goal is to assess **LLM-based grading** in low-resource Baltic languages, addressing the linguistic and semantic challenges of SAM in educational settings.

## Repository Contents

- `data_genereation/`:  contains code for applying different alteration rules on KID datasets; contains datasets as well.   

- `evaluation/`:  contains code to run evaluation of the model of generated data.
  
- `annotation_guidelines/`: contains guidelines provided to the annotators to check the quality of the applied alteration rules.

## Dataset Description

- **Languages:** Latvian, Lithuanian.  
- **Domains:** Wikipedia-based questions and answers.  


## Evaluation Setup

LLMs are evaluated for their ability to correctly classify whether a **student answer matches the reference answer**.  
The pipeline includes:
1. Prompting LLMs with question-answer pairs.
2. Collecting LLM judgments (match/mismatch).
3. Comparing LLM outputs to human annotations.

### LLMs evaluated:

- GPT-4 / GPT-4o
- Qwen2.5 (7B, 72B)
- LLaMa3 (8B, 70B)
- Mistral (7B, 12B)
- EuroLLM 9b



If you use this dataset, code, or findings, please cite:

```
@misc{kostiuk2025velniasdetailsevaluatingllm,
      title={The Veln(ia)s is in the Details: Evaluating LLM Judgment on Latvian and Lithuanian Short Answer Matching}, 
      author={Yevhen Kostiuk and Oxana Vitman and Łukasz Gagała and Artur Kiulian},
      year={2025},
      eprint={2501.09164},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2501.09164}, 
}
```
