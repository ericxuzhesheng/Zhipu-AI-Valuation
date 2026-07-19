import pandas as pd

panel = pd.read_csv('eventstudy/event_panel.csv')
cap = panel[panel['event_type']=='capability']
print('=== Capability events ===')
for _, r in cap.iterrows():
    cols = ['event', 'react_mean', 'drift_mean', 'react_peer', 'drift_peer', 'drift_full']
    vals = [str(r[c]) for c in cols]
    print('  '.join(vals))

print()
rm = round(cap['react_mean'].astype(float).mean(), 1)
dm = round(cap['drift_mean'].astype(float).mean(), 1)
rp = round(cap['react_peer'].astype(float).mean(), 1)
dp = round(cap['drift_peer'].astype(float).mean(), 1)
print(f"Mean react_mean: {rm}")
print(f"Mean drift_mean: {dm}")
print(f"Mean react_peer: {rp}")
print(f"Mean drift_peer: {dp}")

print()
peer = panel[panel['event_type']=='capability_peer']
print('=== Peer capability events ===')
for _, r in peer.iterrows():
    print(f"  {r['event']}: react={r['react_mean']}, drift={r['drift_mean']}")

print()
print('=== Price summary ===')
ps = pd.read_csv('data/price_summary.csv')
print(ps.to_string(index=False))
