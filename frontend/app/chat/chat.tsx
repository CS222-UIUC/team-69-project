import { Link } from 'react-router';
import { Fragment, useEffect, useState } from 'react';
import logo from '../assets/logo.png';
import './chat.css';
import { z } from 'zod';
import { useQuery } from '@tanstack/react-query';
import { socket } from '~/socket';

interface Chat {
  id: number;
  name: string;
  direction: string;
}

interface Message {
  sender: string;
  message: string;
}

export default function Chat_App() {
  const {
    data: chats,
    error,
    isLoading,
    refetch,
  } = useQuery({
    queryKey: ['chats'],
    queryFn: async (): Promise<Chat[]> => {
      return fetch(`${import.meta.env.VITE_API_BASE}/chat/chats`, {
        credentials: 'include',
      }).then((response) => response.json());
    },
    retry: 2,
  });

  const [selectedChat, setSelectedChat] = useState<Chat>({
    id: -1,
    name: '',
    direction: '',
  });
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    function onConnect() {
      console.log('connected');
    }

    function onDisconnect() {
      console.log('disconnected');
    }

    function onMessage(msg: Message) {
      setMessages((prev) => [...prev, msg]);
    }

    socket.on('connect', onConnect);
    socket.on('disconnect', onDisconnect);
    socket.on('message', onMessage);

    return () => {
      socket.off('connect', onConnect);
      socket.off('disconnect', onDisconnect);
      socket.off('message', onMessage);
    };
  }, []);

  useEffect(() => {
    const user_id = new URLSearchParams(window.location.search).get('id');
    if (user_id == null) return;
    window.history.replaceState(
      {},
      '_',
      window.location.origin + window.location.pathname
    ); // react router framework mode is very confusing

    const chat = chats?.find((chat) => chat.id == parseInt(user_id));
    if (!chat) return;

    joinChat(chat);
  }, [chats]);

  const handleKeyPress = (event: React.KeyboardEvent<HTMLInputElement>) => {
    const input = event.target as HTMLInputElement;
    if (event.key === 'Enter' && input.value.trim() !== '') {
      event.preventDefault();

      const message = input.value;
      socket.emit('message', { message });

      input.value = '';
    }
  };

  useEffect(() => {
    if (selectedChat.id == -1) return;

    const fetchMessages = async () => {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE}/chat/messages`,
        {
          credentials: 'include',
        }
      );
      if (response.status != 200) return;

      const msgs = await response.json();
      setMessages((prev) => msgs);
    };

    // fetchMessages(); // too slow
  }, [selectedChat]);

  const joinChat = async (chat: Chat) => {
    const response = await fetch(
      `${import.meta.env.VITE_API_BASE}/chat/join?m=${chat.id}`,
      {
        method: 'POST',
        credentials: 'include',
      }
    );

    if (response.status != 200) {
      alert('Failed to join chat!');
    }

    setMessages((prev) => []);

    socket.disconnect();
    socket.connect();

    await new Promise((resolve) => setTimeout(resolve, 200));

    setSelectedChat(chat);
  };

  return (
    <div className="text-black">
      <nav className="flex justify-between items-center px-8 py-4 bg-white shadow-md">
        <img src={logo} className="w-32" />
        <ul className="flex space-x-6 text-gray-700">
          <li>
            <Link to={'/matches'} id="link">
              Home
            </Link>
          </li>
          <li>
            <a href="#" id="link">
              Find a Tutor
            </a>
          </li>
          <li>
            <Link to={'/chat'} id="link">
              Home
            </Link>
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
          {/* Username <i className="fas fa-caret-down"></i> */}
        </div>
      </nav>

      <div className="main">
        <aside className="chat-list">
          <h2>Chats</h2>
          <div className="chat-contacts">
            {chats &&
              chats.map((chat) => (
                <Fragment key={chat.name}>
                  <div className="contact" onClick={() => joinChat(chat)}>
                    <img
                      className="avatar"
                      src={`https://api.dicebear.com/7.x/bottts/svg?seed=${chat.name}`}
                    ></img>
                    <span>{chat.name}</span>
                  </div>
                  <hr></hr>
                </Fragment>
              ))}
          </div>
        </aside>

        <section className="chat-window">
          <div className="chat-header">
            {selectedChat.name && (
              <img
                className="avatar"
                src={`https://api.dicebear.com/7.x/bottts/svg?seed=${selectedChat.name}`}
              ></img>
            )}
            <span>{selectedChat.name}</span>
          </div>
          <div className="chat-messages" id="chat-messages">
            {selectedChat.id != -1 &&
              messages.map((message, i) => (
                <p
                  className={
                    message.sender == selectedChat.name
                      ? 'message received'
                      : 'message sent'
                  }
                  key={message.sender + i}
                >
                  {message.message}
                </p>
              ))}
          </div>
          <div className="chat-input">
            <input
              type="text"
              id="message-input"
              placeholder="Type a message"
              onKeyUp={handleKeyPress}
            ></input>
          </div>
        </section>
      </div>
    </div>
  );
}
