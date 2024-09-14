import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Simulate Data
# Simulate 1000 observations for control and treatment groups
np.random.seed(42)  # For reproducibility
n_control = 500
n_treatment = 500

# Simulate conversion data (0 or 1) with different probabilities
control_conversion = np.random.binomial(1, p=0.10, size=n_control)
treatment_conversion = np.random.binomial(1, p=0.12, size=n_treatment)

# Combine into a DataFrame
data = pd.DataFrame({
    'group': ['control'] * n_control + ['treatment'] * n_treatment,
    'conversion': np.concatenate([control_conversion, treatment_conversion])
})

# Step 2: Group Data
control_group = data[data['group'] == 'control']
treatment_group = data[data['group'] == 'treatment']

# Step 3: Calculate Conversion Rates
control_conversion_rate = control_group['conversion'].mean()
treatment_conversion_rate = treatment_group['conversion'].mean()

print(f"Control Conversion Rate: {control_conversion_rate * 100:.2f}%")
print(f"Treatment Conversion Rate: {treatment_conversion_rate * 100:.2f}%\n")

# Step 4: Perform t-test
t_stat, p_value = stats.ttest_ind(control_group['conversion'], treatment_group['conversion'])

print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4f}\n")

# Step 5: Visualize the Results
sns.barplot(x='group', y='conversion', data=data, ci=95)
plt.title('Conversion Rate by Group')
plt.ylabel('Conversion Rate')
plt.show()

# Step 6: Conclusion
alpha = 0.05
if p_value < alpha:
    print("Reject the null hypothesis: The intervention has a significant effect.")
    effect_size = (treatment_conversion_rate - control_conversion_rate) * 100
    print(f"Effect Size: {effect_size:.2f}% increase in conversion rate.")
else:
    print("Fail to reject the null hypothesis: The intervention does not have a significant effect.")

# Step 7: Calculate Confidence Interval for Difference in Means
diff_mean = treatment_conversion_rate - control_conversion_rate
pooled_se = np.sqrt(control_conversion_rate * (1 - control_conversion_rate) / n_control +
                    treatment_conversion_rate * (1 - treatment_conversion_rate) / n_treatment)

# 95% Confidence Interval
ci_lower = diff_mean - 1.96 * pooled_se
ci_upper = diff_mean + 1.96 * pooled_se
print(f"\n95% Confidence Interval for Difference in Conversion Rates: [{ci_lower:.4f}, {ci_upper:.4f}]")
