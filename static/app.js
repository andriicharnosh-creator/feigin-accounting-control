const labels = {
  receivable: "Należność",
  payable: "Zobowiązanie",
  missing_material: "Brakujący materiał",
};

const money = (amount, currency) => new Intl.NumberFormat("pl-PL", { maximumFractionDigits: 2 }).format(amount) + " " + currency;

function entityCard(entity) {
  const currencies = Object.entries(entity.currency_totals).map(([currency, totals]) => `
    <div class="currency-block">
      <span class="currency">${currency}</span>
      <dl>
        <div><dt>Należności</dt><dd>${money(totals.receivable, currency)}</dd></div>
        <div><dt>Zobowiązania</dt><dd>${money(totals.payable, currency)}</dd></div>
        <div><dt>Braki</dt><dd>${totals.missing_materials}</dd></div>
      </dl>
    </div>`).join("");
  return `<article class="entity-card"><div class="card-top"><span class="marker"></span><h2>${entity.entity}</h2><span class="count">${entity.records} wpisy</span></div>${currencies}</article>`;
}

function recordRow(record) {
  const verificationClass = record.verification_status.includes("requires") ? "warning" : "synthetic";
  return `<tr><td><strong>${record.id}</strong><span>${record.entity}</span><small>${record.note}</small></td><td>${labels[record.kind]}<span>${record.document_type}</span></td><td>${record.amount ? money(record.amount, record.currency) : "—"}</td><td><span class="pill">${record.payment_status}</span></td><td><span class="pill ${verificationClass}">${record.verification_status}</span><span class="source">źródło: ${record.source}</span></td></tr>`;
}

fetch("/api/summary").then((response) => response.json()).then((summary) => {
  document.querySelector("#entities").innerHTML = summary.entities.map(entityCard).join("");
  document.querySelector("#records").innerHTML = summary.records.map(recordRow).join("");
  document.querySelector("#currency-note").textContent = summary.currency_note;
});