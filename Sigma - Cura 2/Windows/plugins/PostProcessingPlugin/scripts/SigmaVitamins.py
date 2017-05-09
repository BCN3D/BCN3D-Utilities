# Guillem Àvila Padró - April 2017
# Released under GNU LICENSE
# https://opensource.org/licenses/GPL-3.0

# Set of post processing algorithms to make the best GCodes for your BCN3D Sigma

from ..Script import Script
import math
class SigmaVitamins(Script):

    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name":"Sigma Vitamins",
            "key": "SigmaVitamins",
            "metadata": {},
            "version": 2,
            "settings": 
            {                
                "activeExtruders":
                {
                    "label": "Heat only essentials",
                    "description": "When printing with one hotend only, avoid heating the other one.",
                    "type": "bool",
                    "default_value": true
                },
                "fixFirstRetract":
                {
                    "label": "Fix First Extrusion",
                    "description": "Avoid zeroing extruders at the beginning.",
                    "type": "bool",
                    "default_value": true
                },
                "fixToolChangeZHop":
                {
                    "label": "Fix Tool Change Z Hop",
                    "description": "When changing between toolheads, first move X/Y and then move Z.",
                    "type": "bool",
                    "default_value": true
                },
                "zHopDistance":
                {
                    "label": "Z Hop Distance",
                    "description": "Distance to lift Z when changing toolheads.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 2,
                    "minimum_value": "0",
                    "minimum_value_warning": "0",
                    "maximum_value_warning": "5",
                    "enabled": "fixToolChangeZHop"
                },
                "smartPurge":
                {
                    "label": "SmartPurge",
                    "description": "Add an extra prime amount to compensate oozed material while the Extruder was idle. Disable Prime tower to save time and filament.",
                    "type": "bool",
                    "default_value": false
                },
                "leftHotendNozzleSize":
                {
                    "label": "Left Hotend",
                    "description": "Select Left Hotend.",
                    "type": "enum",
                    "options": {"0.3mm_-_Brass": "0.3mm - Brass", "0.4mm_-_Brass": "0.4mm - Brass", "0.5mm_-_Hardened_Steel": "0.5mm - Hardened Steel", "0.6mm_-_Brass": "0.6mm - Brass", "0.8mm_-_Brass": "0.8mm - Brass", "1.0mm_-_Brass": "1.0mm - Brass"},
                    "default_value": "0.4mm_-_Brass",
                    "enabled": "smartPurge"
                },
                "leftHotendFilament":
                {
                    "label": "Left Extruder Material",
                    "description": "Select which material is being used in Left Extruder to prime the right amount.",
                    "type": "enum",
                    "options": {"Arnitel_ID_2045": "Arnitel ID 2045", "Colorfabb_HT": "Colorfabb HT", "Colorfabb_PLA-PHA": "Colorfabb PLA-PHA", "Colorfabb_SteelFill": "Colorfabb SteelFill", "Colorfabb_XT": "Colorfabb XT", "Colorfabb_XT-CF20": "Colorfabb XT-CF20", "Colorfabb_nGen": "Colorfabb nGen", "Colorfabb_nGenflex": "Colorfabb nGenflex", "Colorfila_ABS_Pro": "Colorfila ABS Pro", "Colorfila_PLA": "Colorfila PLA", "Colorfila_TPU": "Colorfila TPU", "Esun_PVA": "Esun PVA", "Recreus_Filaflex_(210-230C)": "Recreus Filaflex (210-230C)", "Recreus_Filaflex_(230-260C)": "Recreus Filaflex (230-260C)"},
                    "default_value": "Colorfila_PLA",
                    "enabled": "smartPurge"
                },
                "rightHotendNozzleSize":
                {
                    "label": "Right Hotend",
                    "description": "Select Right Hotend.",
                    "type": "enum",
                    "options": {"0.3mm_-_Brass": "0.3mm - Brass", "0.4mm_-_Brass": "0.4mm - Brass", "0.5mm_-_Hardened_Steel": "0.5mm - Hardened Steel", "0.6mm_-_Brass": "0.6mm - Brass", "0.8mm_-_Brass": "0.8mm - Brass", "1.0mm_-_Brass": "1.0mm - Brass"},
                    "default_value": "0.4mm_-_Brass",
                    "enabled": "smartPurge"
                },
                "rightHotendFilament":
                {
                    "label": "Right Extruder Material",
                    "description": "Select which material is being used in Right Extruder to prime the right amount",
                    "type": "enum",
                    "options": {"Arnitel_ID_2045": "Arnitel ID 2045", "Colorfabb_HT": "Colorfabb HT", "Colorfabb_PLA-PHA": "Colorfabb PLA-PHA", "Colorfabb_SteelFill": "Colorfabb SteelFill", "Colorfabb_XT": "Colorfabb XT", "Colorfabb_XT-CF20": "Colorfabb XT-CF20", "Colorfabb_nGen": "Colorfabb nGen", "Colorfabb_nGenflex": "Colorfabb nGenflex", "Colorfila_ABS_Pro": "Colorfila ABS Pro", "Colorfila_PLA": "Colorfila PLA", "Colorfila_TPU": "Colorfila TPU", "Esun_PVA": "Esun PVA", "Recreus_Filaflex_(210-230C)": "Recreus Filaflex (210-230C)", "Recreus_Filaflex_(230-260C)": "Recreus Filaflex (230-260C)"},
                    "default_value": "Colorfila_PLA",
                    "enabled": "smartPurge"
                }
            }
        }"""

    def execute(self, data):
        activeExtruders = self.getSettingValueByKey("activeExtruders")
        fixFirstRetract = self.getSettingValueByKey("fixFirstRetract")
        fixToolChangeZHop = self.getSettingValueByKey("fixToolChangeZHop")
        zHopDistance = self.getSettingValueByKey("zHopDistance")
        smartPurge = self.getSettingValueByKey("smartPurge")
        leftHotendId = self.getSettingValueByKey("leftHotendNozzleSize")
        leftFilamentId = self.getSettingValueByKey("leftHotendFilament")
        rightHotendId = self.getSettingValueByKey("rightHotendNozzleSize")
        rightFilamentId = self.getSettingValueByKey("rightHotendFilament")

        if activeExtruders:
            bothExtruders = False
            scanning = False
            printing = False
            idleExtruder = "T1"
            for layer in data:
                index = data.index(layer)
                lines = layer.split("\n")
                for line in lines:                    
                    if scanning:
                        if "G" in line and "X" in line and "Y" in line and "E" in line:
                            printing = True
                        elif line.startswith("T0") or (line.startswith("T1") and printing):
                            bothExtruders = True
                            break
                        elif line.startswith("T1") and not printing:
                            idleExtruder = "T0"
                    else:
                        if line.startswith(";LAYER_COUNT:"):
                            scanning = True
                if bothExtruders:
                    break                    
            if not bothExtruders:
                startGcodeCorrected = False
                for layer in data:
                    index = data.index(layer)
                    lines = layer.split("\n")
                    for tempIndex in range(len(lines)):
                        if not startGcodeCorrected:
                            try:
                                line = lines[tempIndex]
                                line1 = lines[tempIndex + 1]
                                line2 = lines[tempIndex + 2]
                                line3 = lines[tempIndex + 3]
                                if line.startswith(idleExtruder) and line1.startswith("G92 E0") and line2.startswith("G1 E") and line3.startswith("G92 E0"):
                                    layer = layer.replace(line+"\n"+line1+"\n"+line2+"\n"+line3+"\n", "")
                                    startGcodeCorrected = True  
                            except:
                                pass                          
                        if idleExtruder != "T0":
                            if "T1" in line:
                                layer = layer.replace(line+"\n", "")
                        elif idleExtruder != "T1":
                            if (line.startswith("M104 S") or line.startswith("M109 S")) and "T1" not in line:
                                layer = layer.replace(line+"\n", "")  
                    data[index] = layer

        if fixFirstRetract:
            startGcodeCorrected = False
            for layer in data:
                index = data.index(layer)
                lines = layer.split("\n")
                for tempIndex in range(len(lines)):
                    try:
                        line = lines[tempIndex]
                        line1 = lines[tempIndex + 1]
                        line2 = lines[tempIndex + 2]
                        line4 = lines[tempIndex + 4]
                        line5 = lines[tempIndex + 5]
                    except:
                        break
                    if line.startswith(";LAYER:0"):
                        if "G1" in line1 and "F" in line1 and "E" in line1 and line2.startswith("G92 E0") and (line4 == "T0" or line4 == "T1") and line5.startswith("G92 E0"):
                            layer = layer.replace(line+"\n"+line1+"\n"+line2+"\n", line+"\n")
                            layer = layer.replace(line4+"\n"+line5+"\n", line4+"\n"+line1+"\n")
                        break
                data[index] = layer
                if startGcodeCorrected:
                    break

        if fixToolChangeZHop:
            for layer in data:
                index = data.index(layer)
                lines = layer.split("\n")
                for tempIndex in range(len(lines)):
                    try:
                        line = lines[tempIndex]
                        line1 = lines[tempIndex + 1]
                        line2 = lines[tempIndex + 2]
                        line3 = lines[tempIndex + 3]
                        line4 = lines[tempIndex + 4]
                    except:
                        break
                    if (line == "T0" or line == "T1") and line1 == "G92 E0" and line2 == "G91" and "G1 F" in line3 and line4 == "G90":
                        layer = layer.replace(line3, line3.split("Z")[0]+"Z"+str(zHopDistance))
                        lineCount = 6 # According to extruder_start_gcode in Sigma Extruders definitions
                        while not lines[tempIndex+lineCount].startswith(";TYPE"):
                            currentLine = lines[tempIndex+lineCount]
                            if currentLine.startswith("G"):
                                if "G0" in currentLine and "F" in currentLine and "X" in currentLine and "Y" in currentLine and "Z" in currentLine:
                                    zValue = self.getValue(currentLine, "Z")
                                    fValue = self.getValue(currentLine, "F")
                                if lines[tempIndex+lineCount+1].startswith("G"):
                                    layer = layer.replace(currentLine+"\n", "")
                                else:
                                    xValue = self.getValue(currentLine, "X")
                                    yValue = self.getValue(currentLine, "Y")
                                    layer = layer.replace(currentLine, "G0 F"+str(int(fValue))+" X"+str(xValue)+" Y"+str(yValue)+"\nG0 Z"+str(zValue))
                            lineCount += 1
                        break
                data[index] = layer

        if smartPurge:
            for layer in data:
                index = data.index(layer)
                lines = layer.split("\n")
                for tempIndex in range(len(lines)):
                    try:
                        line = lines[tempIndex]
                        line1 = lines[tempIndex + 1]
                        line2 = lines[tempIndex + 2]
                        line3 = lines[tempIndex + 3]
                        line4 = lines[tempIndex + 4]
                    except:
                        break
                    if line == "T0" and line1 == "G92 E0" and line2 == "G91" and "G1 F" in line3 and line4 == "G90":
                        lineCount = 6 # According to extruder_start_gcode in Sigma Extruders definitions
                        while not lines[tempIndex+lineCount].startswith(";TYPE"):
                            lineCount += 1
                        primeLine = lines[tempIndex+lineCount+1]
                        eValue = self.getValue(primeLine, "E")
                        layer = layer.replace(primeLine, primeLine.split("E")[0]+str(eValue+purgeValues(leftHotendId, leftFilamentId))+"\nG92 E"+str(eValue))
                        break
                    if line == "T1" and line1 == "G92 E0" and line2 == "G91" and "G1 F" in line3 and line4 == "G90":
                        lineCount = 6 # According to extruder_start_gcode in Sigma Extruders definitions
                        while not lines[tempIndex+lineCount].startswith(";TYPE"):
                            lineCount += 1
                        primeLine = lines[tempIndex+lineCount+1]
                        eValue = self.getValue(primeLine, "E")
                        layer = layer.replace(primeLine, primeLine.split("E")[0]+str(eValue+purgeValues(rightHotendId, rightFilamentId))+"\nG92 E"+str(eValue))
                        break
                data[index] = layer

        return data

def purgeValues(hotend, filament):
    hotends = {"0.3mm_-_Brass": 0.3, "0.4mm_-_Brass": 0.4, "0.5mm_-_Hardened_Steel": 0.5, "0.6mm_-_Brass": 0.6, "0.8mm_-_Brass": 0.8, "1.0mm_-_Brass": 1.0}
    filaments = {"Arnitel_ID_2045": 120, "Colorfabb_HT": 40, "Colorfabb_PLA-PHA": 40, "Colorfabb_SteelFill": 55, "Colorfabb_XT": 40, "Colorfabb_XT-CF20": 40, "Colorfabb_nGen": 40, "Colorfabb_nGenflex": 80, "Colorfila_ABS_Pro": 10, "Colorfila_PLA": 16, "Colorfila_TPU": 120, "Esun_PVA": 120, "Recreus_Filaflex_(210-230C)": 120, "Recreus_Filaflex_(230-260C)": 120}

    # nozzleSizeBehavior
    maxPurgeLenghtAtHotendTip = 2.25 * filaments[filament]
    minPurgeLenghtAtHotendTip = 0.5  * filaments[filament]
    curveGrowth = 1 # Here we assume the growth curve is constant for all materials. Change this value if it's not
    extraPrimeDistance = (maxPurgeLenghtAtHotendTip - (maxPurgeLenghtAtHotendTip-minPurgeLenghtAtHotendTip)*math.exp(-hotends[hotend]/float(curveGrowth)))/float(filaments[filament])

    return round(extraPrimeDistance / 10, 5)
