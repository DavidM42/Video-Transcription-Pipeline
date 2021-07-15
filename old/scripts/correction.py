import language_tool_python
tool = language_tool_python.LanguageTool('de-DE')

text = 'Test satz mit recht schreib felhern'

matches = tool.check(text)

corrected = tool.correct(text)

print(corrected)