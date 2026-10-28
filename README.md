# Network Quality Monitoring

A Python script that analyzes cell tower telemetry (latency, jitter, and packet loss) to find which towers are delivering poor service.

## How it works
- Parses tower readings from JSON into a pandas DataFrame
- Cleans the data by removing readings with a missing latency value
- Calculates average latency, jitter, and packet loss per tower
- Flags each reading as poor quality if it exceeds any threshold: latency over 100 ms, jitter over 30 ms, or packet loss over 2%
- Calculates the percentage of poor-quality readings per tower
- Reports the single worst latency reading and where it happened

## Example results (sample data)
| Tower | Avg latency | Poor-quality readings |
|-------|-------------|-----------------------|
| T10   | 65.8 ms     | 25%                   |
| T11   | 65.0 ms     | 0%                    |
| T12   | 125.0 ms    | 100%                  |

Worst latency: 150 ms at tower T10.

## How to run
```bash
python network_quality.py
```

## What I learned
- Handling missing values from JSON (`null` becomes `NaN`) with `.dropna(subset=[...])`
- Using `.groupby()` on several columns at once to get averages per tower
- Creating True/False flag columns from threshold comparisons
- Combining flags with `|` (or) to build an overall `poor_quality` column
- Taking the `.mean()` of a True/False column to get a percentage of readings
- Using `.idxmax()` with `.loc[]` to retrieve the full row with the highest value
- Keeping thresholds in named variables so they're easy to change

## Notes
- The thresholds are illustrative values, not official telecom standards.
- All data is fictional sample data.

## Dependencies
Requires pandas:
```bash
pip install pandas
```
