import { useState } from 'react';
import "./Styles/Test.css";
import ReactMarkdown from 'react-markdown';

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
      setQuery(''); // Clear the input field
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSendQuery();
    }
  };

  return (
    <div className="test-container">
      <br />
      <h1 className="test-title">Chatbot Test</h1>

      <div className="chat-window">
        {chatHistory.map((entry, index) => (
          <div key={index} className={entry.sender === 'You' ? 'user-message' : 'bot-message'}>
            <strong>{entry.sender}:</strong> <ReactMarkdown>{entry.message}</ReactMarkdown>
          </div>
        ))}
        {loading && <div className="loading-message">Chatbot is typing...</div>}
      </div>

      <div className="input-container">
        <input
          type="text"
          placeholder="Type your query..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          className="input"
          disabled={loading} // Disable input while loading
        />
        <button onClick={handleSendQuery} className="button" disabled={loading}>
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
};
