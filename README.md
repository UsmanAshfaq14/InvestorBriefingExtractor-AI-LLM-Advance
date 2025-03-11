# InvestorBriefingExtractor-AI Case Study

## Overview

**InvestorBriefingExtractor-AI** is an intelligent system designed to generate nuanced summaries by extracting and highlighting implicit themes from investor briefings. Its primary goal is to inform strategic decision-making through insightful analysis while avoiding sensitive financial advice. The system accepts input data in CSV or JSON formats, rigorously validates the data against predefined rules, and then performs a series of calculations to extract key metrics such as average key metrics, keyword frequency, normalized scores, diversity scores, and composite thematic scores. Every processing step—from data validation to detailed calculations—is explained using clear, step-by-step methods and visual formulas (in LaTeX), making the process accessible even to non-technical users.

## Metadata

- **Project Name:** InvestorBriefingExtractor-AI  
- **Version:** 1.0.0  
- **Author:** Usman Ashfaq  
- **Keywords:** Investor Briefings, Thematic Extraction, Data Validation, Financial Analysis, Strategic Insights

## Features

- **Data Validation:**  
  The system checks the input for:
  - **Format:** Accepts data only in CSV or JSON formats enclosed in markdown code blocks.
  - **Required Fields:** Each investor briefing record must include:
    - `briefing_id`
    - `date` (in YYYY-MM-DD format)
    - `briefing_text`
    - `key_metrics` (if provided, must be a positive number)
  - **Data Integrity:** Verifies that dates are in the correct format and that numeric values are positive. When errors (e.g., missing fields or invalid values) are detected, the system outputs a comprehensive Data Validation Report.

- **Step-by-Step Calculations:**  
  For each investor briefing record, the system calculates:
  - **Average Key Metric:** Sums all key_metrics and divides by the number of records.
  - **Keyword Frequency:** Counts occurrences of expected keywords (such as "growth", "risk", "innovation", "market", etc.) in the briefing text.
  - **Normalized Keyword Score:** Divides the total keyword frequency by the total word count.
  - **Diversity Score:** Determines the percentage of unique expected keywords found.
  - **Composite Thematic Score:** Combines the normalized keyword score and diversity score using weighted factors.
  
  Every calculation is shown explicitly using LaTeX formulas with detailed intermediate steps.

- **Final Recommendation:**  
  Based on the calculated metrics, the system recommends whether the thematic intensity is high or moderate and provides actionable advice—either to "Focus on strategic growth and risk mitigation" or to "Review the investor briefing for additional insights."

- **User Interaction and Feedback:**  
  The system interacts with users by:
  - Greeting users and offering data input templates.
  - Returning detailed error messages and validation reports when issues are detected.
  - Requesting confirmation before proceeding with analysis.
  - Providing comprehensive final reports that include all the necessary calculations and actionable recommendations.

## System Prompt

The behavior of InvestorBriefingExtractor-AI is governed by the following system prompt:


"You are InvestorBriefingExtractor-AI, a system designed to generate nuanced summaries by extracting and highlighting implicit themes from investor briefings. Your primary goal is to inform strategic decision-making through insightful analysis while avoiding sensitive financial advice. Follow the instructions below precisely, using explicit IF/THEN/ELSE logic, detailed step-by-step calculations with formulas and examples, and clear validations. Do not assume any prior knowledge—explain every step in a manner that a 12-year-old can understand.

GREETING PROTOCOL  
If the user’s message contains a greeting, THEN respond with: 'Greetings! I am InvestorBriefingExtractor-AI, your assistant for extracting implicit themes from investor briefings.'  
ELSE IF the user greets without briefing data, THEN respond with: 'Would you like a template for submitting investor briefing data?'  
If the user agrees or asks for a template, THEN provide the following CSV and JSON templates.

DATA INPUT VALIDATION  
For each investor briefing record, validate that the required fields are present and that:
- `date` is in YYYY-MM-DD format.
- `key_metrics`, if provided, is a positive number.
Output a Data Validation Report in markdown format.  


## Variations and Test Flows

### Flow 1: Greeting and Template Request (CSV Data)
- **User Action:**  
  The user greets with "Hi".
- **Assistant Response:**  
  "Greetings! I am InvestorBriefingExtractor-AI, your assistant for extracting implicit themes from investor briefings. Would you like a template for submitting investor briefing data?"
- **User Action:**  
  The user agrees and requests the template.
- **Assistant Response:**  
  Provides CSV and JSON templates.
- **User Action:**  
  The user submits CSV data containing 6 investor briefing records.
- **Assistant Response:**  
  Validates the data, produces a Data Validation Report, and then processes the data to provide a detailed transformation report with calculations (average key metric, keyword frequency, normalized keyword score, diversity score, composite thematic score) and final recommendations.
- **Feedback:**  
  The analysis is rated positively.

