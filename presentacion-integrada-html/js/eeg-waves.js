/* ============================================================
   eeg-waves.js — trazas EEG animadas, sintetizadas a partir de
   la potencia de banda REAL medida por fase (canal C3, µV²).
   Sin dependencias. Liviano, offline, respeta reduced-motion.
   ============================================================ */
(function () {
  "use strict";

  // Potencia absoluta de banda por fase (C3), de outputs/2026-06-11_eeg-resultados-mne_v3.json
  // Clave de scoring de la cátedra: 2 = S3, 3 = S4 (sin S2 separado, sin REM).
  var STAGES = {
    "Vigilia": { delta: 534.5, theta: 11.4, alpha: 18.8, sigma: 4.3,  beta: 19.8, color: "#8A8F9C" },
    "S1":      { delta: 57.0,  theta: 16.7, alpha: 7.1,  sigma: 2.6,  beta: 10.4, color: "#0E7C7B" },
    "S3":      { delta: 192.8, theta: 36.3, alpha: 11.5, sigma: 11.6, beta: 4.7,  color: "#4338CA" },
    "S4":      { delta: 840.2, theta: 43.3, alpha: 14.4, sigma: 5.0,  beta: 1.7,  color: "#312E81" }
  };
  // Frecuencia representativa por banda (Hz aproximado, usado para el nº de ciclos y la velocidad)
  var FREQ = { delta: 1.1, theta: 4, alpha: 7, sigma: 13, beta: 20 };

  // Presets de forma de onda para el diagrama de mecanismo (ondas lentas → husos → ripples)
  var PRESETS = {
    slow:    { cycles: 1.7, amp: 0.80, drift: 0.0016, env: null, color: "#312E81" },
    spindle: { cycles: 13,  amp: 0.66, drift: 0.0010, env: { pk: 2.0, pw: 6, speed: 0.0013 }, color: "#0E7C7B" },
    ripple:  { cycles: 27,  amp: 0.46, drift: 0.0009, env: { pk: 3.2, pw: 8, speed: 0.0018 }, color: "#4338CA" }
  };

  var REDUCED = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Normalización global de amplitud (raíz de la potencia ~ amplitud)
  var MAXAMP = 0;
  Object.keys(STAGES).forEach(function (k) {
    Object.keys(FREQ).forEach(function (b) { MAXAMP = Math.max(MAXAMP, Math.sqrt(STAGES[k][b])); });
  });

  function bandAmps(s) {
    var a = {};
    Object.keys(FREQ).forEach(function (b) { a[b] = Math.sqrt(s[b]) / MAXAMP; });
    return a;
  }

  function Wave(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.stage = canvas.getAttribute("data-eeg-stage") || "S3";
    this.mode = canvas.getAttribute("data-eeg-mode") || "trace";
    this.wave = canvas.getAttribute("data-eeg-wave");          // 'slow' | 'spindle' | 'ripple' | null
    this.preset = this.wave ? PRESETS[this.wave] : null;
    var s = STAGES[this.stage] || STAGES.S3;
    this.amps = bandAmps(s);
    this.color = canvas.getAttribute("data-eeg-color") || (this.preset ? this.preset.color : s.color);
    this.t = 0;
    this.running = false;
    this.raf = null;
    this.last = 0;
    this.resize();
    this.frame();   // frame estático inicial (necesario para export a PDF/PPTX)
  }

  Wave.prototype.resize = function () {
    var dpr = (window.devicePixelRatio || 1) * 1.4;
    var w = this.canvas.clientWidth || 600;
    var h = this.canvas.clientHeight || 110;
    this.canvas.width = Math.round(w * dpr);
    this.canvas.height = Math.round(h * dpr);
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    this.w = w; this.h = h;
  };

  Wave.prototype.framePreset = function () {
    var ctx = this.ctx, w = this.w, h = this.h, mid = h / 2, t = this.t, p = this.preset;
    ctx.clearRect(0, 0, w, h);
    ctx.lineJoin = "round";
    ctx.lineWidth = 2.0;
    ctx.strokeStyle = this.color;
    ctx.beginPath();
    for (var x = 0; x <= w; x += 1.5) {
      var u = x / w;
      var phase = 2 * Math.PI * p.cycles * u + t * p.cycles * p.drift;
      var amp = p.amp;
      if (p.env) {
        var e = Math.sin(2 * Math.PI * p.env.pk * u + t * p.env.speed);
        amp *= Math.pow(Math.max(0, e), p.env.pw);
      }
      var Y = mid - amp * Math.sin(phase) * (h * 0.34);
      if (x === 0) ctx.moveTo(x, Y); else ctx.lineTo(x, Y);
    }
    ctx.stroke();
  };

  Wave.prototype.frame = function () {
    if (this.preset) { this.framePreset(); return; }
    var ctx = this.ctx, w = this.w, h = this.h, mid = h / 2;
    ctx.clearRect(0, 0, w, h);
    ctx.lineJoin = "round";
    ctx.lineWidth = this.mode === "cover" ? 2.0 : 1.9;
    ctx.strokeStyle = this.color;
    ctx.globalAlpha = this.mode === "cover" ? 0.9 : 1;
    ctx.beginPath();

    var cyclesK = 2.6;           // ciclos de delta a lo ancho
    var step = 2;
    var amps = this.amps;
    var t = this.t;

    for (var x = 0; x <= w; x += step) {
      var u = x / w;
      var y = 0;
      for (var b in FREQ) {
        if (!FREQ.hasOwnProperty(b)) continue;
        var cyc = cyclesK * FREQ[b];
        // signo + en el término temporal: la onda se desplaza hacia la izquierda
        // (lo nuevo entra por la derecha, como un polisomnógrafo en vivo)
        var ph = 2 * Math.PI * cyc * u + t * FREQ[b] * 0.0016;
        var amp = amps[b];
        if (b === "sigma") {
          // envolvente de husos: ráfagas ocasionales (más visibles donde sigma es alta, p. ej. S3)
          var burst = Math.pow(Math.max(0, Math.sin(u * Math.PI * 3 + t * 0.0006)), 6);
          amp *= (0.35 + 1.9 * burst);
        }
        y += amp * Math.sin(ph);
      }
      var Y = mid - y * (h * 0.30);
      if (x === 0) ctx.moveTo(x, Y); else ctx.lineTo(x, Y);
    }
    ctx.stroke();
    ctx.globalAlpha = 1;
  };

  Wave.prototype.loop = function (now) {
    if (!this.running) return;
    if (!this.last) this.last = now;
    var dt = now - this.last;
    this.last = now;
    this.t += dt;
    this.frame();
    this.raf = requestAnimationFrame(this.loop.bind(this));
  };

  Wave.prototype.start = function () {
    this.resize();
    if (REDUCED) { this.t = 1200; this.frame(); return; }   // un solo frame estático
    if (this.running) return;
    this.running = true;
    this.last = 0;
    this.raf = requestAnimationFrame(this.loop.bind(this));
  };

  Wave.prototype.stop = function () {
    this.running = false;
    if (this.raf) cancelAnimationFrame(this.raf);
    this.raf = null;
  };

  var waves = [];

  function initAll() {
    var nodes = document.querySelectorAll("canvas[data-eeg-stage], canvas[data-eeg-mode], canvas[data-eeg-wave]");
    Array.prototype.forEach.call(nodes, function (c) {
      if (c._wave) { c._wave.resize(); c._wave.frame(); return; }
      var wv = new Wave(c);
      c._wave = wv;
      waves.push(wv);
    });
  }

  // Dibuja un frame estático en TODOS los canvas (para export a PDF/PPTX,
  // donde todas las diapositivas están visibles a la vez).
  function drawAllStatic() {
    waves.forEach(function (w) { w.resize(); w.frame(); });
  }

  function activate(section) {
    waves.forEach(function (w) {
      if (section && section.contains(w.canvas)) w.start();
      else w.stop();
    });
  }

  window.EEGWaves = { initAll: initAll, activate: activate, drawAllStatic: drawAllStatic, stages: STAGES };
})();
