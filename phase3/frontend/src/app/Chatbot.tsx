"use client";
import { useChatKit, ChatKit } from "@openai/chatkit-react";
import Script from "next/script";
import { useAuth } from "@/context/AuthContext";
// Persistence-related hooks removed to fix build error
// import { useEffect, useState } from "react"; 

export function Chatbot() {
  const { user, token, loading } = useAuth();
  // const [threadId, setThreadId] = useState<string | undefined>(undefined); // Removed

  // // Removed useEffect for loading threadId from localStorage
  // useEffect(() => {
  //   const savedThreadId = localStorage.getItem('chat_thread_id');
  //   if (savedThreadId) {
  //     console.log(`Resuming chat with thread ID: ${savedThreadId}`);
  //     setThreadId(savedThreadId);
  //   }
  // }, []);

  // Guard Clause: Render nothing until user/token are available.
  if (loading || !token || !user) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-gray-800">
        <p className="text-white">Loading Assistant...</p>
      </div>
    );
  }

  // The component that will actually render ChatKit.
  const StableChatComponent = () => {
    const chatkit = useChatKit({
      api: {
        url: `${process.env.NEXT_PUBLIC_CHATKIT_API_URL}/chatkit/api`,
        domainKey: process.env.NEXT_PUBLIC_CHATKIT_DOMAIN_KEY || "gemini-todo-dev",
        fetch: async (url, options) => {
          const newOptions = { ...options };
          newOptions.headers = { ...options?.headers, Authorization: `Bearer ${token}` };
          if (newOptions.body && typeof newOptions.body === 'string' && newOptions.headers && (newOptions.headers as any)['Content-Type'] === 'application/json') {
            try {
              const body = JSON.parse(newOptions.body);
              body.user = { id: String(user.id) };
              newOptions.body = JSON.stringify(body);
            } catch (e) {
              console.error("Failed to inject user ID:", e);
            }
          }
          return fetch(url, newOptions);
        },
      },
      // Removed incorrect threadId prop
      // threadId: threadId,
      onError: ({ error }) => {
        console.error("ChatKit Error:", error);
      },
    });

    return (
      <ChatKit
        key={user.id}
        control={chatkit.control}
        // Removed onEvent prop for saving threadId
        // onEvent={(event) => {
        //   if (event.type === 'thread.created') {
        //     const newThreadId = event.thread.id;
        //     console.log(`New chat thread created. Saving ID: ${newThreadId}`);
        //     setThreadId(newThreadId);
        //     localStorage.setItem('chat_thread_id', newThreadId);
        //   }
        // }}
      />
    );
  };

  return (
    <>
      <Script
        src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
        strategy="afterInteractive"
      />
      <StableChatComponent />
    </>
  );
}
