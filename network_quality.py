import json
import pandas as pd

logs_json = '''
[
    {"timestamp": "2024-01-15 08:00:00", "tower_id": "T10", "latency_ms": 35,  "jitter_ms": 4,  "packet_loss_pct": 0.1},
    {"timestamp": "2024-01-15 08:05:00", "tower_id": "T10", "latency_ms": 40,  "jitter_ms": 5,  "packet_loss_pct": 0.2},
    {"timestamp": "2024-01-15 08:10:00", "tower_id": "T10", "latency_ms": 38,  "jitter_ms": 6,  "packet_loss_pct": 0.1},
    {"timestamp": "2024-01-15 08:15:00", "tower_id": "T10", "latency_ms": 150, "jitter_ms": 45, "packet_loss_pct": 3.5},
    {"timestamp": "2024-01-15 08:00:00", "tower_id": "T11", "latency_ms": 60,  "jitter_ms": 12, "packet_loss_pct": 0.5},
    {"timestamp": "2024-01-15 08:05:00", "tower_id": "T11", "latency_ms": 65,  "jitter_ms": 10, "packet_loss_pct": 0.4},
    {"timestamp": "2024-01-15 08:10:00", "tower_id": "T11", "latency_ms": null, "jitter_ms": 11, "packet_loss_pct": 0.6},
    {"timestamp": "2024-01-15 08:15:00", "tower_id": "T11", "latency_ms": 70,  "jitter_ms": 14, "packet_loss_pct": 0.5},
    {"timestamp": "2024-01-15 08:00:00", "tower_id": "T12", "latency_ms": 120, "jitter_ms": 35, "packet_loss_pct": 2.5},
    {"timestamp": "2024-01-15 08:05:00", "tower_id": "T12", "latency_ms": 130, "jitter_ms": 40, "packet_loss_pct": 3.0},
    {"timestamp": "2024-01-15 08:10:00", "tower_id": "T12", "latency_ms": 110, "jitter_ms": 28, "packet_loss_pct": 1.8},
    {"timestamp": "2024-01-15 08:15:00", "tower_id": "T12", "latency_ms": 140, "jitter_ms": 50, "packet_loss_pct": 4.0}
]
'''

# Load and clean
df = pd.DataFrame(json.loads(logs_json))
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.dropna(subset=['latency_ms'])

# Summary per tower
tower_summary = df.groupby('tower_id')[['latency_ms', 'jitter_ms', 'packet_loss_pct']].mean()
print("Average metrics per tower:")
print(tower_summary.round(2))

# Flag poor-quality readings
latency_threshold = 100
jitter_threshold = 30
packet_loss_threshold = 2.0

df['bad_latency'] = df['latency_ms'] > latency_threshold
df['bad_jitter'] = df['jitter_ms'] > jitter_threshold
df['bad_packet_loss'] = df['packet_loss_pct'] > packet_loss_threshold
df['poor_quality'] = df['bad_latency'] | df['bad_jitter'] | df['bad_packet_loss']

# Bad reading rate per tower
bad_rate = df.groupby('tower_id')['poor_quality'].mean() * 100
print("\nPercentage of poor-quality readings per tower:")
print(bad_rate.round(1))

# Worst reading
worst_row = df.loc[df['latency_ms'].idxmax()]
print(f"\nWorst latency: {worst_row['latency_ms']} ms at tower {worst_row['tower_id']} ({worst_row['timestamp']})")