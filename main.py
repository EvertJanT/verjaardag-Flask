from flask import *
import os
import json

app = Flask(__name__)

# maak een lege mensen arry 
mensen = []

# het pad naar de mensen JSON file
json_file_path = os.path.join(os.path.dirname(__file__), 'templates', 'mensen.json')

# laad de data als de json file bestaat
if os.path.exists(json_file_path):
    with open(json_file_path, 'r') as file:
        try:
            mensen = json.load(file)
        except json.decoder.JSONDecodeError:
            print(f"ongeldige JSON data in de file: {json_file_path}")

@app.route('/')
def start():
    image = 'verjaardag.jpg'
    return render_template('index.html')

@app.route('/invoer', methods=['GET', 'POST'])
def invoer():
    if request.method == 'POST':
        #haal voor en achternaam datum op
        voornaam_input = request.form.get('voornaam')
        achternaam_input = request.form.get('achternaam')
        geboortedatum_input = request.form.get('date')

        # sla de input op in het mensen array
        mensen.append({
            'voornaam' : voornaam_input,
            'achternaam' : achternaam_input,
            'date': geboortedatum_input
        })

        # Save de mensen array in de JSON file
        save_user_inputs()

        return redirect(url_for('start'))  # Redirect naar de index pagina na form invoer
        
    return render_template('form.html')


@app.route('/zoek', methods=['GET', 'POST'])
def zoek():
    if request.method == 'POST':
        picklist_array_name, picklist_array_date = maak_array()
        return render_template('zoek.html', picklist_options=picklist_array_name, geboortedatums = picklist_array_date)
    return render_template('zoek.html')

@app.route('/display')
def display():
    return render_template('display.html', mensen=mensen)

@app.route('/resultaat')
def resultaat():
    return render_template('index.html')

def vind_geboortedatum(voornaam, achternaam):
    geboortedatum = 'niet gevonden'
    for persoon in mensen:
        if 'voornaam' in persoon and 'achternaam' in persoon:
            if persoon['voornaam'] == voornaam and persoon['achternaam'] == achternaam:
                geboortedatum = persoon['date']
                break
    return geboortedatum

def maak_array():
    array_name = []
    array_date=[]
    for persoon in mensen:
        vn = persoon['voornaam']
        an = persoon['achternaam']
        gd = persoon['date']
        fn = vn + ' ' + an
        array_name.append(fn)
        array_date.append(gd)
    return array_name, array_date


def save_user_inputs():
    with open(json_file_path, 'w') as file:
        json.dump(mensen, file, indent=4)

@app.route('/image')
def display_image():
    return send_file('verjaardag.jpg', mimetype='image/jpeg')

if __name__ == '__main__':
    app.run()



