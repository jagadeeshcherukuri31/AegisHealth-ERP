(() => {
  const fields = (p = {}) => [
    { name: "first_name", label: "First name", required: true, value: p.first_name },
    { name: "last_name", label: "Last name", required: true, value: p.last_name },
    { name: "dob", label: "Date of birth", type: "date", required: true, value: p.dob },
    { name: "gender", label: "Gender", options: ["Female", "Male", "Other"], value: p.gender },
    { name: "phone", label: "Phone", value: p.phone },
    { name: "blood_group", label: "Blood group", value: p.blood_group },
    { name: "allergies", label: "Allergies", value: p.allergies },
    { name: "address", label: "Address", value: p.address },
  ];
  let all = [];
  Aegis.register("patients", {
    label: "Patients",
    roles: ["doctor", "nurse", "receptionist", "billing", "pharmacist"],
    async render(root) {
      root.innerHTML = UI.page("Patients", `<input id="q" type="search" placeholder="Search name, MRN, phone"><button class="btn primary" id="add">Register patient</button>`);
      const draw = async () => {
        all = await Api.get("/patients?q=" + encodeURIComponent($("#q").value));
        $("#body").innerHTML = UI.table(
          [{ key: "mrn", label: "MRN" }, { label: "Name", render: (p) => esc(p.first_name + " " + p.last_name) }, { key: "dob", label: "DOB" },
           { key: "phone", label: "Phone" }, { key: "blood_group", label: "Blood" }, { key: "allergies", label: "Allergies" }],
          all, (p) => `<button class="btn sm" data-edit="${p.id}">Edit</button>`);
      };
      $("#q").oninput = () => { clearTimeout(draw.t); draw.t = setTimeout(draw, 250); };
      $("#add").onclick = async () => {
        const v = await UI.form("Register patient", fields());
        if (v && (await UI.run(() => Api.post("/patients", v), "Patient registered"))) draw();
      };
      root.onclick = async (e) => {
        const id = e.target.dataset.edit; if (!id) return;
        const v = await UI.form("Edit patient", fields(all.find((p) => p.id == id)));
        if (v && (await UI.run(() => Api.put("/patients/" + id, v), "Patient updated"))) draw();
      };
      draw();
    },
  });
})();
