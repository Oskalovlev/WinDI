// Сохраняем текущий выбранный userId и WebSocket соединение
let selectedUserId = null;
let socket = null;
let messagePollingInterval = null;

// Функция выхода из аккаунта
async function logout() {
    try {
        const response = await fetch('/auth/logout', {
            method: 'POST',
            credentials: 'include'
        });

        if (response.ok) {
            window.location.href = '/auth';
        } else {
            console.error('Ошибка при выходе');
        }
    } catch (error) {
        console.error('Ошибка при выполнении запроса:', error);
    }
}

// async function createGroup(params) {
//     // Modal functionality
//     createGroupBtn.addEventListener('click', () => {
//         modal.style.display = 'block';
//     });

//     closeButton.addEventListener('click', () => {
//         modal.style.display = 'none';
//         clearGroupModal();
//     });

//     window.addEventListener('click', (event) => {
//         if (event.target == modal) {
//             modal.style.display = 'none';
//             clearGroupModal();
//         }
//     });

//     addMemberBtn.addEventListener('click', () => {
//         const email = inviteEmailInput.value;
//         if (email && !groupMembers.includes(email)) {
//             groupMembers.push(email);
//             const li = document.createElement('li');
//             li.textContent = email;
//             groupMembersList.appendChild(li);
//             inviteEmailInput.value = '';
//         }
//     });

//     createGroupConfirmBtn.addEventListener('click', () => {
//         const groupName = groupNameInput.value;
//         if (groupName && groupMembers.length > 0) {
//             socket.emit('createGroup', { name: groupName, members: groupMembers });
//             modal.style.display = 'none';
//             clearGroupModal();
//         } else {
//             alert('Введите название группы и добавьте участников.');
//         }
//     });

//     function clearGroupModal() {
//         groupNameInput.value = '';
//         inviteEmailInput.value = '';
//         groupMembers = [];
//         groupMembersList.innerHTML = '';
//     }

//     // Обновление списка пользователей
//     socket.on('users', (users) => {
//         usersList.innerHTML = '';
//         users.forEach(user => {
//             const li = document.createElement('li');
//             li.textContent = user.username;
//             li.addEventListener('click', () => {
//                 selectedChat = { type: 'user', id: user.id, name: user.username };
//                 chatTitle.textContent = `Чат с ${user.username}`;
//                 loadMessages(selectedChat);
//             });
//             usersList.appendChild(li);
//         });
//     });

//     // Обновление списка групп
//     socket.on('groups', (groups) => {
//         groupsList.innerHTML = '';
//         groups.forEach(group => {
//             const li = document.createElement('li');
//             li.textContent = group.name;
//             li.addEventListener('click', () => {
//                 selectedChat = { type: 'group', id: group.id, name: group.name };
//                 chatTitle.textContent = `Чат группы ${group.name}`;
//                 loadMessages(selectedChat);
//             });
//             groupsList.appendChild(li);
//         });
//     });
// }

// Создание новой группы

async function createGroup(groupTitle) {
    try {
        const response = await fetch('/groups', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: groupTitle })
        });

        if (!response.ok) throw new Error('Не удалось создать группу.');
        
        const data = await response.json();
        console.log(`Группа создана: ${data.id}`);
        return data.id;
    } catch (error) {
        console.error('Ошибка при создании группы:', error);
    }
}

// Добавление участника в группу
async function addMemberToGroup(groupId, userId) {
    try {
        const response = await fetch(`/groups/${groupId}/members`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId })
        });

        if (!response.ok) throw new Error('Не удалось добавить участника в группу.');
        
        console.log(`Участник добавлен в группу: ${groupId}`);
    } catch (error) {
        console.error('Ошибка при добавлении участника в группу:', error);
    }
}

