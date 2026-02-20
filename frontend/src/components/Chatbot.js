import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./Chatbot.css";

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { role: "ai", content: "Hi! I'm SalesMind AI. How can I help you scale your outreach today?" }
  ]);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isOpen]);

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMessage = { role: "user", content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput("");

    try {
      const res = await axios.post("http://127.0.0.1:5000/api/chat", { message: input });
      setMessages(prev => [...prev, { role: "ai", content: res.data.reply }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: "ai", content: "I'm having trouble connecting to my brain! Please try again later." }]);
    }
  };

  return (
    <div className="chatbot-container">
      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <div className="bot-info">
              <div className="online-indicator"></div>
              <span>SalesMind AI</span>
            </div>
            <button className="close-btn" onClick={() => setIsOpen(false)}>×</button>
          </div>
          
          <div className="chat-body">
            {messages.map((msg, i) => (
              <div key={i} className={`message-row ${msg.role}`}>
                <div className="message-bubble">{msg.content}</div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-footer">
            <input 
              value={input} 
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleSend()}
              placeholder="Type a message..."
            />
            <button className="send-btn" onClick={handleSend}>➤</button>
          </div>
        </div>
      )}
      <button className="chat-launcher" onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? "✕" : "💬"}
      </button>
    </div>
  );
}