HM_SteppeLandmark_2017
Resolution: 2017 x 2017
Formats: 16-bit PNG + .r16 (little-endian uint16)
Seed: 42

Terrain intent: semi-arid highland steppe/plateau for the tower concept
- Low-amplitude rolling plains
- Soft hero mound (~center-left) for landmark placement
- Soft eroded distant hills on far edges
- Light micro roughness

UE5 Landscape import:
1. Landscape Mode -> Import from File
2. Use HM_SteppeLandmark_2017.png (or .r16 with width/height 2017)
3. Match overall resolution 2017x2017
4. Start with relatively low Z scale (50-120) — concept is flat steppe
5. Place tower on the soft mound near center-left of the map

Keep distant mountain silhouette as fog + far hills in heightmap, or extra mesh cards if needed for shot matching.
