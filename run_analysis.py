#!/usr/bin/env python3

import os
import argparse
from get_results import (
    get_results_from_judgements, 
    calculate_language_fidelity, 
    name_mappings
)

def main() -> None:
    """Main function to run analysis and generate visualizations."""
    parser = argparse.ArgumentParser(description="Run analysis on Leaving Certificate results.")
    parser.add_argument("--model", default="gemini-2.0-flash", help="Model to analyze")
    parser.add_argument("--judge-model", default="gemini-2.5-flash-preview-04-17", help="Judge model")
    parser.add_argument("--judgements-dir", default="judgements", help="Directory containing judgements")
    parser.add_argument("--responses-dir", default="responses", help="Directory containing responses")
    parser.add_argument("--output-dir", default="output", help="Directory to save outputs")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    print(f"Analyzing model: {args.model}")

    # Get list of subjects
    subjects = list(name_mappings.keys())

    # Get results from judgements
    print(f"Getting results from judgements for {len(subjects)} subjects...")
    results, lang_fidelity, confidences, correct_irish, incorrect_irish, both = get_results_from_judgements(
        subjects=subjects,
        model=args.model,
        judge_model=args.judge_model,
        judgements_dir=args.judgements_dir
    )
    
    # Calculate language fidelity
    print("Calculating language fidelity...")
    language_fidelity = calculate_language_fidelity(
        subjects=subjects,
        models=[args.model],
        responses_dir=args.responses_dir
    )
    
    # Display summary
    print("\n--- Summary ---")
    print(f"Model: {args.model}")
    
    english_subjects = [s for s in subjects if s.endswith('EV')]
    irish_subjects = [s for s in subjects if s.endswith('IV')]
    
    english_score = 0
    english_count = 0
    irish_score = 0
    irish_count = 0
    
    for subject in english_subjects:
        if subject in results and len(results[subject]) > 0:
            score = sum(results[subject]) / len(results[subject]) * 100
            english_score += score
            english_count += 1
            print(f"{name_mappings[subject]}: {score:.2f}%")
    
    print("\n")
    
    for subject in irish_subjects:
        if subject in results and len(results[subject]) > 0:
            score = sum(results[subject]) / len(results[subject]) * 100
            irish_score += score
            irish_count += 1
            print(f"{name_mappings[subject]}: {score:.2f}%")
    
    print("\nAverage scores:")
    print(f"English: {english_score/english_count if english_count else 0:.2f}%")
    print(f"Irish: {irish_score/irish_count if irish_count else 0:.2f}%")

if __name__ == "__main__":
    main()
