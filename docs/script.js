d3.csv("data/spot_price_2025-07-16.csv").then(data => {
  // Prepare data for the chart
  const labels = data.map(d => d.hour_range);
  const prices = data.map(d => +d.price_eur_per_kwh);

  // Create the line chart with Chart.js
  const ctx = document.getElementById("priceChart").getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [{
        label: "Price €/kWh",
        data: prices,
        borderColor: "rgb(75, 192, 192)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        fill: true,
        tension: 0.3,
        pointRadius: 4,
        pointHoverRadius: 6,
      }]
    },
    options: {
      scales: {
        x: {
          title: { display: true, text: "Hour Range" }
        },
        y: {
          title: { display: true, text: "Price €/kWh" },
          beginAtZero: true
        }
      },
      plugins: {
        legend: { display: true },
        tooltip: { mode: "index", intersect: false }
      },
      responsive: true,
      maintainAspectRatio: false
    }
  });

  // Render simplified table
  const container = document.getElementById("table-container");

  const table = document.createElement("table");
  table.style.borderCollapse = "collapse";
  table.style.width = "100%";

  // Table header
  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");
  ["Hour Range", "Price €/kWh"].forEach(text => {
    const th = document.createElement("th");
    th.textContent = text;
    th.style.border = "1px solid #ccc";
    th.style.padding = "8px";
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  // Table body
  const tbody = document.createElement("tbody");
  data.forEach(row => {
    const tr = document.createElement("tr");
    ["hour_range", "price_eur_per_kwh"].forEach(key => {
      const td = document.createElement("td");
      td.textContent = row[key];
      td.style.border = "1px solid #ccc";
      td.style.padding = "8px";
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);

  container.appendChild(table);
}).catch(err => {
  console.error("Failed to load CSV:", err);
});
