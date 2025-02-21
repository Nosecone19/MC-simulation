
def simulate_website_navigation(
    pages={
        'expertise': {'base_probability': 0.25, 'std_dev': 0.03},
        'insights': {'base_probability': 0.15, 'std_dev': 0.02},
        'events': {'base_probability': 0.10, 'std_dev': 0.02},
        'about_us': {'base_probability': 0.20, 'std_dev': 0.03},
        'career': {'base_probability': 0.20, 'std_dev': 0.025},
        'contact_us': {'base_probability': 0.10, 'std_dev': 0.015}
    },
    num_simulations=10000,
    num_visitors=1000
):
    results = []
    
    for _ in range(num_simulations):
        simulation = {}
        
        # Generate probabilities with random variation
        probabilities = {}
        for page, params in pages.items():
            prob = np.random.normal(
                params['base_probability'],
                params['std_dev']
            )
            # Ensure probability stays within reasonable bounds
            probabilities[page] = max(0.01, min(0.4, prob))
            
        # Normalize probabilities to sum to 1
        total_prob = sum(probabilities.values())
        probabilities = {k: v/total_prob for k, v in probabilities.items()}
        
        # Simulate visitor clicks
        clicks = np.random.multinomial(num_visitors, list(probabilities.values()))
        
        # Store results
        for page, click_count in zip(pages.keys(), clicks):
            simulation[page] = click_count
            
        results.append(simulation)
    
    return pd.DataFrame(results)

# Run simulation
sim_results = simulate_website_navigation()

# Calculate statistics
stats = {
    'mean': sim_results.mean(),
    'std': sim_results.std(),
    'lower_ci': sim_results.quantile(0.025),
    'upper_ci': sim_results.quantile(0.975)
}

# Print results
print("Predicted page visits per 1000 visitors:")
print("\nPage | Mean (95% CI)")
print("-" * 40)
for page in sim_results.columns:
    mean = stats['mean'][page]
    ci_lower = stats['lower_ci'][page]
    ci_upper = stats['upper_ci'][page]
    print(f"{page:15} | {mean:.1f} ({ci_lower:.1f} - {ci_upper:.1f})")