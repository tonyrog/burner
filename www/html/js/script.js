function deleteRow(button) {
  const item = button.closest('.burner-item');
  if (item) item.remove();
}

function enterEditMode(el) {
  const text = el.textContent;
  const container = el.closest('.description-container');
  container.innerHTML = `
    <div class="description-edit">
      <input type="text" value="${text}">
      <button class="icon-button cancel" title="Cancel">✕</button>
      <button class="icon-button confirm green" title="Save">✔</button>
    </div>
    <div class="label">DESCRIPTION</div>
  `;

  container.querySelector('.cancel').addEventListener('click', () => {
    container.innerHTML = `
      <div class="description-block">
        <div class="description-text" onclick="enterEditMode(this)">${text}</div>
      </div>
      <div class="label">DESCRIPTION</div>
    `;
  });

  container.querySelector('.confirm').addEventListener('click', () => {
    const newText = container.querySelector('input').value;
    container.innerHTML = `
      <div class="description-block">
        <div class="description-text" onclick="enterEditMode(this)">${newText}</div>
      </div>
      <div class="label">DESCRIPTION</div>
    `;
  });
}

document.addEventListener("DOMContentLoaded", () => {
  console.log("🔥 Script running");

  const data = JSON.parse(document.getElementById("burner-data").textContent);
  const conf = JSON.parse(document.getElementById("burner-config").textContent);
  const list = document.getElementById("burnerList");

  console.log("✅ Parsed data:", data);

  data.forEach(entry => {
    const li = document.createElement("li");
    li.className = "burner-item";

    const isOn = entry.block === false;

    li.innerHTML = `
      <div class="alias">
        <div class="alias-input">
          <span class="prefix">${conf.username}.</span>
          <input type="text" value="${entry.alias}" placeholder="alias">
          <span class="suffix">@${conf.domain}</span>
        </div>
        <div class="label">BURNER ADDRESS</div>
      </div>

      <div class="description-container" data-original="${entry.description}">
        <div class="description-block">
          <div class="description-text" onclick="enterEditMode(this)">${entry.description || "No description"}</div>
        </div>
        <div class="label">DESCRIPTION</div>
      </div>

      <div>
        <div class="value">${entry.date}</div>
        <div class="label">CREATED AT</div>
      </div>

      <div>
        <div class="value">${entry.forwarded}</div>
        <div class="label">FORWARDED</div>
      </div>

      <div>
        <div class="value">${entry.blocked}</div>
        <div class="label">BLOCKED</div>
      </div>

      <div class="toggle-wrap">
        <label class="switch">
          <input type="checkbox" ${isOn ? "checked" : ""} onchange="this.nextElementSibling.textContent = this.checked ? 'ON' : 'OFF'">
          <span class="slider"></span>
        </label>
        <div class="label">${isOn ? "ON" : "OFF"}</div>
      </div>

      <div class="burn-cell">
        <img src="img/flaming_skull_icon.png" alt="burn icon" class="burn-icon" title="Burn" onclick="deleteRow(this)">
        <div class="label">BURN</div>
      </div>
    `;

    list.appendChild(li);
  });
});