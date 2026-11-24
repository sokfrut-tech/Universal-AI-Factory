# Forest LTE Connectivity

- Project ID: `FOREST_LTE`
- Repository: not confirmed
- Evidence status: REPORTED (original owner-authored project memory located; technical field claims not independently measured)

## Goal
Portable, reliable 4G LTE connectivity deep in a forest. Prioritize reception stability and weather resilience over lowest price or minimum size. 5G is out of scope.

## Recovered original project memory
The original owner project-memory file dated 2026-10-27 is preserved in the Library and referenced in [UPKB/SOURCES/FOREST_LTE_ORIGINAL_BRIEF_REFERENCE.md](../../SOURCES/FOREST_LTE_ORIGINAL_BRIEF_REFERENCE.md). The original file was not modified.

- Library file: `Память_проект_интернет_в_лесу_2026-10-27.md`
- Library file ID: `file_00000000d01c8211b6540c2541903399`
- Library item ID: `libfile_1e9bfc9db7588191959b3cd8793b0664`
- Duplicate snapshot ID: `file_00000000ecd482118aa70e0b96d902b5`

## Reported constraints from the original brief
- Bands of interest: B3, B7, B20, B31 (LTE450, about 450 MHz) and B38.
- Existing antenna: VARIUS Forester MIMO 2x2; reception reportedly changes with weather. The cause is unknown; do not assume the antenna itself is defective.
- Current use: temporary shelter; later a compact transportable setup for a new forest home.
- Mast top may be approximately 3–6 m above nearby trees; tower distance and direction are unknown.
- Masts and SMA pigtails are available; actual cable type, length, connectors and losses are not yet verified.
- Router was not in hand at the time of the original brief; do not demand RF measurements before there is a modem/router to measure.
- Router must support external antennas, weather-safe installation and operator/SIM failover where technically available.
- 5 GHz Wi-Fi is for the local network, not cellular access.

## Engineering constraints
- Verify local B31/LTE450 availability; band support alone does not imply network coverage.
- Verify the exact modem/router hardware revision and every required band.
- Evaluate LTE450 separately from higher LTE bands.
- Do not equate four antenna connectors with useful LTE 4x4 MIMO.
- Calculate coax loss from real cable type, length and frequency; consider a protected router enclosure and Ethernet backhaul.
- Include sealing, drip loops, wind restraint, safe mounting, power and thermal limits.
- Distinguish dual-SIM switching in one modem from independent modem/Multi-WAN failover.
- Do not invent coverage, speed, RF measurements or current prices.

## Evidence gaps
No canonical repository, RF survey, confirmed operator/site coverage, exact cable inventory or current equipment labels/photos are indexed. Original brief details remain owner-reported until measured or confirmed against primary technical sources.

## Next
Recover any newer site survey, equipment labels/photos, operator observations and cable inventory. Then verify current official datasheets and local B31 availability before selecting hardware or purchasing anything.
