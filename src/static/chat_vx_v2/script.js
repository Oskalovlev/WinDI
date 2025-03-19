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

            const groupNameSpan = document.createElement('span');
            groupNameSpan.textContent = group.name;
            item.appendChild(groupNameSpan);
            
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
        
        if (type === 'personal') {
            displayUserList(chatId);
        } else if (type === 'group') {
            const group = groups.find(g => g.id === chatId);
            if (group) {
                displayGroupInfo(group);
            }
        }
    }

    function displayUserList(user) {
      messagesContainer.innerHTML = '';
      const chatHeader = document.createElement('div');
      chatHeader.style.display = 'flex';
      chatHeader.style.justifyContent = 'space-between';
      chatHeader.style.alignItems = 'center';

      const chatTitle = document.createElement('h2');
      chatTitle.textContent = `Чат с ${user}`;
      chatHeader.appendChild(chatTitle);

      messagesContainer.appendChild(chatHeader);
    }

    function displayGroupInfo(group) {
        messagesContainer.innerHTML = '';
        const chatHeader = document.createElement('div');
        chatHeader.style.display = 'flex';
        chatHeader.style.justifyContent = 'space-between';
        chatHeader.style.alignItems = 'center';

        const chatTitle = document.createElement('h2');
        chatTitle.textContent = `Чат группы ${group.name}`;
        chatHeader.appendChild(chatTitle);

        const addMemberButton = document.createElement('button');
        addMemberButton.textContent = '+';
        addMemberButton.addEventListener('click', (event) => {
            event.stopPropagation(); // Prevent opening the chat
            openAddMemberModal(group.id);
        });
        chatHeader.appendChild(addMemberButton);

        messagesContainer.appendChild(chatHeader);

        // Display group members
        const membersList = document.createElement('ul');
        membersList.textContent = 'Участники:'; // Added title for clarity
        group.members.forEach(member => {
            const memberItem = document.createElement('li');
            memberItem.textContent = member;
            membersList.appendChild(memberItem);
        });
        messagesContainer.appendChild(membersList);
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
        // Ensure email input is present, and clear group member list
        groupMemberEmailInput.style.display = 'none';
        addMemberButton.style.display = 'none';
        newGroupMembers = [];
    }

    function closeCreateGroupModal() {
        addGroupModal.style.display = 'none';
        groupNameInput.value = '';
        groupMemberEmailInput.value = '';
        newGroupMembers = [];
        // Reset email input visibility
        groupMemberEmailInput.style.display = 'block';
        addMemberButton.style.display = 'block';
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

        const newGroupId = uuidv4();
        const newGroup = {
            id: newGroupId,
            name: groupName,
            members: [] // groupMembers
        };

        groups.push(newGroup);
        displayGroups();
        closeCreateGroupModal();
    }

    function openAddMemberModal(groupId) {
      const modal = document.createElement('div');
      modal.style.position = 'fixed';
      modal.style.top = '0';
      modal.style.left = '0';
      modal.style.width = '100%';
      modal.style.height = '100%';
      modal.style.backgroundColor = 'rgba(0,0,0,0.5)';
      modal.style.display = 'flex';
      modal.style.justifyContent = 'center';
      modal.style.alignItems = 'center';
      modal.innerHTML = `
          <div style="background-color: white; padding: 20px; border-radius: 5px; text-align: center;">
              <h2>Добавить участника в группу</h2>
              <input type="email" id="new-member-email" placeholder="Email участника" style="margin-bottom: 10px; padding: 8px; width: 200px;">
              <button id="add-new-member-button" style="padding: 8px 12px; background-color: #4CAF50; color: white; border: none; cursor: pointer;">Добавить</button>
              <button id="cancel-add-member-button" style="padding: 8px 12px; background-color: #ddd; border: none; cursor: pointer;">Отмена</button>
          </div>
      `;
      document.body.appendChild(modal);

      const addNewMemberButton = modal.querySelector('#add-new-member-button');
      const cancelAddMemberButton = modal.querySelector('#cancel-add-member-button');
      const newMemberEmailInput = modal.querySelector('#new-member-email');

      addNewMemberButton.addEventListener('click', () => {
          const email = newMemberEmailInput.value.trim();
          if (email !== '') {
              const groupIndex = groups.findIndex(group => group.id === groupId);
              if (groupIndex !== -1) {
                  if (!groups[groupIndex].members.includes(email)) {
                      groups[groupIndex].members.push(email);
                      displayGroups();
                  }
              }
              modal.remove();
          }
      });

      cancelAddMemberButton.addEventListener('click', () => {
          modal.remove();
      });
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