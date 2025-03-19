let selectedGroupId = null;
let groupSocket = null;

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

/////////////////////////////////////////////////////////////

// Функция создания группы
async function createGroup(name, participants) {
    try {
        const response = await fetch('/groups/create', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, participants})
        });

        if (response.ok) {
            alert('Группа создана успешно!');
            fetchGroups(); // Перезагружаем список групп после успешного создания
        } else {
            console.error('Ошибка при создании группы');
        }
    } catch (error) {
        console.error('Ошибка при выполнении запроса:', error);
    }
}

// Функция выбора группы
async function selectGroup(groupId, groupName, event) {
    selectedGroupId = groupId;
    document.getElementById('chatHeader').innerHTML = `<span>Чат с группой ${groupName}</span><button class="logout-button" id="logoutButton">Выход</button>`;
    document.getElementById('messageInput').disabled = false;
    document.getElementById('sendButton').disabled = false;

    document.querySelectorAll('.group-item').forEach(item => item.classList.remove('active'));
    event.target.classList.add('active');

    const messagesContainer = document.getElementById('messages');
    messagesContainer.innerHTML = '';
    messagesContainer.style.display = 'block';

    document.getElementById('logoutButton').onclick = logout;

    await loadGroupMessages(groupId);
    connectGroupWebSocket();
    startGroupMessagePolling(groupId);
}

// Загрузка сообщений группы
async function loadGroupMessages(groupId) {
    try {
        const response = await fetch(`/groups/messages/${groupId}`);
        const messages = await response.json();

        const messagesContainer = document.getElementById('messages');
        messagesContainer.innerHTML = messages.map(message =>
            createMessageElement(message.content, message.sender_id)
        ).join('');
    } catch (error) {
        console.error('Ошибка загрузки сообщений группы:', error);
    }
}

// Подключение WebSocket для группы
function connectGroupWebSocket() {
    if (groupSocket) groupSocket.close();

    groupSocket = new WebSocket(`wss://${window.location.host}/groups/ws/${selectedGroupId}`);

    groupSocket.onopen = () => console.log('WebSocket соединение для группы установлено');

    groupSocket.onmessage = (event) => {
        const incomingMessage = JSON.parse(event.data);
        if (incomingMessage.group_id === selectedGroupId) {
            addMessage(incomingMessage.content, incomingMessage.sender_id);
        }
    };

    groupSocket.onclose = () => console.log('WebSocket соединение для группы закрыто');
}

// // Отправка сообщения в группу
// async function sendGroupMessage() {
//     const messageInput = document.getElementById('messageInput');
//     const message = messageInput.value.trim();

//     if (message &&...


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
