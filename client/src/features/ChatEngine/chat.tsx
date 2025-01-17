import React from 'react';
import { Paperclip, Mic, Send, Plus, MessageSquare } from 'lucide-react';
import SideBar from './components/Sidebar';

const ChatInterface = () => {
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Left Sidebar - Chat Threads */}
      <SideBar/>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* Sample Messages */}
          <div className="flex gap-4 max-w-3xl mx-auto">
            <div className="w-8 h-8 rounded-full bg-blue-600 flex-shrink-0" />
            <div className="flex-1">
              <p className="bg-white rounded-lg p-4 shadow-sm">
                Hello! How can I help you today?
              </p>
            </div>
          </div>
          
          <div className="flex gap-4 max-w-3xl mx-auto">
            <div className="w-8 h-8 rounded-full bg-gray-300 flex-shrink-0" />
            <div className="flex-1">
              <p className="bg-blue-50 rounded-lg p-4 shadow-sm">
                I have a question about...
              </p>
            </div>
          </div>
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-200 p-4">
          <div className="max-w-3xl mx-auto">
            <div className="relative bg-white rounded-lg shadow-sm">
              <div className="min-h-[20px] max-h-[200px] overflow-y-auto p-3 pr-12">
                <textarea 
                  placeholder="Type your message..." 
                  className="w-full resize-none outline-none"
                  rows={1}
                />
              </div>
              
              {/* Action Buttons */}
              <div className="absolute bottom-2 right-2 flex items-center gap-2">
                <button className="p-2 text-gray-500 hover:text-gray-700 rounded-full hover:bg-gray-100">
                  <Paperclip size={20} />
                </button>
                <button className="p-2 text-gray-500 hover:text-gray-700 rounded-full hover:bg-gray-100">
                  <Mic size={20} />
                </button>
                <button className="p-2 text-white bg-blue-600 rounded-full hover:bg-blue-700">
                  <Send size={20} />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;