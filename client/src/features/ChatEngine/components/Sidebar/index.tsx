
import { Plus, MessageSquare } from 'lucide-react';


function SideBar() {
  return (
    <div className="w-50 bg-red-400 border-r border-gray-200">
        {/* New Chat Button */}
        <div className="p-4 border-b border-gray-200">
          <button className="w-full flex items-center justify-center gap-2 bg-blue-600 text-white rounded-lg py-2 px-4 hover:bg-blue-700">
            <Plus size={20} />
            New Chat
          </button>
        </div>
        
        {/* Thread List */}
        <div className="overflow-y-auto h-[calc(100vh-70px)]">
          {/* Sample Thread Items */}
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="flex items-center gap-3 p-4 hover:bg-gray-100 cursor-pointer border-b border-gray-100"
            >
              <MessageSquare size={20} className="text-gray-500" />
              <div>
                <p className="font-medium">Chat Thread {i}</p>
                <p className="text-sm text-gray-500 truncate">
                  Last message preview...
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
  )
}

export default SideBar