// Отправка сообщения в группе
async function sendGroupMessage(groupId, message) {
    try {
        const payload = { group_id: groupId, content: message };
        const response = await fetch('/group-messages', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('Не удалось отправить сообщение.');
        
        const data = await response.json();
        console.log(`Сообщение отправлено в группу: ${groupId}`);
        return data.message_id;
    } catch (error) {
        console.error('Ошибка при отправке сообщения в группу:', error);
    }
}

// Получение сообщений группы
async function getGroupMessages(groupId) {
    try {
        const response = await fetch(`/group-messages?group_id=${groupId}`);
        const messages = await response.json();

        const messagesContainer = document.getElementById('messages');
        messagesContainer.innerHTML = messages.map(message =>
            createMessageElement(message.content, message.sender_id)
        ).join('');
    } catch (error) {
        console.error('Ошибка получения сообщений группы:', error);
    }
}

// Функция выбора пользователя
async function selectUser(userId, userName, event) {
    selectedUserId = userId;
    document.getElementById('chatHeader').innerHTML = `<span>Чат с ${userName}</span><button class="logout-button" id="logoutButton">Выход</button>`;
    document.getElementById('messageInput').disabled = false;
    document.getElementById('sendButton').disabled = false;

    document.querySelectorAll('.user-item').forEach(item => item.classList.remove('active'));
    event.target.classList.add('active');

    const messagesContainer = document.getElementById('messages');
    messagesContainer.innerHTML = '';
    messagesContainer.style.display = 'block';

    document.getElementById('logoutButton').onclick = logout;

    await loadMessages(userId);
    connectWebSocket();
    startMessagePolling(userId);
}

// Загрузка сообщений
async function loadMessages(userId) {
    try {
        const response = await fetch(`/chat/messages/${userId}`);
        const messages = await response.json();

        const messagesContainer = document.getElementById('messages');
        messagesContainer.innerHTML = messages.map(message =>
            createMessageElement(message.content, message.recipient_id)
        ).join('');
    } catch (error) {
        console.error('Ошибка загрузки сообщений:', error);
    }
}

// Подключение WebSocket
function connectWebSocket() {
    if (socket) socket.close();

    socket = new WebSocket(`wss://${window.location.host}/chat/ws/${selectedUserId}`);

    socket.onopen = () => console.log('WebSocket соединение установлено');

    socket.onmessage = (event) => {
        const incomingMessage = JSON.parse(event.data);
        if (incomingMessage.recipient_id === selectedUserId) {
            addMessage(incomingMessage.content, incomingMessage.recipient_id);
        }
    };

    socket.onclose = () => console.log('WebSocket соединение закрыто');
}

// Отправка сообщения
async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();

    if (message && selectedUserId) {
        const payload = {recipient_id: selectedUserId, content: message};

        try {
            await fetch('/chat/messages', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });

            socket.send(JSON.stringify(payload));
            addMessage(message, selectedUserId);
            messageInput.value = '';
        } catch (error) {
            console.error('Ошибка при отправке сообщения:', error);
        }
    }
}

// Добавление сообщения в чат
function addMessage(text, recipient_id) {
    const messagesContainer = document.getElementById('messages');
    messagesContainer.insertAdjacentHTML('beforeend', createMessageElement(text, recipient_id));
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Создание HTML элемента сообщения
function createMessageElement(text, recipient_id) {
    const userID = parseInt(selectedUserId, 10);
    const messageClass = userID === recipient_id ? 'my-message' : 'other-message';
    return `<div class="message ${messageClass}">${text}</div>`;
}

// Запуск опроса новых сообщений
function startMessagePolling(userId) {
    clearInterval(messagePollingInterval);
    messagePollingInterval = setInterval(() => loadMessages(userId), 1000);
}

// Обработка нажатий на пользователя
function addUserClickListeners() {
    document.querySelectorAll('.user-item').forEach(item => {
        item.onclick = event => selectUser(item.getAttribute('data-user-id'), item.textContent, event);
    });
}

// Первоначальная настройка событий нажатия на пользователей
addUserClickListeners();

// Обновление списка пользователей
async function fetchUsers() {
    try {
        const response_users = await fetch('/auth/users');
        const response_groups = await fetch('/auth/grops');
        const users = await response_users.json();
        const groups = await response_groups.json();
        const userList = document.getElementById('userList');
        const groupList = document.getElementById('userList');

        // Очищаем текущий список пользователей
        userList.innerHTML = '';

        // Создаем элемент "Избранное" для текущего пользователя
        const favoriteElement = document.createElement('div');
        favoriteElement.classList.add('favorite');
        favoriteElement.setAttribute('data-user-id', currentUserId);
        favoriteElement.textContent = 'Избранное';

        // Добавляем "Избранное" в начало списка
        userList.appendChild(favoriteElement);

        // Генерация списка остальных пользователей
        users.forEach(user => {
            if (user.id !== currentUserId) {
                const userElement = document.createElement('div');
                userElement.classList.add('user-item');
                userElement.setAttribute('data-user-id', user.id);
                userElement.textContent = user.name;
                userList.appendChild(userElement);
            }
        });

        // Очищаем текущий список групп
        groupList.innerHTML = '';

        // Генерация списка групп
        groups.forEach(group => {
            if (user.id !== currentUserId) {
                const groupElement = document.createElement('div');
                groupElement.classList.add('user-item');
                groupElement.setAttribute('data-user-id', user.id);
                groupElement.textContent = group.title;
                groupList.appendChild(groupElement);
            }
        });

        // Повторно добавляем обработчики событий для каждого пользователя
        addUserClickListeners();
    } catch (error) {
        console.error('Ошибка при загрузке списка пользователей:', error);
    }
}


document.addEventListener('DOMContentLoaded', fetchUsers);
setInterval(fetchUsers, 10000); // Обновление каждые 10 секунд

// Обработчики для кнопки отправки и ввода сообщения
document.getElementById('sendButton').onclick = sendMessage;

document.getElementById('messageInput').onkeypress = async (e) => {
    if (e.key === 'Enter') {
        await sendMessage();
    }
};