/* industrietaucher.ch · gemeinsames Script für alle Seiten */

/* Mobilmenü */
function toggleMenu() {
  var nav = document.getElementById('main-nav');
  var btn = document.querySelector('.menu-btn');
  var open = nav.classList.toggle('open');
  btn.setAttribute('aria-expanded', open ? 'true' : 'false');
}
document.addEventListener('click', function (e) {
  if (e.target.closest('#main-nav a')) {
    var nav = document.getElementById('main-nav');
    if (nav) nav.classList.remove('open');
  }
});

/* Sprache (Auswahl bleibt beim Seitenwechsel erhalten) */
function setLang(lang) {
  document.body.classList.toggle('en', lang === 'en');
  document.querySelectorAll('.lang-btn').forEach(function (b) {
    b.classList.toggle('active', b.dataset.lang === lang);
  });
  try { localStorage.setItem('lang', lang); } catch (err) {}
}
(function () {
  var lang = 'de';
  try { lang = localStorage.getItem('lang') || 'de'; } catch (err) {}
  // Nur auf zweisprachigen Seiten (mit Sprachumschalter) anwenden
  if (lang === 'en' && document.querySelector('.lang-btn')) setLang('en');
})();

/* Bildergalerie */
function openLightbox(btn) {
  var img = btn.querySelector('img');
  var box = document.getElementById('lightbox');
  box.querySelector('img').src = img.src;
  box.querySelector('img').alt = img.alt;
  box.classList.add('active');
}
function closeLightbox() {
  var box = document.getElementById('lightbox');
  if (box) box.classList.remove('active');
}
document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeLightbox(); });

/* Leistung wählen und zum Formular springen */
function selectService(type) {
  var sel = document.getElementById('anfrage-type');
  if (sel) sel.value = type;
  document.getElementById('kontakt').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/* Kontaktformular: öffnet das Mailprogramm mit vorausgefüllter Anfrage */
function sendForm(e) {
  e.preventDefault();
  var form = e.target;
  var d = new FormData(form);
  var sel = form.querySelector('select[name="type"]');
  var typ = sel && sel.value ? sel.options[sel.selectedIndex].text : 'Allgemein';
  var subject = 'Anfrage industrietaucher.ch: ' + typ;
  var body =
    'Auftraggeber: ' + d.get('name') + '\n' +
    'Kontakt: ' + d.get('contact') + '\n' +
    'Art: ' + typ + '\n' +
    'Ort / Gewässer: ' + (d.get('ort') || '') + '\n\n' +
    'Beschreibung:\n' + d.get('message');
  window.location.href = 'mailto:info@industrietaucher.ch?subject=' +
    encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  document.getElementById('form-ok').style.display = 'block';
}
