import { useState } from 'react';

export const Test = () => {
    const [query, setQuery] = useState('');
    const [chatHistory, setChatHistory] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleSendQuery = async () => {
        if (query.trim() === '') return;

        const userMessage = { sender: 'You', message: query };
        setChatHistory([...chatHistory, userMessage]);
        setLoading(true);

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            });

            const data = await response.json();
            const botMessage = { sender: 'Chatbot', message: data.response };

            setChatHistory((prevHistory) => [...prevHistory, botMessage]);
        } catch (error) {
            console.error('Error communicating with chatbot:', error);
        } finally {
            setLoading(false);
            setQuery('');  // Clear the input field
        }
    };

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            handleSendQuery();
        }
    };

    return (
        <div style={styles.container}>
            <br />
            <h1>Chatbot Test</h1>

            <div style={styles.chatWindow}>
                {chatHistory.map((entry, index) => (
                    <div key={index} style={entry.sender === 'You' ? styles.userMessage : styles.botMessage}>
                        <strong>{entry.sender}:</strong> {entry.message}
                    </div>
                ))}
                {loading && <div style={styles.loadingMessage}>Chatbot is typing...</div>}
            </div>

            <div style={styles.inputContainer}>
                <input
                    type="text"
                    placeholder="Type your query..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyPress={handleKeyPress}
                    style={styles.input}
                    disabled={loading}  // Disable input while loading
                />
                <button onClick={handleSendQuery} style={styles.button} disabled={loading}>
                    {loading ? 'Sending...' : 'Send'}
                </button>
            </div>
        </div>
    );
};

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
    loadingMessage: {
        textAlign: 'center',
        color: '#999',
    },
};
