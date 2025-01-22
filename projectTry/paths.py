import xml.etree.ElementTree as ET

# Load the SVG file
tree = ET.parse('static/usa.svg')
root = tree.getroot()

# Extract paths
state_paths = {}
for path in root.findall('.//{http://www.w3.org/2000/svg}path'):
    state_code = path.attrib.get('id')
    state_d = path.attrib.get('d')
    if state_code and state_d:
        state_paths[state_code] = state_d

print(state_paths)  # Dictionary of state codes and paths
