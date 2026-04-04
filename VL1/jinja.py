import jinja2

def print_mails(): #email soll an verschiedene namen geschickt werden
    environment = jinja2.Environment()
    template = environment.from_string("Hallo {{ name }}, How are you?") #jinja kann auch funktionen einbauen

    for name1 in ["D","R","E","I"]:
        print(template.render(name=name1))

#print_mails()

def print_text():
    environment = jinja2.Environment()
    template = environment.from_string("{% for text in texts %} {{text}} {% endfor %}") #jinja braucht das ende (endfor)
    texts =["this is a text", "another text", "yet antoher"]

    print(template.render(texts = texts))

print_text()