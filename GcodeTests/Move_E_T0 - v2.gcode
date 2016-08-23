;M190 S{print_bed_temperature} ;Uncomment to add your own bed temperature line
M109 S170 ;Uncomment to add your own temperature line
G21        ;metric values
G90        ;absolute positioning
M82        ;set extruder to absolute mode
M107       ;start with the fan off
G28 X0 Y0  ;move X/Y to min endstops
G28 Z0     ;move Z to min endstops
G92 E0                  ;zero the extruded length
G1 Y150

G1	F5.6432	E1.1286
G1	F7.5242	E2.6334
G1	F9.0291	E4.4392
G1	F11.2863	E6.6966
G1	F13.1674	E9.33
G1	F15.0484	E12.3398
G1	F18.8106	E16.1018
G1	F19.7511	E20.052
G1	F22.5727	E24.5666
G1	F26.3348	E29.8336
G1	F30.0969	E35.853
G1	F37.6211	E43.3772
G1	F39.5022	E51.2776
G1	F45.1453	E60.3066
G1	F56.4317	E71.593
G1	F67.718	E	85.1366
G1	F90.2907	E103.1948
G1	F135.436	E130.282
