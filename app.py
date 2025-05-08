from flask import Flask, app, jsonify, request, render_template, url_for, send_from_directory, redirect
import os

aplikacja = Flask(__name__)
folder_przeslane = 'uploads'

# Tworzymy folder 'uploads', jesli nie istnieje
if not os.path.exists(folder_przeslane):
    os.makedirs(folder_przeslane)

aplikacja.config['UPLOAD_FOLDER'] = folder_przeslane
aplikacja.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Funkcja sprawdzajaca, czy plik ma dozwolone rozszerzenie
def dozwolony_plik(nazwa_pliku):
    return '.' in nazwa_pliku and nazwa_pliku.rsplit('.', 1)[1].lower() in aplikacja.config['ALLOWED_EXTENSIONS']

# Strona glowna
@aplikacja.route('/', methods=['GET', 'POST'])
def strona_glowna():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Brak pliku w formularzu!', 400

        plik = request.files['file']

        if plik.filename == '':
            return 'Nie wybrano zadnego pliku!', 400

        if plik and dozwolony_plik(plik.filename):
            sciezka = os.path.join(aplikacja.config['UPLOAD_FOLDER'], plik.filename)
            plik.save(sciezka)
            # Przekierowanie do GET z nazwą zdjęcia
            return redirect(url_for('strona_glowna', zdjecie=plik.filename))

    # Obsługa GET – odczytanie zdjęcia z parametru
    zdjecie_nazwa = request.args.get('zdjecie')
    zdjecie = url_for('pokaz_plik', filename=zdjecie_nazwa) if zdjecie_nazwa else None

    wszystkie_zdjecia = sorted(
        os.listdir(aplikacja.config['UPLOAD_FOLDER']),
        key=lambda x: os.path.getmtime(os.path.join(aplikacja.config['UPLOAD_FOLDER'], x)),
        reverse=True
    )

    return render_template('index.html', zdjecie=zdjecie, wszystkie_zdjecia=wszystkie_zdjecia)


# Wyswietlanie pliku z folderu 'uploads'
@aplikacja.route('/uploads/<filename>')
def pokaz_plik(filename):
    return send_from_directory(aplikacja.config['UPLOAD_FOLDER'], filename)

@aplikacja.route('/usun', methods=['POST'])
def usun():
    dane = request.get_json()
    nazwa = dane.get('nazwa')
    if not nazwa:
        return jsonify({'error': 'Brak nazwy pliku'}), 400

    sciezka = os.path.join(aplikacja.config['UPLOAD_FOLDER'], nazwa)
    if os.path.exists(sciezka):
        os.remove(sciezka)
        return jsonify({'sukces': True}), 200
    else:
        return jsonify({'error': 'Plik nie istnieje'}), 404
    
if __name__ == '__main__':
    aplikacja.run(debug=True)