function deleteRow(button) {
  const item = button.closest('.burner-item');
  if (item) item.remove();
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

    li.innerHTML = `
      <div>
        <div class="alias-input">
          <span class="prefix">${conf.username}.</span>
          <input type="text" value="${entry.alias}" placeholder="alias" />
          <span class="suffix">@${conf.domain}</span>
        </div>
        <div class="label">BURNER ADDRESS</div>
      </div>
      <div>
        <div class="description-block">
          <input type="text" value="${entry.description}" />
          <button class="icon-button">✕</button>
          <button class="icon-button confirm">✔</button>
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
      <div class="delete-burn-wrap">
        <div class="delete-wrap">
          <button class="icon-button" onclick="deleteRow(this)" title="Delete">✕</button>
          <div class="label">DELETE</div>
        </div>
        <div class="burn-wrap">
          <img src="img/flaming_skull_icon.png" alt="burn icon" onclick="deleteRow(this)" style="cursor:pointer;" title="Burn" />
          <div class="label">BURN</div>
        </div>
      </div>
    `;

    list.appendChild(li);
  });
});