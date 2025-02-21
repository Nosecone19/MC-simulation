
# Define a class for simulating our risks 
class RiskSimulation:
    def __init__(self, num_simulations=1000):
        self.num_simulations = num_simulations
        
        self.likelihood = {  # Dictionary of our risks in terms of likelihood (based on historical occurrence data)
            'Data Migration Issues': 0.35,    # 35% chance of occurring
            'Integration Failures': 0.25,      
            'Performance Problems': 0.20,      
            'Security Configuration Issues': 0.15,  
            'Custom Script Errors': 0.30,      
            'Authentication Problems': 0.10,    
            'API Connection Issues': 0.20 
        }

        self.impact_ranges = {  # Dictionary of the impact in terms of min/max duration (in days)
            'Data Migration Issues': (1, 10),  # Can have impact between 1-10 days
            'Integration Failures': (2, 15),
            'Performance Problems': (1, 7),
            'Security Configuration Issues': (3, 12),
            'Custom Script Errors': (1, 5),
            'Authentication Problems': (1, 8),
            'API Connection Issues': (2, 10)
        }

    # Method to simulate a single project implementation
    def simulate_single_project(self):
        total_impact = 0  # Counter for total days of delay in this project
        encountered_issues = []  # A log to store all encountered issues in ONE simulation

        for risk, probability in self.likelihood.items():  # Iteration over each identified risk and its probability
            if np.random.random() < probability:  # Generates a random number between 0 and 1, and compares to probability
                impact = np.random.randint(  # Calculation for how many days of delay it causes
                    self.impact_ranges[risk][0],  # minimum days of delay
                    self.impact_ranges[risk][1] + 1  # maximum days of delay (+1 because randint is exclusive)
                )
                total_impact += impact
                encountered_issues.append((risk, impact))  # Add this risk to our list
        return total_impact, encountered_issues

    def run_simulation(self):  # Method for running multiple simulations
        results = []  # Store total impact from each simulation
        all_issues = []  

        for _ in range(self.num_simulations):  # "_" is used since we don't need the loop variable
            impact, issues = self.simulate_single_project()  # Get the results of total issues and max value of impact_range for one simulation 
            results.append(impact)  # Add the impact from the single simulation to our results list
            all_issues.extend(issues)  # Add all issues from this simulation to our 'all_issues' list
        return results, all_issues

    def analyze_results(self, results, issues):  # Here we calculate basic stats from all simulations
        stats = {
            'Mean Impact (days)': np.mean(results),          # Average delay across all simulations
            'Median Impact (days)': np.median(results),      # Middle value when sorted
            'Std Dev (days)': np.std(results),              # How spread out the delays are
            '90th Percentile (days)': np.percentile(results, 90),  # 90% of values fall below this
            'Max Impact (days)': np.max(results),           # Longest delay seen
            'Min Impact (days)': np.min(results)            # Shortest delay seen
        }

        issue_counts = pd.DataFrame(issues, columns=['Issue', 'Impact'])  # With pandas we can create a dataframe for segmenting our issues and impacts in columns
        issue_summary = issue_counts.groupby('Issue').agg({  # Group issues by type and calculate stats for each type
            'Impact': ['count', 'mean', 'sum']  # The selected stats for each issue type
        })
        
        # Rename the columns to be more descriptive
        issue_summary.columns = ['Frequency', 'Avg Impact', 'Total Impact']
        
        # Add a column showing how often each issue occurred across all simulations
        issue_summary['Occurrence Rate'] = issue_summary['Frequency'] / self.num_simulations
        
        return stats, issue_summary

    # Now we visualize our issues and impact ranges with matplotlib
    def plot_results(self, results):
        plt.figure(figsize=(12, 6))  # Determining the columns and rows for our visualization 
        plt.hist(results, bins=30, alpha=0.7, color='red') # We will use a histogram to visualize ALL our impact ranges
        plt.title('Distrubution of our identified risks') # Title
        plt.xlabel('Total Impact (days)') # X-axis
        plt.ylabel('Frequency') # Y-axis
        plt.axvline(np.mean(results), # Adds a vertical line showing 90th percentile
                   color='red', 
                   linestyle='dashed', 
                   linewidth=2, 
                   label=f'Mean: {np.mean(results):.1f} days')
        plt.legend() # Legend makes a box with descriptions of each plot
        plt.grid(True, alpha=0.3) # Adds gridlines to the plot above
        plt.show() # Displays the plot
simulator = RiskSimulation(num_simulations=1000) # Create an instance of 10k simulations instead of 1k, in case we want to try a differen batch size
results, issues = simulator.run_simulation() # Run all simulations and get results
stats, issue_summary = simulator.analyze_results(results, issues) # We run the analyze method through our results and issue data

# Print simulation statistics with formatting
print("\nSimulation Statistics:")
for key, value in stats.items():
    # Print each statistic with 2 decimal places
    print(f"{key}: {value:.2f}")

# Print detailed issue analysis
print("\nIssue Analysis:")
print(issue_summary)

# Create and display visualization
simulator.plot_results(results)
# Print simulation statistics with formatting
print("\nSimulation Statistics:")
for key, value in stats.items():
    # Print each statistic with 2 decimal places
    print(f"{key}: {value:.2f}")

# Print detailed issue analysis
print("\nIssue Analysis:")
print(issue_summary)

# Create and display visualization
simulator.plot_results(results)
