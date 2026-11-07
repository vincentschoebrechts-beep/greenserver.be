/* greenserver.be — questions de contrôle et QCM final de la formation SAP.
   Tout se passe dans le navigateur : rien n'est envoyé, rien n'est enregistré. */
(function () {
  "use strict";
  var BANK = window.SAP_Q || [];

  var TXT = {
    en: { right: "Right.", wrong: "Not quite.", answer_is: "The answer is:" },
    fr: { right: "Exact.", wrong: "Pas tout à fait.", answer_is: "La bonne réponse :" }
  };

  function shuffle(a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function el(tag, attrs, text) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (k === "class") e.className = attrs[k]; else e.setAttribute(k, attrs[k]);
    }
    if (text != null) e.textContent = text;
    return e;
  }

  var counter = 0;
  /* Construit une question. onAnswer(correct) est appelé au premier choix si immediate = true. */
  function renderQuestion(q, lang, opts) {
    opts = opts || {};
    var t = q[lang];
    var name = "q" + (++counter);
    var box = el("div", { "class": "q" });
    var fs = el("fieldset");
    var lg = el("legend");
    if (opts.label) lg.appendChild(el("span", { "class": "from" }, opts.label));
    lg.appendChild(document.createTextNode(t.q));
    fs.appendChild(lg);
    var order = shuffle([0, 1, 2, 3]);
    var labels = [];
    order.forEach(function (idx) {
      var lab = el("label");
      var inp = el("input", { type: "radio", name: name, value: String(idx) });
      lab.appendChild(inp);
      lab.appendChild(el("span", null, t.o[idx]));
      lab.dataset.idx = String(idx);
      fs.appendChild(lab);
      labels.push(lab);
    });
    var fb = el("p", { "class": "fb", "aria-live": "polite" });
    box.appendChild(fs);
    box.appendChild(fb);

    function reveal() {
      var chosen = fs.querySelector("input:checked");
      var ok = chosen && chosen.value === "0";
      labels.forEach(function (lab) {
        var i = lab.dataset.idx;
        lab.querySelector("input").disabled = true;
        if (i === "0") lab.classList.add("is-right");
        else if (chosen && chosen.value === i) lab.classList.add("is-wrong");
      });
      box.classList.add("locked");
      var L = opts.labels || TXT[lang];
      fb.textContent = "";
      var s = el("strong", { "class": ok ? "ok" : "ko" }, ok ? L.right : L.wrong);
      fb.appendChild(s);
      fb.appendChild(document.createTextNode(" " + (ok ? "" : L.answer_is + " " + t.o[0] + ". ") + t.e));
      return ok;
    }

    if (opts.immediate) {
      fs.addEventListener("change", function () { reveal(); });
    }
    return {
      node: box,
      answered: function () { return !!fs.querySelector("input:checked"); },
      reveal: reveal,
      onChange: function (fn) { fs.addEventListener("change", fn); }
    };
  }

  /* Questions de contrôle en fin de leçon */
  Array.prototype.forEach.call(document.querySelectorAll(".qcheck"), function (zone) {
    var lang = zone.dataset.lang || "en";
    zone.dataset.ids.split(",").forEach(function (id) {
      var q = BANK[Number(id)];
      if (q) zone.appendChild(renderQuestion(q, lang, { immediate: true }).node);
    });
  });

  /* QCM final : deux questions par leçon, tirées au hasard */
  var quiz = document.getElementById("quiz");
  if (quiz) {
    var lang = quiz.dataset.lang || "en";
    var L = JSON.parse(quiz.dataset.labels || "{}");

    var start = function () {
      quiz.textContent = "";
      var picked = [];
      for (var l = 1; l <= 10; l++) {
        var pool = BANK.filter(function (q) { return q.l === l; });
        picked = picked.concat(shuffle(pool).slice(0, 2));
      }
      picked = shuffle(picked);

      var scoreZone = el("div");
      quiz.appendChild(scoreZone);
      var items = picked.map(function (q, i) {
        var item = renderQuestion(q, lang, {
          label: (i + 1) + " / " + picked.length + " · " + L.from_lesson + " " + q.l,
          labels: L
        });
        quiz.appendChild(item.node);
        return item;
      });

      var bar = el("div", { "class": "quiz-bar" });
      var count = el("span", { "aria-live": "polite" });
      var submit = el("button", { type: "button", "class": "btn" }, L.submit);
      bar.appendChild(count);
      bar.appendChild(submit);
      quiz.appendChild(bar);
      var msg = el("p", { "class": "quiz-msg muted", "aria-live": "polite" });
      quiz.appendChild(msg);

      var update = function () {
        var n = items.filter(function (it) { return it.answered(); }).length;
        count.textContent = n + " / " + items.length + " " + L.answered;
      };
      items.forEach(function (it) { it.onChange(update); });
      update();

      submit.addEventListener("click", function () {
        var missing = items.filter(function (it) { return !it.answered(); }).length;
        if (missing) {
          msg.textContent = L.missing;
          var first = items.filter(function (it) { return !it.answered(); })[0];
          first.node.scrollIntoView({ behavior: "smooth", block: "center" });
          return;
        }
        var good = items.filter(function (it) { return it.reveal(); }).length;
        var box = el("div", { "class": "score-box", role: "status" });
        box.appendChild(el("strong", null, L.score));
        box.appendChild(el("span", { "class": "big" }, good + " / " + items.length));
        box.appendChild(el("p", null, good >= 14 ? L.pass : L.fail));
        var again = el("button", { type: "button", "class": "btn" }, L.again);
        again.addEventListener("click", function () { start(); quiz.scrollIntoView({ behavior: "smooth" }); });
        box.appendChild(again);
        scoreZone.appendChild(box);
        bar.remove();
        msg.remove();
        box.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    };
    start();
  }
})();
