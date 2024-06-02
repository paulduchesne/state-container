from flask import Flask, render_template
import json
import pathlib
import rdflib
import uuid

app = Flask(__name__)

# initialise user credentials.

credentials_path = pathlib.Path.cwd() / 'identification.json'
if not credentials_path.exists():
    name_uuid, pass_uuid = str(uuid.uuid4()), str(uuid.uuid4())
    with open(credentials_path, 'w', encoding='utf-8') as f:
        json.dump({'name':name_uuid, 'pass':pass_uuid}, f, ensure_ascii=False, indent=4)
else: 
    with open(credentials_path, encoding='utf-8') as f:
        pay = json.loads(f.read())
        name_uuid, pass_uuid = pay['name'], pay['pass']

# TODO credential validity checks would be a great idea here.

# load existing local rdf into rdflib graph.

graph = rdflib.Graph()
for x in (pathlib.Path.cwd() / 'local').rglob('*'):
    if x.suffix == '.ttl':
        graph.parse(x)

print(len(graph), 'triples loaded from local storage.')

@app.route("/")
def main_page():

    # if author label does not exist, send to page requesting that data.

    author_label = [o for s,p,o in graph.triples((rdflib.URIRef(f"https://{name_uuid}.org/resource/{name_uuid}"), rdflib.RDFS.label, None))]
    if not len(author_label):
        return render_template('label.html')
    else:

        # don't go to main, instead you should be going to https://{name_uuid}.org/resource/{name_uuid}
        # this raises a question around local storage vs general web access.
        # I would imagine a good model to follow is "local" is unencrypted which drives the local experience
        # but the data which is exported for sharing (and federating) sits in a "share" directory.

        return render_template('main.html')

if __name__ == "__main__":
    app.run(debug=True, port=5017)