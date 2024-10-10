// Auto-scroll the chat window to the bottom when new content is added
function scrollToBottom() {
    var chatWindow = document.getElementById('chat-window');
    if (chatWindow) {
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
}

// Submit the chat form using AJAX to prevent page reload
function submitChatForm(event) {
    event.preventDefault();  // Prevent the default form submission

    var form = document.getElementById('chat-form');
    var formData = new FormData(form);
    var sessionId = form.dataset.sessionId;

    fetch('/chat/' + sessionId, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'  // Identify the request as AJAX
        },
        credentials: 'same-origin'  // Include cookies in the request
    })
    .then(response => response.text())
    .then(html => {
        // Replace the chat content with the updated content from the server
        var parser = new DOMParser();
        var doc = parser.parseFromString(html, 'text/html');
        var newContent = doc.getElementById('chat-content');
        document.getElementById('chat-content').innerHTML = newContent.innerHTML;

        // Clear the input field
        document.getElementById('question').value = '';

        // Scroll to the bottom of the chat window
        scrollToBottom();
    })
    .catch(error => console.error('Error:', error));
}

// Attach event listeners after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Attach the submit event handler to the chat form
    var chatForm = document.getElementById('chat-form');
    if (chatForm) {
        chatForm.addEventListener('submit', submitChatForm);
    }

    // Scroll to bottom on page load
    scrollToBottom();
});
