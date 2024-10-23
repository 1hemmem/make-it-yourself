import { useState } from 'react';

export const Test = () => {
    const [query, setQuery] = useState('');
    const [chatHistory, setChatHistory] = useState([]);

    // Function to handle submitting the user's query
    const handleSendQuery = async () => {
        if (query.trim() === '') return;

        // Append the user's query to the chat history
        const userMessage = { sender: 'You', message: query };
        setChatHistory([...chatHistory, userMessage]);

        // Simulate the chatbot's response
        const chatbotResponse = await getChatbotResponse(query);
        const botMessage = { sender: 'Chatbot', message: chatbotResponse };

        // Update the chat history with the bot's response
        setChatHistory(prevHistory => [...prevHistory, botMessage]);

        // Clear the query input
        setQuery('');
    };

    // Simulate the chatbot's response (replace this with your actual chatbot integration)
    const getChatbotResponse = async (userQuery) => {
        // Simulate a delay for the chatbot's response
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(`This is a response to "${userQuery}"`);
            }, 1000);
        });
    };

    // Function to handle pressing Enter in the input field
    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            handleSendQuery();
        }
    };

    return (
        <div style={styles.container}>
            <h1>Chatbot Test</h1>

            {/* Conversation window */}
            <div style={styles.chatWindow}>
                {chatHistory.map((entry, index) => (
                    <div key={index} style={entry.sender === 'You' ? styles.userMessage : styles.botMessage}>
                        <strong>{entry.sender}:</strong> {entry.message}
                    </div>
                ))}
            </div>

            {/* Input for sending a query */}
            <div style={styles.inputContainer}>
                <input
                    type="text"
                    placeholder="Type your query..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyPress={handleKeyPress}
                    style={styles.input}
                />
                <button onClick={handleSendQuery} style={styles.button}>Send</button>
            </div>
        </div>
    );
};

// Styles for the component
const styles = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '20px',
        fontFamily: 'Inter, system-ui, Avenir, Helvetica, Arial, sans-serif',
    },
    chatWindow: {
        width: '100%',
        maxWidth: '600px',
        height: '400px',
        border: '1px solid #ccc',
        borderRadius: '10px',
        padding: '10px',
        overflowY: 'scroll',
        marginBottom: '20px',
        backgroundColor: '#f9f9f9',
    },
    userMessage: {
        alignSelf: 'flex-end',
        backgroundColor: '#daf0da',
        padding: '10px',
        borderRadius: '10px',
        margin: '5px',
        maxWidth: '80%',
    },
    botMessage: {
        alignSelf: 'flex-start',
        backgroundColor: '#f0f0f0',
        padding: '10px',
        borderRadius: '10px',
        margin: '5px',
        maxWidth: '80%',
    },
    inputContainer: {
        display: 'flex',
        justifyContent: 'center',
        width: '100%',
        maxWidth: '600px',
    },
    input: {
        flex: 1,
        padding: '10px',
        fontSize: '1rem',
        borderRadius: '10px',
        border: '1px solid #ccc',
        marginRight: '10px',
    },
    button: {
        padding: '10px 20px',
        fontSize: '1rem',
        borderRadius: '10px',
        border: 'none',
        backgroundColor: '#646cff',
        color: 'white',
        cursor: 'pointer',
    },
};
