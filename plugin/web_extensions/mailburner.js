// this script is inserted in all matching documents
// script to intercept email entry
// <input type=email> 

(function() {
    const emails = ['bob@mail.com',
		    '[shopping]',
		    '[spam]',
		    '[sport]',
		    'Select...',
		    'New...'
		   ];

  // Skapa popup-diven
  const popup = document.createElement('div');
  popup.className = 'email-popup';
  Object.assign(popup.style, {
    position: 'absolute',
    background: 'white',
    border: '1px solid #ccc',
    boxShadow: '2px 2px 6px rgba(0,0,0,0.2)',
    display: 'none',
    zIndex: 1000,
  });
  document.body.appendChild(popup);

  function attachToInput(input) {
    // Undvik dubbel-hookning
    if (input.dataset.emailPopupAttached) return;
    input.dataset.emailPopupAttached = 'true';

    input.addEventListener('focus', () => showPopupFor(input));
    input.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        showPopupFor(input);
        e.preventDefault();
      }
    });
  }

  function showPopupFor(input) {
      popup.innerHTML = '';
      emails.forEach(email => {
	  const div = document.createElement('div');
	  div.textContent = email;
	  Object.assign(div.style, {
              padding: '5px 10px',
              cursor: 'pointer'
	  });
	  div.addEventListener('mousedown', function() {
	      if (email.includes('@'))
		  input.value = email;
	      else if (email[0] == '[')
		  input.value = email.substr(1,email.length-2) + "@domain.com";
	      else
		  ;  // action
              hidePopup();
	  });
	  div.addEventListener('mouseover', () => div.style.backgroundColor = '#eee');
	  div.addEventListener('mouseout', () => div.style.backgroundColor = '');
	  popup.appendChild(div);
      });

    const rect = input.getBoundingClientRect();
    popup.style.left = rect.left + 'px';
    popup.style.top = rect.bottom + window.scrollY + 'px';
    popup.style.width = rect.width + 'px';
    popup.style.display = 'block';
  }

  function hidePopup() {
    popup.style.display = 'none';
  }

  // Initial setup för redan befintliga inputs
  document.querySelectorAll('input[type="email"]').forEach(attachToInput);

  // Övervaka DOM-förändringar
  const observer = new MutationObserver(mutations => {
    for (const mutation of mutations) {
      mutation.addedNodes.forEach(node => {
        if (node.nodeType !== 1) return; // Element nodes only
        if (node.matches && node.matches('input[type="email"]')) {
          attachToInput(node);
        } else {
          // Kolla om det finns inputs i det nya subtree:t
          node.querySelectorAll?.('input[type="email"]').forEach(attachToInput);
        }
      });
    }
  });

  observer.observe(document.body, { childList: true, subtree: true });

  // Klick utanför stänger popupen
  document.addEventListener('click', function(e) {
    if (!popup.contains(e.target) && e.target.type !== 'email') {
      hidePopup();
    }
  });
})();
