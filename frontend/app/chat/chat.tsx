import { Link } from 'react-router';
import { useEffect } from 'react';
import logo from '../assets/logo.png';
import './chat.css';
import { z } from 'zod';

export default function Chat_App() {
  useEffect(() => {
    const input = document.getElementById('message-input') as HTMLInputElement;
    const chatMessages = document.getElementById('chat-messages');

    if (input && chatMessages) {
      input.addEventListener('keypress', function (event) {
        if (event.key === 'Enter' && input.value.trim() !== '') {
          event.preventDefault();

          const newMessage = document.createElement('div');
          newMessage.classList.add('message', 'sent');
          newMessage.innerHTML = `<p>${input.value}</p>`;

          chatMessages.appendChild(newMessage);

          chatMessages.scrollTop = chatMessages.scrollHeight;

          input.value = '';
        }
      });
    }
  }, []);

  return (
    <body>
      <link
        rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
      />
      <nav className="flex justify-between items-center px-8 py-4 bg-white shadow-md">
        <img src={logo} className="w-32" />
        <ul className="flex space-x-6 text-gray-700">
          <li>
            <a href="#" id="link">
              Home
            </a>
          </li>
          <li>
            <a href="#" id="link">
              Find a Tutor
            </a>
          </li>
          <li>
            <a href="#" id="link">
              Messages
            </a>
          </li>
          <li>
            <a href="#" id="link">
              About Us
            </a>
          </li>
          <li>
            <a href="#" id="link">
              Contact
            </a>
          </li>
        </ul>
        <div className="user-dropdown">
          Username <i className="fas fa-caret-down"></i>
        </div>
      </nav>

      <div className="main">
        <aside className="chat-list">
          <h2>Chats</h2>
          <input type="text" placeholder="Search"></input>
          <div className="chat-contacts">
            <div className="contact">
              <div className="avatar"></div>
              <span>Adeetya Upadhyay</span>
            </div>
          </div>
        </aside>

        <section className="chat-window">
          <div className="chat-header">
            <div className="avatar"></div>
            <span>Adeetya Upadhyay</span>
          </div>
          <div className="chat-messages" id="chat-messages"></div>
          <div className="chat-input">
            <input
              type="text"
              id="message-input"
              placeholder="Type a message"
            ></input>
          </div>
        </section>
      </div>
    </body>
  );
}
