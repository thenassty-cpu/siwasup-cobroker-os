with open(r'C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts\line_gemini_webhook.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('SEARCH_ACTION_KEYWORDS =')
print(repr(text[idx:idx+350]))
