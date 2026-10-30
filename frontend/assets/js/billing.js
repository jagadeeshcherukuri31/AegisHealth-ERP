Aegis.register("billing", {
  label: "Billing",
  roles: ["billing", "receptionist"],
  async render(root) {
    root.innerHTML = UI.page("Billing", `<select id="st"><option value="">All invoices</option><option>unpaid</option><option>partial</option><option>paid</option></select><button class="btn primary" id="add">New invoice</button>`);
    const draw = async () => {
      const rows = await Api.get("/billing?status=" + $("#st").value);
      $("#body").innerHTML = UI.table(
        [{ label: "Invoice", render: (i) => "#" + i.id }, { key: "patient_name", label: "Patient" }, { key: "created_at", label: "Date", render: (i) => fmtDT(i.created_at) },
         { label: "Items", render: (i) => esc(i.items.map((x) => x.description).join(", ")) }, { label: "Total", render: (i) => money(i.total) },
         { label: "Balance", render: (i) => money(i.balance) }, { label: "Status", render: (i) => UI.badge(i.status) }],
        rows, (i) => (i.status === "paid" ? "" : `<button class="btn sm" data-pay="${i.id}" data-bal="${i.balance}">Record payment</button>`));
    };
    $("#st").onchange = draw;
    $("#add").onclick = async () => {
      const patients = await Api.get("/patients");
      const v = await UI.form("New invoice", [
        { name: "patient_id", label: "Patient", options: patients.map((p) => [p.id, `${p.first_name} ${p.last_name}`]) },
        { name: "description", label: "Service / item", required: true },
        { name: "quantity", label: "Quantity", type: "number", value: 1 },
        { name: "unit_price", label: "Unit price", type: "number", step: "0.01", required: true }], "Create invoice");
      if (!v) return;
      const body = { patient_id: +v.patient_id, items: [{ description: v.description, quantity: +v.quantity, unit_price: +v.unit_price }] };
      if (await UI.run(() => Api.post("/billing", body), "Invoice created")) draw();
    };
    root.onclick = async (e) => {
      const id = e.target.dataset.pay; if (!id) return;
      const v = await UI.form("Record payment", [{ name: "amount", label: "Amount", type: "number", step: "0.01", value: e.target.dataset.bal, required: true }], "Record payment");
      if (v && (await UI.run(() => Api.post(`/billing/${id}/pay`, { amount: +v.amount }), "Payment recorded"))) draw();
    };
    draw();
  },
});
