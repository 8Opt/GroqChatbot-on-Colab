const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const chatHistory = document.getElementById('chat-history');

const GROQ_API_KEY = "gsk_sTH6Z8...........QZGfUQ6";
const GROQ_URL = "https://api.groq.com/openai/v1/chat/completions";
const GROQ_MODEL = "llama3-8b-8192";

// Mock chatbot responses fetch data from a GROQ API)
async function groqResonse (userPrompt) {
    console.log("Hi")
    const response = await fetch(GROQ_URL, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${GROQ_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: [
            {
                role: 'system',
                content:
                    'You are a helpful assistant in the areas of consulting. Do not use MARKDOWN, just plain-text.'
            },
            {
                role: 'user',
                content: userPrompt
            }
        ],
        model: GROQ_MODEL,
        temperature: 1,
        // max_tokens: 1024,
        top_p: 1,
        stream: false,
        stop: null
    })
    });
  
    if (!response.ok) {
      throw new Error(`API request failed with status: ${response.status}`);
    }
  
    const responseData = await response.json();
    // console.log(responseData.choices[0].message.content)
    return responseData.choices[0].message.content; // Assuming the first choice contains the response
  }

sendButton.addEventListener('click', function() {
    const userMessage = userInput.value.trim();
    if (userMessage) {
        appendMessage(userMessage, 'user');
        userInput.value = '';

        // try{
        // Simulate fetching data from GROQ API (replace with actual API call)
        const botResponse = groqResonse(userMessage).then((response) => {
          appendMessage(response, 'bot')
        })
        console.log(botResponse)
        // setTimeout(() => {
        // appendMessage(botResponse, 'bot');
        // }, 1000); // Simulate a delay
        // }catch(err){
        //     appendMessage("We are sorry for the convinient, somethine went wrong" ,"bot")
        // }
  }
});

function appendMessage(message, type) {
    const messageElement = document.createElement('div');
    messageElement.classList.add(`${type}-message`);
    messageElement.textContent = message;
    chatHistory.appendChild(messageElement);
    chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll down to the latest message
}