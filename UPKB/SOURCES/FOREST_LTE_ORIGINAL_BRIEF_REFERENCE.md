# Forest LTE — original brief provenance

- Project: `FOREST_LTE`
- Source artifact: `Память_проект_интернет_в_лесу_2026-10-27.md`
- Library file ID: `file_00000000d01c8211b6540c2541903399`
- Library item ID: `libfile_1e9bfc9db7588191959b3cd8793b0664`
- Version: `1`
- Source created: `2026-10-27T10:52:45.923974Z`
- Duplicate snapshot: `Память_проект_интернет_в_лесу_2026-10-27(1).md`, file ID `file_00000000ecd482118aa70e0b96d902b5`, created `2026-10-27T10:59:00Z`
- Source handling: original Library files are preserved and were not modified.
- Evidence status: original owner-authored project memory located; equipment/field statements inside it remain owner-reported unless independently measured.

## Recovered scope

Portable, reliable 4G LTE connectivity deep in a forest. 5G is out of scope. Priority is stable reception and weather resilience over lowest cost or minimum size.

Reported bands: B3, B7, B20, B31 (LTE450, around 450 MHz) and B38. Existing antenna: VARIUS Forester MIMO 2x2. Its reception was reported as weather-sensitive, but the cause was explicitly unresolved; do not assume the antenna itself is defective.

Reported installation constraints: antenna mast may rise roughly 3–6 m above nearby trees; tower distance/direction unknown. Masts and SMA pigtails are available; cable type, length, losses and connectors still require verification. Router was not yet in hand at the time of the brief, so do not request RSRP/RSRQ/SINR measurements prematurely.

The brief records important distinctions:
- 5 GHz Wi-Fi is an indoor LAN band, not a cellular band.
- Dual-SIM switching in one modem is not the same as simultaneous independent modem/WAN failover.
- Four antenna connectors do not prove LTE 4x4 MIMO benefit.
- B31 support must be confirmed in the actual modem/router hardware revision; B31 network availability at the eventual site is also unknown.
- Weather-related outages may involve wet vegetation/path loss, connectors, wind/aim, cable losses, cell/band changes or operator network conditions; cause remains unknown.

## Engineering gates

1. Verify local B31/LTE450 availability rather than assuming coverage.
2. Require official evidence for B3+B7+B20+B31+B38 support in one hardware revision, or document a deliberate multi-modem architecture.
3. Evaluate LTE450 separately from higher LTE bands; confirm antenna gain, pattern, polarization, independent ports, impedance and weather protection.
4. Verify modem category, supported LTE MIMO layers and network capability before valuing 4x4.
5. Calculate real coax loss from cable type, length and frequency; consider protected router placement and Ethernet backhaul.
6. Include connector sealing, drip loops, wind restraint, safe mounting and power/thermal protection.
7. Verify health checks, failover/failback and actual interruption time for any multi-SIM/Multi-WAN design.
8. Calculate carried mass, dimensions, power and full installed cost.
9. Do not invent coverage, speed, RF measurements or current prices.
10. Separate manufacturer claims from independent measurements.

## Continuation

Recover any newer site survey, operator coverage observations, equipment labels/photos and cable inventory. Then refresh current product datasheets and coverage evidence before selecting hardware. Do not buy or deploy based on this historical brief alone.
