document.addEventListener('DOMContentLoaded', () => {
  const tabButtons = document.querySelectorAll('.tab-button');
  const tabContents = document.querySelectorAll('.tab-content');

  function activateTab(tabId) {
    tabContents.forEach(content => {
      content.classList.remove('active');
    });
    tabButtons.forEach(button => {
      button.classList.remove('active');
    });

    const tabContent = document.getElementById(tabId);
    const tabButton = document.querySelector(`.tab-button[data-tab="${tabId}"]`);

    if (tabContent && tabButton) {
      tabContent.classList.add('active');
      tabButton.classList.add('active');
    }
  }

  tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      const tabId = button.dataset.tab;
      activateTab(tabId);
    });
  });

  // обработка форм
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');
  const container = document.querySelector('.container');
  const chatContainer = document.getElementById('chat-container');

  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    //  Здесь будет логика для отправки данных на сервер для входа
    console.log('Login:', {
      email,
      password
    });

    // временно переключаем контейнеры для отображения чата
    container.style.display = 'none';
    chatContainer.style.display = 'flex';


    // todo: добавить логику сетевых запросов и отображения ошибок
  });

  registerForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const email = document.getElementById('register-email').value;
    const name = document.getElementById('register-name').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-confirm-password').value;

    if (password !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    // Здесь будет логика для отправки данных на сервер для регистрации
    console.log('Register:', {
      email,
      name,
      password
    });
    // todo: добавить логику сетевых запросов и отображения ошибок
  });

  // Logout button functionality
  const logoutButton = document.getElementById('logout-button');
  logoutButton.addEventListener('click', async () => {
    // todo: заменить на настоящий запрос
    console.log('Logout');
    // const response = await fetch('/auth/logout', {
    //   method: 'POST',
    // });

    // if (response.ok) {
    //   window.location.href = '/auth'; //  Переадресация на /auth
    // } else {
    //   alert('Logout failed');
    // }
    container.style.display = 'flex';
    chatContainer.style.display = 'none';
  });
});