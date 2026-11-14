/* Desenha os gráficos do Dashboard do PSM (docs/gestao/dashboard.md) com Chart.js.
   Os dados vêm do bloco <script id="psm-dados">, gerado por hooks/dashboard_psm.py.

   Cores: laranja para o realizado (ou o que aumentou), azul para o previsto,
   vermelho tracejado só para o limite de decisão. */
(function () {
  "use strict";
  var graficos = [];

  function paleta() {
    var escuro = document.body.getAttribute("data-md-color-scheme") === "slate";
    return {
      texto: escuro ? "#bcc5d2" : "#3d4654",
      forte: escuro ? "#edf0f5" : "#172332",
      grade: escuro ? "rgba(255,255,255,0.08)" : "rgba(23,35,50,0.08)",
      laranja: escuro ? "#ffac52" : "#e07000",
      azul: escuro ? "#7fb3ff" : "#1f5fa8",
      azulClaro: escuro ? "#3f6da8" : "#9cc0ea",
      limite: escuro ? "#ff8a80" : "#c62828"
    };
  }

  function num(v, casas) {
    if (v === null || v === undefined) return "—";
    return Number(v).toLocaleString("pt-BR", { minimumFractionDigits: casas, maximumFractionDigits: casas });
  }

  // Escreve o valor em cima (ou ao lado) de cada barra, como nos painéis de BI.
  var rotulosBarras = {
    id: "rotulosBarras",
    afterDatasetsDraw: function (chart, args, opts) {
      if (!opts || !opts.formato) return;
      var ctx = chart.ctx;
      ctx.save();
      ctx.fillStyle = opts.cor;
      ctx.font = "12px " + Chart.defaults.font.family;
      chart.data.datasets.forEach(function (ds, k) {
        if (ds.type === "line" || (opts.conjuntos && opts.conjuntos.indexOf(k) < 0)) return;
        chart.getDatasetMeta(k).data.forEach(function (barra, i) {
          var txt = opts.formato(ds.data[i], i);
          if (!txt) return;
          if (chart.options.indexAxis === "y") {
            ctx.textAlign = "left"; ctx.textBaseline = "middle";
            ctx.fillText(txt, barra.x + 6, barra.y);
          } else {
            ctx.textAlign = "center"; ctx.textBaseline = "bottom";
            ctx.fillText(txt, barra.x, Math.min(barra.y, barra.base) - 4);
          }
        });
      });
      ctx.restore();
    }
  };

  function opcoes(p, extra) {
    var o = {
      responsive: true,
      maintainAspectRatio: false,
      layout: { padding: { top: 20, right: 12 } },
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { position: "top", align: "end", labels: { color: p.texto, usePointStyle: true, boxHeight: 8,
          padding: 14, font: { size: 12 } } },
        tooltip: { callbacks: {} },
        rotulosBarras: { cor: p.texto }
      },
      scales: {
        x: { ticks: { color: p.texto, font: { size: 12 }, maxRotation: 0, autoSkip: false },
          grid: { display: false }, border: { display: false } },
        y: { beginAtZero: true, ticks: { color: p.texto, font: { size: 11 } }, grid: { color: p.grade },
          border: { display: false } }
      }
    };
    return Object.assign(o, extra || {});
  }

  function desenhar() {
    var bloco = document.getElementById("psm-dados");
    if (!bloco || typeof Chart === "undefined") return;
    graficos.forEach(function (g) { g.destroy(); });
    graficos = [];

    var d = JSON.parse(bloco.textContent);
    var p = paleta();
    var sprints = d.sprints;
    var rotulos = sprints.map(function (s) { return s.rotulo; });
    Chart.defaults.font.family = getComputedStyle(document.body).fontFamily;

    // 1. Estimado vs. real: barras do real, linha do estimado.
    var o1 = opcoes(p);
    o1.plugins.rotulosBarras.formato = function (v) { return v ? num(v, 1) + " h" : ""; };
    o1.plugins.rotulosBarras.conjuntos = [0];
    o1.plugins.tooltip.callbacks.label = function (c) { return c.dataset.label + ": " + num(c.raw, 1) + " h"; };
    o1.plugins.tooltip.callbacks.afterBody = function (itens) {
      var s = sprints[itens[0].dataIndex];
      return ["Razão real ÷ estimado: " + num(s.razao, 2) + " (limite " + num(d.limites.razao, 1) + ")",
              "Custo real: R$ " + num(s.custo, 2)];
    };
    graficos.push(new Chart(document.getElementById("psm-horas"), {
      data: {
        labels: rotulos,
        datasets: [
          { type: "bar", label: "Real", data: sprints.map(function (s) { return s.h_real; }),
            backgroundColor: p.laranja, borderRadius: 4, maxBarThickness: 48, order: 2 },
          { type: "line", label: "Estimado", data: sprints.map(function (s) { return s.h_est; }),
            borderColor: p.azul, backgroundColor: p.azul, borderWidth: 2.5, pointRadius: 5,
            tension: 0.35, order: 1 }
        ]
      },
      plugins: [rotulosBarras],
      options: o1
    }));

    // 2. Ponte: da linha de base às horas reais (barras flutuantes).
    var ponte = d.ponte || [];
    var acumulado = 0;
    var faixas = ponte.map(function (passo) {
      if (passo.tipo === "variacao") {
        var ini = acumulado;
        acumulado += passo.valor;
        return [ini, acumulado];
      }
      acumulado = passo.valor;
      return [0, passo.valor];
    });
    var cores = ponte.map(function (passo) {
      if (passo.tipo === "base") return p.azul;
      if (passo.tipo === "total") return p.forte;
      return passo.valor >= 0 ? p.laranja : p.azulClaro;
    });
    var o2 = opcoes(p, { interaction: { mode: "nearest", intersect: true } });
    o2.plugins.legend.display = false;
    o2.scales.x.ticks.autoSkip = false;
    o2.scales.x.ticks.maxRotation = 0;
    o2.plugins.rotulosBarras.formato = function (v, i) {
      var passo = ponte[i];
      var sinal = passo.tipo === "variacao" && passo.valor > 0 ? "+" : "";
      return sinal + num(passo.valor, 1) + " h";
    };
    o2.plugins.tooltip.callbacks.label = function (c) {
      var passo = ponte[c.dataIndex];
      if (passo.tipo === "variacao") {
        return (passo.valor >= 0 ? "Aumentou " : "Diminuiu ") + num(Math.abs(passo.valor), 1) + " h";
      }
      return num(passo.valor, 1) + " h (R$ " + num(passo.valor * d.custo_hora, 2) + ")";
    };
    graficos.push(new Chart(document.getElementById("psm-ponte"), {
      type: "bar",
      data: {
        labels: ponte.map(function (passo) { return passo.rotulo; }),
        datasets: [{ label: "Horas", data: faixas, backgroundColor: cores, borderRadius: 3, maxBarThickness: 56 }]
      },
      plugins: [rotulosBarras],
      options: o2
    }));

    // 3. Percentual de issues concluídas por sprint, com o limite de decisão.
    var comSprint = sprints.filter(function (s) { return s.nome !== "Sem sprint"; });
    var o3 = opcoes(p);
    o3.plugins.legend.display = false;
    o3.scales.y.max = 110;
    o3.scales.y.ticks.stepSize = 25;
    o3.scales.y.ticks.callback = function (v) { return v <= 100 ? v + "%" : ""; };
    o3.plugins.rotulosBarras.formato = function (v) { return num(v, 0) + "%"; };
    o3.plugins.rotulosBarras.conjuntos = [0];
    o3.plugins.tooltip.callbacks.label = function (c) {
      if (c.datasetIndex === 1) return "Limite: " + num(c.raw, 0) + "%";
      var s = comSprint[c.dataIndex];
      return "Concluídas: " + s.concluidas + " de " + s.planejadas + (s.andamento ? " (em andamento)" : "");
    };
    graficos.push(new Chart(document.getElementById("psm-progresso"), {
      data: {
        labels: comSprint.map(function (s) { return s.rotulo; }),
        datasets: [
          { type: "bar", label: "Concluídas", data: comSprint.map(function (s) { return s.pct; }),
            backgroundColor: comSprint.map(function (s) { return s.andamento ? p.azulClaro : p.laranja; }),
            borderRadius: 4, maxBarThickness: 48, order: 2 },
          { type: "line", label: "Limite (" + num(d.limites.concluido, 0) + "%)",
            data: comSprint.map(function () { return d.limites.concluido; }), borderColor: p.limite,
            borderDash: [6, 5], borderWidth: 2, pointRadius: 0, order: 1 }
        ]
      },
      plugins: [rotulosBarras],
      options: o3
    }));

    // 4. Ranking das issues que mais demoraram na entrega em foco.
    var ranking = d.issues.filter(function (i) { return i.entrega === d.foco; })
      .sort(function (a, b) { return b.dias - a.dias; }).slice(0, 10);
    var o4 = opcoes(p, { indexAxis: "y", interaction: { mode: "nearest", axis: "y", intersect: false } });
    o4.layout.padding.right = 48;
    o4.layout.padding.left = 4;
    o4.plugins.legend.display = false;
    o4.scales.x.grid = { color: p.grade };
    o4.scales.x.beginAtZero = true;
    o4.scales.y = { ticks: { color: p.texto, font: { size: 12 } }, grid: { display: false }, border: { display: false } };
    o4.plugins.rotulosBarras.formato = function (v) { return num(v, 1) + " d"; };
    o4.plugins.tooltip.callbacks.title = function (itens) {
      var i = ranking[itens[0].dataIndex];
      return "#" + i.numero + " · " + i.sprint;
    };
    o4.plugins.tooltip.callbacks.label = function (c) {
      var i = ranking[c.dataIndex];
      return [i.titulo, num(i.dias, 1) + " dia(s), " + (i.situacao === "acima" ? "acima da faixa" : "dentro da faixa")];
    };
    graficos.push(new Chart(document.getElementById("psm-ranking"), {
      type: "bar",
      data: {
        labels: ranking.map(function (i) {
          var t = i.titulo.length > 22 ? i.titulo.slice(0, 21) + "…" : i.titulo;
          return "#" + i.numero + " " + t;
        }),
        datasets: [{ label: "Dias", data: ranking.map(function (i) { return i.dias; }),
          backgroundColor: ranking.map(function (i) { return i.situacao === "acima" ? p.laranja : p.azul; }),
          borderRadius: 3, maxBarThickness: 22 }]
      },
      plugins: [rotulosBarras],
      options: o4
    }));
  }

  function iniciar() {
    desenhar();
    new MutationObserver(desenhar).observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(iniciar);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciar);
  } else {
    iniciar();
  }
})();