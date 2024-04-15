import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create DataFrame
df = pd.read_csv('./dataset/Data_Set_3.csv')

# Convert 'TIME' column to datetime
df['TIME'] = pd.to_datetime(df['TIME'])

# Convert time to seconds
df['TIME_SECONDS'] = (df['TIME'] - df['TIME'].iloc[0]).dt.total_seconds()

# # Calculate magnitude of acceleration
df['MAGNETIC_FIELD_MAGNITUDE'] = np.sqrt(df['GYROSCOPE_X']**2 + df['GYROSCOPE_Y']**2 + df['GYROSCOPE_Z']**2)
# df['MAGNETIC_FIELD_MAGNITUDE'] = df['MAGNETIC_FIELD_X']
plt.figure(figsize=(10, 6))

# Style
plt.style.use('default')
# Get unique contexts
contexts = df['CONTEXT'].unique()

# Plot each context separately with different background colors
for context in contexts:
    context_data = df[df['CONTEXT'] == context]
    plt.plot(context_data['TIME_SECONDS'], context_data['MAGNETIC_FIELD_MAGNITUDE'], label=f'Gyroscope Over Time ({context})')
    if context == 'OUTDOOR':
        plt.axvspan(context_data['TIME_SECONDS'].iloc[0], context_data['TIME_SECONDS'].iloc[-1], facecolor='white', alpha=0.5)
    if context == 'INDOOR':
        plt.axvspan(context_data['TIME_SECONDS'].iloc[0], context_data['TIME_SECONDS'].iloc[-1], facecolor='lightblue', alpha=0.5)

plt.xlabel('Time (seconds)')
plt.ylabel('Angular Velocity')
plt.title('Gyroscope Over Time')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

