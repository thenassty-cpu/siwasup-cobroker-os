import json

with open('siwasup_all_properties.json', 'r', encoding='utf-8') as f:
    props = json.load(f)

js_content = 'var ALL_PROPERTIES_DATA = ' + json.dumps(props, ensure_ascii=False, indent=2) + ';\n\n'
js_content += 'if (typeof window !== "undefined") {\n'
js_content += '  window.SIWASUP_PROPERTIES = ALL_PROPERTIES_DATA;\n'
js_content += '  window.ALL_PROPERTIES_DATA = ALL_PROPERTIES_DATA;\n'
js_content += '}\n'
js_content += 'if (typeof module !== "undefined" && module.exports) {\n'
js_content += '  module.exports = ALL_PROPERTIES_DATA;\n'
js_content += '}\n'

with open('siwasup_all_properties.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Successfully generated siwasup_all_properties.js with {len(props)} properties")
