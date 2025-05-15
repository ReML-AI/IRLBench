import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, List, Tuple, Optional, Any

# Import the data processing functions
from get_results import prepare_visualization_data, name_mappings

def plot_language_comparison(data: Dict[str, Any]) -> None:
    """
    Plot comparison of model performance between English and Irish.
    
    Args:
        data: Dictionary containing results data
    """
    # Set a more appealing style
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Extract data
    models = data['models']
    results = data['results']
    
    # Define a custom color palette
    colors = ['#3498db', '#e74c3c']  # Blue and red tones
    
    # Bar settings
    x = np.arange(len(models))
    width = 0.35
    
    # Plot with improved styling
    fig, ax = plt.subplots(figsize=(10, 7))
    bars1 = ax.bar(x - width/2, results['English'], width, label='English', 
                   color=colors[0], edgecolor='white', linewidth=1)
    bars2 = ax.bar(x + width/2, results['Irish'], width, label='Irish', 
                   color=colors[1], edgecolor='white', linewidth=1)
    
    # Improved styling for labels and title
    ax.set_ylabel('Score', fontsize=14, fontweight='bold')
    ax.set_title('Scores by Model and Language', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=45, ha='right', fontsize=14)
    
    # Add a subtle horizontal grid and remove spines
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    # Enhanced legend
    ax.legend(fontsize=15, frameon=True, facecolor='white', framealpha=0.9)
    
    # Improved value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}', 
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('output/language_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_results_vs_confidence(data: Dict[str, Any]) -> None:
    """
    Plot model performance: results vs. confidence with arrows.
    
    Args:
        data: Dictionary containing results and confidence data
    """
    # Extract data
    models = data['models']
    results = data['results']
    confidences = data['confidences']
    
    # Extract results and confidence scores for each language
    english_results = results['English']
    irish_results = results['Irish']
    english_confidences = confidences['English']
    irish_confidences = confidences['Irish']

    plt.figure(figsize=(10, 8))
    
    # Define markers and colors for better visibility
    markers = ['o', 's', 'D', '^', 'v', 'P']
    colors = plt.cm.tab10(np.linspace(0, 1, len(models)))
    
    # Plot each model
    for i, model in enumerate(models):
        # Plot both points for this model
        plt.scatter(english_results[i], english_confidences[i], marker=markers[i], color=colors[i], s=150, 
                    label=model, edgecolors='black')
        plt.scatter(irish_results[i], irish_confidences[i], marker=markers[i], color=colors[i], s=150,
                    edgecolors='black')
        
        # Plot an arrow between the two points pointing from English to Irish
        plt.annotate('', xy=(irish_results[i], irish_confidences[i]), xytext=(english_results[i], english_confidences[i]),
                     arrowprops=dict(arrowstyle='->,head_length=0.4,head_width=0.3', color=colors[i], lw=1.2, linestyle='dashed', shrinkA=8, shrinkB=8),
                     fontsize=10, color=colors[i])
    
    # Add annotations for languages
    for i, model in enumerate(models):
        if model in ['aya-vision-8b']:
            plt.annotate('English', (english_results[i], english_confidences[i]), 
                        xytext=(-42, 8), textcoords='offset points', fontsize=12)
        else:
            plt.annotate('English', (english_results[i], english_confidences[i]), 
                        xytext=(-17, 12), textcoords='offset points', fontsize=12)
        if model in ['gpt-4.1']:
            plt.annotate('Irish', (irish_results[i], irish_confidences[i]), 
                        xytext=(-10.5, -18), textcoords='offset points', fontsize=12)
        elif model in ['Llama-4-Scout-17B-Instruct']:
            plt.annotate('Irish', (irish_results[i], irish_confidences[i]), 
                        xytext=(4.5, -13), textcoords='offset points', fontsize=12)
        else:
            plt.annotate('Irish', (irish_results[i], irish_confidences[i]), 
                        xytext=(-10.5, 12), textcoords='offset points', fontsize=12)
    
    plt.xlabel('Result Score', fontsize=14, fontweight='bold')
    plt.ylabel('Confidence Score', fontsize=14, fontweight='bold')
    plt.title('Model Performance: Results vs. Confidence', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(title="Models", bbox_to_anchor=(0.5, -0.07), loc='upper center', ncol=3, frameon=True, facecolor='white', framealpha=0.9)
    
    # Adjust axis limits to better show the data
    plt.xlim([-5, 85])
    plt.ylim([80, 100])
    
    plt.tight_layout()
    plt.savefig('output/results_vs_confidence.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_radar_chart(data: Dict[str, Any]) -> None:
    """
    Create a radar chart showing model performance across subject areas.
    
    Args:
        data: Dictionary containing subject results data
    """
    # Extract data
    models = data['models']
    subject_results = data['subject_results']
    
    # Set up figure
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, polar=True)
    
    # Get subject names and count
    subjects = list(subject_results.keys())
    N = len(subjects)
    
    # Set the angles for each subject (evenly spaced)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Set chart rotation to start from the top
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw axis lines for each subject
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(subjects, fontsize=12, fontweight='bold')
    
    # Set y-axis limits
    ax.set_ylim(0, 80)
    
    # Set grid line style and draw labels
    ax.set_rgrids([20, 40, 60, 80], angle=0, fontsize=10)
    ax.tick_params(axis='both', which='major', pad=15)
    
    # Define color palette
    colors = plt.cm.tab10(np.linspace(0, 1, len(models)))
    
    # Plot each model
    for i, model in enumerate(models):
        values = [subject_results[subject][i] for subject in subjects]
        values += values[:1]  # Close the loop
        
        # Plot the line
        ax.plot(angles, values, 'o-', linewidth=2, color=colors[i], 
                label=model, markersize=6)
        
        # Fill the area
        ax.fill(angles, values, color=colors[i], alpha=0.1)
    
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), frameon=True, 
               fontsize=10, title="Models", title_fontsize=12)
    
    # Add a title
    plt.title('Model Performance Across Subject Areas', size=16, fontweight='bold', y=1.1)
    
    # Improve aesthetics
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('output/radar_chart.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_language_fidelity(data: Dict[str, Any]) -> None:
    """
    Plot language fidelity statistics for Irish responses.
    
    Args:
        data: Dictionary containing language data
    """
    # Extract data
    models = data['language_models']
    language_data = data['language_data']
    
    # Set a more appealing style
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Define a custom color palette
    colors = ['#118822', '#3498db', '#e74c3c']  # Green, blue, and red tones
    
    # Create DataFrame for clarity
    df = pd.DataFrame({
        'Model': models,
        'Correct_Irish': language_data['correct_irish'],
        'Incorrect_Irish': language_data['incorrect_irish'],
        'Total_Irish': language_data['total_irish'],
    })
    
    # Plot
    x = np.arange(len(models))
    width = 0.225
    
    fig, ax = plt.subplots(figsize=(10, 6))
    # plot 3 bar per slot:
    bars1 = ax.bar(x - width, df['Total_Irish'], width, label='All responses', color=colors[0], edgecolor='white', linewidth=1)
    bars2 = ax.bar(x, df['Correct_Irish'], width, label='Correct responses', color=colors[1], edgecolor='white', linewidth=1)
    bars3 = ax.bar(x + width, df['Incorrect_Irish'], width, label='Incorrect responses', color=colors[2], edgecolor='white', linewidth=1)
    
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=14)
    ax.set_ylabel('Percentage of Responses', fontweight='bold', fontsize=14)
    ax.set_title('Percentage of Responses in Irish', fontweight='bold', fontsize=16)
    
    # Add a subtle horizontal grid and remove spines
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    # Enhanced legend
    ax.legend(fontsize=15, frameon=True, facecolor='white', framealpha=0.9, loc='upper center',bbox_to_anchor=(0.5, -0.08),ncol=3)
    
    # Improved value labels
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}', 
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('output/language_fidelity.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_benchmark_comparison(data: Dict[str, Any]) -> None:
    """
    Plot performance comparison across different Irish benchmarks.
    
    Args:
        data: Dictionary containing benchmark data
    """
    # Extract data
    models = data['benchmark_models']
    benchmark_data = data['benchmark_data']
    
    # Set a more appealing style
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Define a custom color palette
    colors = ['#5577dd', '#1177dd', '#3498db', '#ee4132']  # Blue and red tones
    
    # Create DataFrame for clarity
    df = pd.DataFrame({
        'Model': models,
        'SIB200': benchmark_data['SIB200'],
        'Belebele': benchmark_data['Belebele'],
        'IrishQA': benchmark_data['IrishQA'],
        'IrishBench': benchmark_data['IrishBench'],
    })
    
    # Plot
    x = np.arange(len(models))
    width = 0.15
    
    fig, ax = plt.subplots(figsize=(10, 5))
    # plot 4 bars per slot:
    bars1 = ax.bar(x - width * 1.5, df['SIB200'], width, label='SIB200', color=colors[0], edgecolor='white', linewidth=1)
    bars2 = ax.bar(x - width/2, df['Belebele'], width, label='Belebele', color=colors[1], edgecolor='white', linewidth=1)
    bars3 = ax.bar(x + width/2, df['IrishQA'], width, label='IrishQA', color=colors[2], edgecolor='white', linewidth=1)
    bars4 = ax.bar(x + width * 1.5, df['IrishBench'], width, label='IRLBench', color=colors[3], edgecolor='white', linewidth=1)
    
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=14)
    ax.set_ylabel('Score', fontweight='bold', fontsize=14)
    ax.set_ylim(20)
    
    ax.set_title('Performance of State-of-the-Art models on recent Irish benchmarks.', fontweight='bold', fontsize=16)
    
    # Add a subtle horizontal grid and remove spines
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    # Enhanced legend
    ax.legend(fontsize=15, frameon=True, facecolor='white', framealpha=0.9, loc='upper center',bbox_to_anchor=(0.5, -0.08),ncol=4)
    
    # Improved value labels
    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}', 
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('output/benchmark_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_subject_distribution(data: Dict[str, Any]) -> None:
    """
    Create a sunburst chart of the subject distribution.
    
    Args:
        data: Dictionary containing subject count data
    """
    subject_count = data['subject_count']
    
    # Flatten the dictionary
    labels = []
    parents = []
    values = []
    percentages = []
    
    # Calculate total sum
    total = sum(sum(sub.values()) for sub in subject_count.values())
    
    # Build sunburst data
    for main_cat, subcats in subject_count.items():
        main_sum = sum(subcats.values())
        labels.append(main_cat)
        parents.append("")
        values.append(main_sum)
        percentages.append(main_sum / total * 100)  # Percentage for inner layer
        
        for subcat, val in subcats.items():
            labels.append(subcat)
            parents.append(main_cat)
            values.append(val)
            percentages.append(val / total * 100)  # Percentage for outer layer
    
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(
            colors=percentages,
            colorscale='YlOrRd',
            colorbar=dict(
                title="%",
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5,
                thickness=20,
                len=0.7
            )
        ),
        hovertemplate='<b>%{label}</b><br>Value: %{value}<br>Percentage: %{color:.2f}%<extra></extra>',
        branchvalues="total"
    ))
    
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.write_html('subject_distribution.html')
    fig.show()

if __name__ == "__main__":
    # Get data for visualization
    data = prepare_visualization_data()
    
    # Generate all plots
    plot_language_comparison(data)
    plot_results_vs_confidence(data)
    plot_radar_chart(data)
    plot_language_fidelity(data)
    plot_benchmark_comparison(data)
    plot_subject_distribution(data)
    
    print("All visualizations have been generated and saved.")
