
const input = document.getElementById('nameInput');
const container = document.querySelector('.input-container');
const cancelBtn = document.getElementById('cancelBtn');
const confirmBtn = document.getElementById('confirmBtn');
const nameList = document.getElementById('nameList');

input.addEventListener('focus', () => {
  container.classList.add('focused');
});

input.addEventListener('blur', () => {
  setTimeout(() => {
    if (!container.contains(document.activeElement)) {
      container.classList.remove('focused');
    }
  }, 150);
});

cancelBtn.addEventListener('click', () => {
  input.value = '';
  input.focus();
});

confirmBtn.addEventListener('click', () => {
  const name = input.value.trim();
  if (name) {
    const li = document.createElement('li');

    const span = document.createElement('span');
    span.textContent = name;
    span.className = 'name-text';

    const delBtn = document.createElement('button');
    delBtn.textContent = '✕';
    delBtn.className = 'icon-button';
    delBtn.onclick = () => {
      li.remove();
    };

    li.appendChild(span);
    li.appendChild(delBtn);
    nameList.appendChild(li);

    input.value = '';
    input.blur();
    container.classList.remove('focused');
  }
});
