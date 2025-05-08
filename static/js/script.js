const deletePic = document.getElementById('usun')
const galeria = document.getElementById('galeria')
const ButtonAdd = document.getElementById('plik')
let currentImg = document.getElementById('current')
let zdjecia = document.querySelectorAll('.zdj')

// Konwertujemy NodeList na tablicę
let tab = Array.from(zdjecia)

deletePic.addEventListener('click', () => {
    if (tab.length === 0) return;

    const pierwszeZdjecie = tab[0]
    const src = pierwszeZdjecie.getAttribute('src')
    const nazwaPliku = src.split('/').pop()  // Pobiera tylko nazwę pliku np. "zdj.jpg"

    fetch('/usun', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nazwa: nazwaPliku })
    })
    .then(response => {
        if (response.ok) {
            pierwszeZdjecie.remove()
            tab.shift()
        } else {
            alert('Błąd podczas usuwania zdjęcia')
        }
    })
})

document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById('plik');
    const preview = document.getElementById('preview');
    const wybraneDiv = document.getElementById('wybrane');

    input.addEventListener('change', function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();

            reader.addEventListener('load', function () {
                preview.setAttribute('src', this.result);
                preview.style.display = 'block';
                wybraneDiv.style.display = 'flex';
            });

            reader.readAsDataURL(file);
        } else {
            preview.setAttribute('src', '#');
            preview.style.display = 'none';
            wybraneDiv.style.display = 'none';
        }
    });
});