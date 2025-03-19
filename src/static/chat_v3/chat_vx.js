import { v4 as uuidv4 } from 'uuid';

document.addEventListener('DOMContentLoaded', () => {
    // Mock data (replace with actual user data and group data)
    const currentUser = "Имя Пользователя";
    let personalMessages = ["user1@example.com", "user2@example.com"];
    let groups = [{ id: "group1", name: "Группа 1", members: ["user1@example.com"] }];
    let currentChat = null;

    // DOM elements
    const currentUserElement = document.getElementById('current-user');
    const createGroupButton = document.getElementById('create-group-button');
    const personalMessagesList = document.getElementById('personal-messages-list');
    const groupsList = document.getElementById('groups-list');
    const chatList = document.querySelector('.chat-list');
    const chatWindow = document.querySelector('.chat-window');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const addGroupModal = document.getElementById('add-group-modal');
    const groupNameInput = document.getElementById('group-name');
    const groupMemberEmailInput = document.getElementById('group-member-email');
    const addMemberButton = document.getElementById('add-member-button');
    const createGroupConfirmButton = document.getElementById('create-group-confirm');
    const cancelGroupCreationButton = document.getElementById('cancel-group-creation');
    const messagesContainer = document.querySelector('.messages');

    let newGroupMembers = [];

    // Functions
    function displayCurrentUser() {
        return currentUser;
    }

    function displayPersonalMessages() {
        personalMessagesList.innerHTML = '';
        personalMessages.forEach(email => {
            const item = document.createElement('div');
            item.classList.add('chat-list-item');
            item.textContent = email;
            item.addEventListener('click', () => openChat(email, 'personal'));
            personalMessagesList.appendChild(item);
        });
    }

    function displayGroups() {
        groupsList.innerHTML = '';
        groups.forEach(group => {
            const item = document.createElement('div');
            item.classList.add('chat-list-item');
            item.textContent = group.name;
            item.addEventListener('click', () => openChat(group.id, 'group'));
            groupsList.appendChild(item);
        });
    }

    function openChat(chatId, type) {
        currentChat = { id: chatId, type: type };
        displayChat(chatId, type);
    }

    function displayChat(chatId, type) {
        messagesContainer.innerHTML = ''; // Clear previous messages
        const chatHeader = document.createElement('h2');
        messagesContainer.appendChild(chatHeader);

        if (type === 'personal') {
            chatHeader.textContent = `Чат с ${chatId}`;
            // Display chat messages for the selected user (fetch from server later)
            displayUserList(chatId);
        } else if (type === 'group') {
            const group = groups.find(g => g.id === chatId);
            if (group) {
                chatHeader.textContent = `Чат группы ${group.name}`;
                // Display chat messages for the selected group (fetch from server later)
                displayGroupInfo(group);
            }
        }
    }

    function displayUserList(user) {
      messagesContainer.innerHTML = '';
      const chatHeader = document.createElement('h2');
      chatHeader.textContent = `Чат с ${user}`;
      messagesContainer.appendChild(chatHeader);
    }

    function displayGroupInfo(group) {
      messagesContainer.innerHTML = '';
      const chatHeader = document.createElement('h2');
      chatHeader.textContent = `Чат группы ${group.name}`;
      messagesContainer.appendChild(chatHeader);
    }

    function sendMessage() {
        if (!currentChat) {
            alert('Выберите чат для отправки сообщения.');
            return;
        }

        const messageText = messageInput.value.trim();
        if (messageText === '') return;

        // Simulate sending message
        console.log(`Sending message "${messageText}" to chat ${currentChat.id} (${currentChat.type})`);
        messageInput.value = '';
    }

    function openCreateGroupModal() {
        addGroupModal.style.display = 'block';
        newGroupMembers = [];
    }

    function closeCreateGroupModal() {
        addGroupModal.style.display = 'none';
        groupNameInput.value = '';
        groupMemberEmailInput.value = '';
        newGroupMembers = [];
    }

    function addGroupMember() {
        const email = groupMemberEmailInput.value.trim();
        if (email !== '' && !newGroupMembers.includes(email)) {
            newGroupMembers.push(email);
            groupMemberEmailInput.value = '';
            alert(`Участник ${email} добавлен.`)
        }
    }

    function createGroup() {
        const groupName = groupNameInput.value.trim();
        if (groupName === '') {
            alert('Введите название группы.');
            return;
        }

        if (newGroupMembers.length === 0) {
            alert('Добавьте хотя бы одного участника в группу.');
            return;
        }

        const newGroupId = uuidv4();
        const newGroup = {
            id: newGroupId,
            name: groupName,
            members: newGroupMembers
        };

        groups.push(newGroup);
        displayGroups();
        closeCreateGroupModal();
    }

    // Event listeners
    createGroupButton.addEventListener('click', openCreateGroupModal);
    cancelGroupCreationButton.addEventListener('click', closeCreateGroupModal);
    addMemberButton.addEventListener('click', addGroupMember);
    createGroupConfirmButton.addEventListener('click', createGroup);
    sendButton.addEventListener('click', sendMessage);

    const favorites = document.getElementById('favorites');
    favorites.addEventListener('click', () => {
      openChat(displayCurrentUser(), 'personal')
    });

    // Initial display
    displayCurrentUser();
    displayPersonalMessages();
    displayGroups();
});