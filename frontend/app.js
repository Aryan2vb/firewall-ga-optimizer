let ruleHitsChart = null;
let paretoChart = null;

async function loadResults() {
  try {
    const res = await fetch('/api/results');
    const data = await res.json();
    renderSummary(data);
    renderTables(data);
    renderRuleHitsChart(data);
    renderParetoChart(data);
  } catch (e) {
    console.error('Error loading results', e);
  }
}

function renderSummary(data) {
  const b = data.baseline;
  const g = data.ga_best;

  document.getElementById('baseline-avg-checks').textContent = b.avg_checks.toFixed(2);
  document.getElementById('ga-avg-checks').textContent = g.avg_checks.toFixed(2);
  document.getElementById('baseline-avg-time').textContent = b.avg_time.toExponential(2);
  document.getElementById('ga-avg-time').textContent = g.avg_time.toExponential(2);
}

function fillTable(tableId, rules) {
  const tbody = document.querySelector(`#${tableId} tbody`);
  tbody.innerHTML = '';
  rules
    .sort((a, b) => a.position - b.position)
    .forEach(r => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${r.position}</td>
        <td>${r.rule_id}</td>
        <td>${r.hit_count}</td>
        <td>${r.total_time.toFixed(4)}</td>
      `;
      tbody.appendChild(tr);
    });
}

function renderTables(data) {
  fillTable('baseline-table', data.baseline.per_rules);
  fillTable('ga-table', data.ga_best.per_rules);
}

function renderRuleHitsChart(data) {
  const labels = data.baseline.per_rules.map(r => r.rule_id);
  const baselineHits = data.baseline.per_rules.map(r => r.hit_count);
  const gaHits = data.ga_best.per_rules.map(r => r.hit_count);

  const ctx = document.getElementById('ruleHitsChart').getContext('2d');
  if (ruleHitsChart) ruleHitsChart.destroy();

  ruleHitsChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Baseline Hits',
          data: baselineHits,
          backgroundColor: 'rgba(244, 67, 54, 0.6)'
        },
        {
          label: 'GA Hits',
          data: gaHits,
          backgroundColor: 'rgba(76, 175, 80, 0.6)'
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        x: { stacked: false },
        y: { beginAtZero: true }
      }
    }
  });
}

function renderParetoChart(data) {
  const ctx = document.getElementById('paretoChart').getContext('2d');
  if (paretoChart) paretoChart.destroy();

  const baselinePoints = data.pareto.filter(p => p.is_baseline);
  const selectedPoints = data.pareto.filter(p => p.is_selected);
  const others = data.pareto.filter(p => !p.is_baseline && !p.is_selected);

  paretoChart = new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [
        {
          label: 'Other Solutions',
          data: others.map(p => ({ x: p.avg_checks, y: p.avg_time })),
          backgroundColor: 'rgba(158, 158, 158, 0.6)'
        },
        {
          label: 'Baseline',
          data: baselinePoints.map(p => ({ x: p.avg_checks, y: p.avg_time })),
          backgroundColor: 'rgba(244, 67, 54, 0.9)',
          pointRadius: 6
        },
        {
          label: 'Selected GA',
          data: selectedPoints.map(p => ({ x: p.avg_checks, y: p.avg_time })),
          backgroundColor: 'rgba(76, 175, 80, 0.9)',
          pointRadius: 6
        }
      ]
    },
    options: {
      scales: {
        x: {
          title: { display: true, text: 'Average Checks' }
        },
        y: {
          title: { display: true, text: 'Average Time' }
        }
      }
    }
  });
}

document.getElementById('refresh-btn').addEventListener('click', loadResults);

// auto-load once on page open
window.addEventListener('load', loadResults);
