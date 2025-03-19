import { io } from "socket.io-client";

document.addEventListener('DOMContentLoaded', () => {
    const socket = io('http://localhost:3000'); // Укажите адрес вашего сервера

    const usersList = document.getElementById('users');
    const groupsList = document.getElementById('groups');
    const createGroupBtn = document.getElementById('create-group-btn');
    const modal = document.getElementById('modal');
    const closeButton = document.querySelector('.close-button');
    const createGroupConfirmBtn = document.getElementById('create-group-confirm-btn');
    const groupNameInput = document.getElementById('group-name');
    const inviteEmailInput = document.getElementById('invite-email');
    const addMemberBtn = document.getElementById('add-member-btn');
    const groupMembersList = document.getElementById('group-members-list');
    const chatTitle = document.getElementById('chat-title');
    const messageArea = document.getElementById('message-area');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    let selectedChat = null;
    let groupMembers = [];

    // Modal functionality
    createGroupBtn.addEventListener('click', () => {
        modal.style.display = 'block';
    });

    closeButton.addEventListener('click', () => {
        modal.style.display = 'none';
        clearGroupModal();
    });

    window.addEventListener('click', (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
            clearGroupModal();
        }
    });

    addMemberBtn.addEventListener('click', () => {
        const email = inviteEmailInput.value;
        if (email && !groupMembers.includes(email)) {
            groupMembers.push(email);
            const li = document.createElement('li');
            li.textContent = email;
            groupMembersList.appendChild(li);
            inviteEmailInput.value = '';
        }
    });

    createGroupConfirmBtn.addEventListener('click', () => {
        const groupName = groupNameInput.value;
        if (groupName && groupMembers.length > 0) {
            socket.emit('createGroup', { name: groupName, members: groupMembers });
            modal.style.display = 'none';
            clearGroupModal();
        } else {
            alert('Введите название группы и добавьте участников.');
        }
    });

    function clearGroupModal() {
        groupNameInput.value = '';
        inviteEmailInput.value = '';
        groupMembers = [];
        groupMembersList.innerHTML = '';
    }


    // Обновление списка пользователей
    socket.on('users', (users) => {
        usersList.innerHTML = '';
        users.forEach(user => {
            const li = document.createElement('li');
            li.textContent = user.username;
            li.addEventListener('click', () => {
                selectedChat = { type: 'user', id: user.id, name: user.username };
                chatTitle.textContent = `Чат с ${user.username}`;
                loadMessages(selectedChat);
            });
            usersList.appendChild(li);
        });
    });

    // Обновление списка групп
    socket.on('groups', (groups) => {
        groupsList.innerHTML = '';
        groups.forEach(group => {
            const li = document.createElement('li');
            li.textContent = group.name;
            li.addEventListener('click', () => {
                selectedChat = { type: 'group', id: group.id, name: group.name };
                chatTitle.textContent = `Чат группы ${group.name}`;
                loadMessages(selectedChat);
            });
            groupsList.appendChild(li);
        });
    });


    // Sending messages
    sendButton.addEventListener('click', () => {
        const message = messageInput.value;
        if (message && selectedChat) {
            socket.emit('sendMessage', {
                to: selectedChat.id,
                type: selectedChat.type,
                message: message
            });
            messageInput.value = '';
        }
    });

    // Receiving messages
    socket.on('newMessage', (message) => {
        if (selectedChat && ((message.sender === selectedChat.id && message.type === 'user') ||
                             (message.group === selectedChat.id && message.type === 'group'))) {
            displayMessage(message);
        }
    });


    function loadMessages(chat) {
        messageArea.innerHTML = ''; // Clear existing messages
        socket.emit('getMessages', { to: chat.id, type: chat.type });
    }

    socket.on('messages', (messages) => {
        messages.forEach(message => {
            displayMessage(message);
        });
    });


    function displayMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.textContent = `${message.sender}: ${message.message}`;
        messageArea.appendChild(messageElement);
        messageArea.scrollTop = messageArea.scrollHeight; // Scroll to bottom
    }
});

