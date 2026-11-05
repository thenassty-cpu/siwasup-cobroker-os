import win32com.client

try:
    app = win32com.client.Dispatch("Illustrator.Application")
    app.UserInteractionLevel = -1
    res = app.DoJavaScript("app.name + ' ' + app.version;")
    print("SUCCESS:", res)
    print("Open Docs:", app.Documents.Count)
    for i in range(1, app.Documents.Count + 1):
        print(f"Doc {i}: {app.Documents(i).Name}")
except Exception as e:
    print("ERROR:", e)
