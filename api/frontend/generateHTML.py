begin = None
middle = ""
end = None
eventHandlers = ""
with open('beginHTML.html') as file:
    begin = file.read()
with open('endHTML.html') as file:
    end = file.read()

for x in range(16):
    for y in range(30):
        middle += f'\t<button id="{x}-{y}" type="button" class="btn btn-secondary"></button>\n'
    middle += '\t<br>\n'

eventHandlers += "<script>\n"
for x in range (16):
    for y in range(30):
        eventHandlers += f'\tvar button{x}_{y}=document.getElementById("{x}-{y}"); button{x}_{y}.addEventListener("click", function(event) {{ button{x}_{y}.innerText="hello"}})\n'
eventHandlers += "</script>"
with open('index.html', 'w') as index:
    index.write(begin)
    index.write(middle)
    index.write(eventHandlers)
    index.write(end)