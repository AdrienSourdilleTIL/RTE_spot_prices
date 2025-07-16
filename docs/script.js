// Load CSV and render a simple table
d3.csv("data/spot_price_2025-07-16.csv").then(data => {
  const container = document.getElementById("table-container");
  
  const table = document.createElement("table");
  table.style.borderCollapse = "collapse";
  table.style.width = "100%";

  // Header
  const headers = Object.keys(data[0]);
  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");
  headers.forEach(h => {
    const th = document.createElement("th");
    th.textContent = h;
    th.style.border = "1px solid #ccc";
    th.style.padding = "8px";
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  // Body
  const tbody = document.createElement("tbody");
  data.forEach(row => {
    const tr = document.createElement("tr");
    headers.forEach(h => {
      const td = document.createElement("td");
      td.textContent = row[h];
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
