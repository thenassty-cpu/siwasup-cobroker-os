with open(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\index.html", encoding="utf-8") as f:
    text = f.read()

idx = text.find('function renderProperties()')
print(text[idx+500:idx+2500])
