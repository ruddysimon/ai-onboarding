$(document).ready(function () {
  const chatForm = document.getElementById('chat-form');
  const chatMessages = document.getElementById('chat-messages');
  const userInput = document.getElementById('user-input');

  chatForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const userMessage = userInput.value.trim();
    if (userMessage === '') return;

    const messageContainer = document.createElement('div');
    messageContainer.classList.add('message');
    messageContainer.classList.add('user-message');
    const messageText = document.createElement('p');
    messageText.textContent = userMessage;
    messageContainer.appendChild(messageText);
    chatMessages.appendChild(messageContainer);

    userInput.value = '';

    fetch('/chatbot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt: userMessage }),
    })
      .then((response) => response.json())
      .then((data) => {
        const botMessage = data.response;

        const messageContainer = document.createElement('div');
        messageContainer.classList.add('message');
        messageContainer.classList.add('bot-message');
        const messageText = document.createElement('p');
        messageText.textContent = botMessage;
        messageContainer.appendChild(messageText);
        chatMessages.appendChild(messageContainer);

        chatMessages.scrollTop = chatMessages.scrollHeight;
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  });
});
