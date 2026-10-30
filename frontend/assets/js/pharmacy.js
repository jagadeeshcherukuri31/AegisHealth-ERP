Aegis.register("pharmacy", {
  label: "Pharmacy",
  roles: ["pharmacist", "doctor", "nurse"],
  async render(root) {
    const manage = ["pharmacist", "admin"].includes(Aegis.user.role);
    root.innerHTML = UI.page("Pharmacy inventory", `<input id="q" type="search" placeholder="Search medicines">` + (manage ? `<button class="btn primary" id="add">Add medicine</button>` : ""));
    const draw = async () => {
      const rows = await Api.get("/pharmacy?q=" + encodeURIComponent($("#q").value));
      $("#body").innerHTML = UI.table(
        [{ key: "sku", label: "SKU" }, { key: "name", label: "Medicine" },
         { label: "Stock", render: (m) => esc(m.stock) + (m.low_stock ? ` <span class="badge warn">low</span>` : "") },
         { label: "Price", render: (m) => money(m.unit_price) }, { key: "expiry_date", label: "Expires" }],
        rows, manage && ((m) => `<button class="btn sm" data-d="${m.id}">Dispense</button> <button class="btn sm" data-r="${m.id}">Restock</button>`));
    };
    $("#q").oninput = () => { clearTimeout(draw.t); draw.t = setTimeout(draw, 250); };
    if (manage) {
      $("#add").onclick = async () => {
        const v = await UI.form("Add medicine", [{ name: "name", label: "Name", required: true }, { name: "sku", label: "SKU", required: true },
          { name: "stock", label: "Opening stock", type: "number", value: 0 }, { name: "reorder_level", label: "Reorder level", type: "number", value: 20 },
          { name: "unit_price", label: "Unit price", type: "number", step: "0.01" }, { name: "expiry_date", label: "Expiry date", type: "date" }]);
        if (v && (await UI.run(() => Api.post("/pharmacy", v), "Medicine added"))) draw();
      };
      root.onclick = async (e) => {
        const { d, r } = e.target.dataset; if (!d && !r) return;
        const v = await UI.form(d ? "Dispense" : "Restock", [{ name: "quantity", label: "Quantity", type: "number", value: 1, required: true }], d ? "Dispense" : "Restock");
        if (v && (await UI.run(() => Api.post(`/pharmacy/${d || r}/${d ? "dispense" : "restock"}`, { quantity: +v.quantity }), d ? "Dispensed" : "Stock updated"))) draw();
      };
    }
    draw();
  },
});
