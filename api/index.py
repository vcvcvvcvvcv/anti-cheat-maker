"use client";

import { useState } from "react";
import { Send, Shield } from "lucide-react";

export default function Home() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([
    {
      role: "ai",
      content:
        "Welcome to Spectre AI. I specialize in Gorilla Tag copy security, anti-cheat architecture, Unity, PlayFab, Photon, and multiplayer protection."
    }
  ]);

  async function sendMessage() {
    if (!message.trim()) return;

    const userMessage = message;

    setChat((old) => [
      ...old,
      { role: "user", content: userMessage }
    ]);

    setMessage("");

    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: userMessage
      })
    });

    const data = await response.json();

    setChat((old) => [
      ...old,
      {
        role: "ai",
        content: data.reply
      }
    ]);
  }

  return (
    <main className="min-h-screen bg-black text-white flex flex-col">

      <header className="p-5 border-b border-zinc-800 flex justify-between">
        <div className="flex gap-2 items-center">
          <Shield />
          <h1 className="text-xl font-bold">
            Spectre AI
          </h1>
        </div>

        <button className="bg-zinc-800 px-4 py-2 rounded-xl">
          Credits
        </button>
      </header>


      <section className="flex-1 p-5 space-y-4 overflow-y-auto">

        {chat.map((msg,index)=>(
          <div
            key={index}
            className={
              msg.role==="user"
              ?
              "bg-purple-700 p-4 rounded-xl ml-auto max-w-xl"
              :
              "bg-zinc-900 p-4 rounded-xl max-w-xl"
            }
          >
            {msg.content}
          </div>
        ))}

      </section>


      <footer className="p-5 border-t border-zinc-800 flex gap-3">

        <input
          value={message}
          onChange={(e)=>setMessage(e.target.value)}
          onKeyDown={(e)=>{
            if(e.key==="Enter") sendMessage();
          }}
          placeholder="Ask about anti-cheat..."
          className="flex-1 bg-zinc-900 p-4 rounded-xl outline-none"
        />

        <button
          onClick={sendMessage}
          className="bg-purple-600 p-4 rounded-xl"
        >
          <Send/>
        </button>

      </footer>

    </main>
  );
}