### Flow 2: Direct Data Submission with Invalid Format (CSV Data)
- **User Action:**  
  The user declines the template and provides CSV data directly but with an invalid data type for `key_metrics`.
- **Assistant Response:**  
  Validates the data and returns a Data Validation Report similar to:
  ```markdown
  # Investor Briefing Data Validation Report
  ## Overview
  - Total Briefings Provided: 6

  ## Field Checks per Record
    - briefing_id: **present**
    - date: **valid**
    - briefing_text: **present**
    - key_metrics: **invalid**

  ## Summary
  ERROR: Invalid value for the field(s): key_metrics in record 4. Please correct and resubmit.

- **User Action:**  
  The user corrects the error and resubmits the data.
- **Assistant Response:**  
  Validates the corrected data and proceeds with the detailed analysis and final report.

### Flow 3: Error Handling with JSON Data (Missing Field)
- **User Action:**  
  The user provides JSON data containing 10 investor briefing records, but one record is missing a required field (e.g., `date`).
- **Assistant Response:**  
  Returns a detailed Data Validation Report in the format:

  # Investor Briefing Data Validation Report
  ## Overview
  - Total Briefings Provided: 10

  ## Field Checks per Record
  - **Record 1 (B311):** briefing_id: **present**, date: **valid**, briefing_text: **present**, key_metrics: **valid**
  - **Record 2 (B312):** briefing_id: **present**, date: **missing**, briefing_text: **present**, key_metrics: **valid**
  ...
  
  ## Summary
  ERROR: Missing required field(s): date in record 2. Please correct and resubmit.

- **User Action:**  
  The user then asks for the template, receives it, and provides corrected JSON data.
- **Assistant Response:**  
  Validates the corrected data and, after confirmation, performs a detailed analysis with step-by-step calculations for each of the 10 investor briefings, providing a final report with recommendations.

## Final Report Example (from Flow 4)

Below is an excerpt of the final detailed report generated for one of the flows (using JSON data with 10 records):


# Investor Briefing Summary
## Total Briefings Evaluated: 10

**Global Average Key Metric Calculation:**

- **Sum of key_metrics:**  
  $$96 + 94 + 92 + 95 + 93 + 91 + 90 + 92 + 94 + 93 = 930$$

- **Number of records with key_metrics:**  
  $$10$$

- **Average Key Metric:**  
  $$\frac{930}{10} = 93.00$$

---

### Detailed Analysis per Briefing:

#### Briefing B311
**Input Data:**
- **Date:** 2023-07-11  
- **Briefing Text Snippet:** "The company shows significant growth driven by innovative solutions."  
- **Key Metrics:** 96

**Detailed Calculations:**

1. **Average Key Metric Calculation:**  
   - **Formula:**  
     $$\text{Average Key Metric} = \frac{930}{10}$$  
   - **Calculation:**  
     $$\frac{930}{10} = 93.00$$

2. **Keyword Frequency Calculation:**  
   - **Expected Keywords:** "growth", "risk", "innovation", "market", "confidence", "investment", "strategic", "opportunity", "challenges", "expansion"  
   - **Occurrences in Text:**  
     - "growth": 1  
   - **Total Keyword Frequency:**  
     $$1$$

3. **Normalized Keyword Score Calculation:**  
   - **Formula:**  
     $$\text{Normalized Keyword Score} = \frac{1}{9}$$  
   - **Calculation:**  
     $$\frac{1}{9} \approx 0.11$$

4. **Diversity Score Calculation:**  
   - **Formula:**  
     $$\text{Diversity Score} = \frac{1}{10} \times 100$$  
   - **Calculation:**  
     $$\frac{1}{10} \times 100 = 10.00\%$$

5. **Composite Thematic Score Calculation:**  
   - **Formula:**  
     $$\text{Composite Thematic Score} = (0.11 \times 50) + (10.00 \times 0.5)$$  
   - **Calculation:**  
     $$0.11 \times 50 = 5.50$$  
     $$10.00 \times 0.5 = 5.00$$  
     $$5.50 + 5.00 = 10.50$$

**Final Recommendation for B311:**  
- **Composite Thematic Score:** 10.50 (below 30.00)  
- **Normalized Keyword Score:** 0.11  
- **Thematic Intensity:** Moderate  
- **Recommended Action:** Review the investor briefing for additional insights

*(Detailed analyses for Briefings B312 to B320 follow a similar structure.)*


## Conclusion

InvestorBriefingExtractor-AI is a robust and user-friendly tool that automates the extraction of thematic insights from investor briefings. By enforcing strict data validation rules and providing detailed, step-by-step calculations with clear LaTeX formulas, the system ensures both accuracy and clarity in its recommendations. The various test flows—ranging from greeting and template requests to error handling with invalid and missing data—demonstrate the system's ability to handle different data formats and error scenarios while continuously refining its outputs based on user feedback. This case study highlights the effectiveness of automated thematic extraction in supporting investor analysis and strategic decision-making.
