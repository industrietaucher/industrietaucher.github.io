/* industrietaucher.ch · gemeinsames Script */

/* Farbmodus: Systemeinstellung, per Knopf übersteuerbar */
(function () {
  var btn = document.getElementById('themeToggle');
  if (!btn) return;
  btn.addEventListener('click', function () {
    var root = document.documentElement;
    var current = root.getAttribute('data-theme') ||
      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var next = current === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });
})();

/* Mobilmenü */
(function () {
  var burger = document.getElementById('burger');
  var menu = document.getElementById('menu');
  if (!burger || !menu) return;
  burger.addEventListener('click', function () {
    var open = menu.classList.toggle('open');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  menu.addEventListener('click', function (e) {
    if (e.target.closest('a')) menu.classList.remove('open');
  });
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

/* Kontaktformular: Auftragsart aus der URL übernehmen (?art=inspektion) */
(function () {
  var sel = document.getElementById('anfrage-type');
  if (!sel) return;
  var m = location.search.match(/[?&]art=([a-z-]+)/);
  if (m) sel.value = m[1];
})();

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
    'Ansprechperson: ' + (d.get('person') || '') + '\n' +
    'Kontakt: ' + d.get('contact') + '\n' +
    'Art: ' + typ + '\n' +
    'Ort / Gewässer: ' + (d.get('ort') || '') + '\n' +
    'Gewünschter Zeitraum: ' + (d.get('termin') || '') + '\n\n' +
    'Beschreibung:\n' + d.get('message');
  window.location.href = 'mailto:info@industrietaucher.ch?subject=' +
    encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  document.getElementById('form-ok').style.display = 'block';
}
