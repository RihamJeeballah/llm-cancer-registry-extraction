# LLM-based Cancer Registry Information Extraction

This repository accompanies our study on automated extraction of structured cancer registry variables from unstructured clinical text using open-source large language models (LLMs).

The work evaluates multiple prompt-based configurations and compares them against rule-based baselines across key registry fields.

---

## Overview

We investigate the effectiveness of LLMs for extracting structured information from pathology reports, including:

- **Grade**
- **Morphology**
- **Tumor staging (TNM: T, N, M)**
- **Laterality**
- **Treatment (exploratory)**

The repository provides the code used for:

- Prompt-based extraction experiments  
- Output normalization and mapping  
- Performance evaluation 
- Error analysis  
- Statistical validation (bootstrap confidence intervals and paired hypothesis testing)

---

## Repository Structure
experiments/
Field-specific extraction pipelines and Multi_field combined pipeline
(grade, morphology, TNM, laterality)

prompts/
Prompt templates used across different prompting strategies

evaluation/
Metric computation scripts (precision, recall, F1)
statistical_analysis/
Bootstrap resampling and paired t-test scripts
error_analysis/
Error categorization and qualitative analysis

similarity_score/
Utility scripts for similarity-based normalization

treatment/
Experimental scripts for treatment extraction

docs/
master excel sheet with all metrics results


---

## Methodological Summary

- Multiple LLM configurations were evaluated using prompt engineering strategies.
- Predictions were normalized into controlled label spaces.
- Performance was assessed using:
  - **Weighted F1 (primary metric)**
  - Macro F1, precision, and recall (secondary metrics)
- Statistical robustness was established via:
  - **Bootstrap resampling (95% confidence intervals)**
  - **Paired t-tests comparing best configurations against baseline systems**
- A structured error taxonomy was used to analyze model behavior across different failure modes.

---

## Reproducibility

This repository is designed to support reproducibility of the reported results by providing:

- Experiment scripts. 
- Prompt configurations used in evaluation  
- Evaluation and reporting utilities  
- Statistical analysis scripts used to compute confidence intervals and p-values  

---

## Data Availability

Due to privacy and ethical constraints, clinical data and raw reports are not publicly released.

This repository does **not** contain:

- Patient-level data  
- Raw clinical text  
- Identifiable information  

All scripts are provided to demonstrate the experimental and evaluation pipeline.

---

## Usage

The scripts can be adapted to new datasets by:

1. Providing input reports in a compatible format  
2. Running extraction scripts within `experiments/`  
3. Applying normalization and evaluation pipelines  

---

## Citation

If you use this code or build upon this work, please cite our paper.

---
