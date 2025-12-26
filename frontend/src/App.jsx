import React, { useState, useEffect, useRef } from 'react';
import {
  Monitor,
  Camera,
  MessageSquare,
  Settings,
  X,
  Maximize2,
  Minimize2,
  Cpu,
  Layers,
  Image as ImageIcon,
  Send,
  Bot,
  MoreVertical,
  History,
  Zap,
  Globe,
  Code,
  PenTool,
  Grid,
  ChevronRight,
  ChevronDown,
  Key,
  Server,
  Shield
} from 'lucide-react';

// --- Mock Data ---

const MOCK_SESSIONS = [
  { id: 1, title: 'Debugging React Component', app: 'VS Code', time: '2m ago' },
  { id: 2, title: 'Excel Pivot Table Help', app: 'Excel', time: '2h ago' },
  { id: 3, title: 'Blender UV Unwrapping', app: 'Blender', time: 'Yesterday' },
  { id: 4, title: 'Email Drafting Assistance', app: 'Outlook', time: 'Yesterday' },
];

const APPS_CONTEXTS = [
  { id: 'vscode', name: 'VS Code', icon: Code, color: 'text-blue-500' },
  { id: 'browser', name: 'Browser', icon: Globe, color: 'text-orange-500' },
  { id: 'design', name: 'Design Tools', icon: PenTool, color: 'text-purple-500' },
  { id: 'data', name: 'Data/Excel', icon: Grid, color: 'text-green-500' },
  { id: 'ue5', name: 'Unreal Engine', icon: Layers, color: 'text-blue-400' },
];

// --- Components ---

const SidebarItem = ({ active, title, subtitle, icon: Icon }) => (
  <div className={`group flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-all duration-200 ${active ? 'bg-indigo-600/10 border border-indigo-500/30' : 'hover:bg-slate-800'}`}>
    <div className={`p-2 rounded-lg ${active ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400 group-hover:bg-slate-700 group-hover:text-slate-200'}`}>
      <Icon size={18} />
    </div>
    <div className="flex-1 min-w-0">
      <h4 className={`text-sm font-medium truncate ${active ? 'text-indigo-100' : 'text-slate-300'}`}>{title}</h4>
      <p className="text-xs text-slate-500 truncate">{subtitle}</p>
    </div>
  </div>
);

const MessageBubble = ({ message }) => {
  const isAi = message.sender === 'ai';

  return (
    <div className={`flex gap-4 ${isAi ? '' : 'flex-row-reverse'} mb-6 animate-fade-in`}>
      <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${isAi ? 'bg-indigo-600' : 'bg-slate-600'}`}>
        {isAi ? <Bot size={20} className="text-white" /> : <div className="text-sm font-bold text-white">ME</div>}
      </div>

      <div className={`flex flex-col max-w-[75%] ${isAi ? 'items-start' : 'items-end'}`}>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xs font-bold text-slate-300">{isAi ? 'Chimera Assistant' : 'You'}</span>
          <span className="text-xs text-slate-500">{message.timestamp}</span>
        </div>

        <div className={`p-4 rounded-2xl shadow-sm ${isAi ? 'bg-slate-800 text-slate-200 rounded-tl-none' : 'bg-indigo-600 text-white rounded-tr-none'}`}>
          {message.image && (
            <div className="mb-3 rounded-lg overflow-hidden border border-white/10">
              <img src={message.image} alt="Context" className="w-full h-auto object-cover max-h-64" />
            </div>
          )}
          <p className="whitespace-pre-wrap leading-relaxed text-sm">{message.text}</p>
          {message.code && (
            <div className="mt-3 bg-slate-950 p-3 rounded-lg border border-slate-700/50 overflow-x-auto">
              <pre className="text-xs font-mono text-green-400 font-medium">{message.code}</pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const SettingsModal = ({ isOpen, onClose, status, provider, setProvider }) => {
  const [activeTab, setActiveTab] = useState('Providers');

  if (!isOpen) return null;

  const renderContent = () => {
    switch (activeTab) {
      case 'Providers':
        return (
          <div className="space-y-6 animate-fade-in">
            <h3 className="text-sm uppercase tracking-wider text-slate-500 font-bold mb-4">LLM Provider Setup</h3>

            <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800 space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-300 flex items-center gap-2">
                  <Server size={14} className="text-indigo-400" /> Primary Provider
                </label>
                <select
                  value={provider}
                  onChange={(e) => setProvider(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:ring-2 focus:ring-indigo-500 outline-none"
                >
                  {status.plugins.map(p => (
                    <option key={p} value={p}>{p.toUpperCase()}</option>
                  ))}
                </select>
              </div>

              <div className="text-xs text-slate-500">
                Available providers: {status.plugins.join(', ')}
              </div>
            </div>
          </div>
        );
      case 'General':
        return (
           <div className="space-y-6 animate-fade-in">
             <h3 className="text-sm uppercase tracking-wider text-slate-500 font-bold mb-4">Application Settings</h3>
              <div className="pt-2">
                <div className="flex items-center justify-between p-3 bg-slate-950/50 rounded-xl border border-slate-800">
                  <div>
                    <h4 className="text-sm font-medium text-slate-200">Auto-Context Awareness</h4>
                    <p className="text-xs text-slate-500">Automatically detect active window focus</p>
                  </div>
                  <div className="w-11 h-6 bg-indigo-600 rounded-full relative cursor-pointer">
                    <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full shadow-sm"></div>
                  </div>
                </div>
              </div>
           </div>
        );
      default:
        return <div className="text-slate-500 text-sm p-4">Settings for {activeTab} coming soon...</div>;
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 w-full max-w-2xl rounded-2xl border border-slate-700 shadow-2xl overflow-hidden flex flex-col h-[600px]">
        <div className="p-5 border-b border-slate-700 flex justify-between items-center bg-slate-800/50">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2">
            <Settings size={20} /> Chimera Settings
          </h2>
          <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors">
            <X size={20} />
          </button>
        </div>

        <div className="flex flex-1 overflow-hidden">
          {/* Sidebar */}
          <div className="w-48 bg-slate-900 border-r border-slate-800 p-3 space-y-1">
            {['General', 'Providers', 'Shortcuts', 'Privacy', 'About'].map((item) => (
              <button
                key={item}
                onClick={() => setActiveTab(item)}
                className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === item ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'}`}
              >
                {item}
              </button>
            ))}
          </div>

          {/* Content */}
          <div className="flex-1 p-6 overflow-y-auto custom-scrollbar">
            {renderContent()}
          </div>
        </div>

        <div className="p-4 border-t border-slate-800 bg-slate-800/30 flex justify-end gap-3">
          <button onClick={onClose} className="px-4 py-2 rounded-lg text-sm font-medium text-slate-300 hover:bg-slate-800 transition-colors">Cancel</button>
          <button onClick={onClose} className="px-4 py-2 rounded-lg text-sm font-medium bg-indigo-600 hover:bg-indigo-500 text-white transition-colors shadow-lg shadow-indigo-500/20">Save Configuration</button>
        </div>
      </div>
    </div>
  );
};

// --- Main App Component ---

export default function DesktopAssistant() {
  const [activeTab, setActiveTab] = useState('chat');
  const [showSettings, setShowSettings] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'ai',
      text: "Hello! I'm Chimera, your AI assistant. I can help you with coding, debugging, and understanding your screen context. How can I assist you today?",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isCapturing, setIsCapturing] = useState(false);
  const [selectedContext, setSelectedContext] = useState('vscode');
  const [widgetExpanded, setWidgetExpanded] = useState(false);
  const [status, setStatus] = useState({ plugins: [], active_sessions: [], tools: [] });
  const [provider, setProvider] = useState('ollama');
  const [isLoading, setIsLoading] = useState(false);

  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Fetch backend status
  const fetchStatus = async () => {
    try {
      const res = await fetch('/api/status');
      const data = await res.json();
      setStatus(data);

      // Set default provider
      if (!data.plugins.includes(provider)) {
        setProvider(data.plugins.includes("ollama") ? "ollama" : (data.plugins[0] || "ollama"));
      }
    } catch (e) {
      console.error('Failed to fetch status:', e);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    const newMsg = {
      id: messages.length + 1,
      sender: 'user',
      text: inputText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages([...messages, newMsg]);
    setInputText('');
    setIsLoading(true);

    // Call backend API
    try {
      const res = await fetch('/v1/chat/completions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: provider,
          messages: [{ role: 'user', content: inputText }]
        })
      });
      const data = await res.json();

      setMessages(prev => [...prev, {
        id: prev.length + 1,
        sender: 'ai',
        text: data?.choices?.[0]?.message?.content || "I couldn't generate a response. Please try again.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        id: prev.length + 1,
        sender: 'ai',
        text: `Error: ${error.message}. Make sure the backend server is running.`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const captureScreen = () => {
    setIsCapturing(true);
    setTimeout(() => setIsCapturing(false), 800);
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-200 font-sans selection:bg-indigo-500/30 overflow-hidden">

      {/* --- Left Sidebar: Navigation & History --- */}
      <aside className="w-[280px] bg-slate-900 border-r border-slate-800 flex flex-col flex-shrink-0 z-20">
        <div className="h-16 flex items-center px-6 border-b border-slate-800">
          <div className="flex items-center gap-2 text-indigo-400">
            <Cpu size={24} className="animate-pulse-slow" />
            <h1 className="text-xl font-bold tracking-tight text-white">CHIMERA</h1>
          </div>
        </div>

        <div className="p-4">
          <button
            onClick={() => setMessages([{
              id: 1,
              sender: 'ai',
              text: "New session started. How can I help you?",
              timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            }])}
            className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white py-3 rounded-xl transition-all shadow-lg shadow-indigo-900/20 font-medium"
          >
            <Monitor size={18} />
            <span>New Session</span>
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-4 pb-4 space-y-6 custom-scrollbar">
          <div>
            <div className="flex items-center justify-between mb-3 px-2">
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Active Contexts</h3>
            </div>
            <div className="space-y-1">
              {APPS_CONTEXTS.map((app) => (
                <div
                  key={app.id}
                  onClick={() => setSelectedContext(app.id)}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer text-sm transition-colors ${selectedContext === app.id ? 'bg-slate-800 text-white ring-1 ring-slate-700' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'}`}
                >
                  <app.icon size={16} className={selectedContext === app.id ? app.color : 'text-slate-500'} />
                  <span>{app.name}</span>
                  {selectedContext === app.id && <div className="ml-auto w-1.5 h-1.5 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]"></div>}
                </div>
              ))}
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-3 px-2">
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Recent History</h3>
              <History size={14} className="text-slate-600" />
            </div>
            <div className="space-y-2">
              {MOCK_SESSIONS.map((session) => (
                <SidebarItem
                  key={session.id}
                  active={session.id === 1}
                  title={session.title}
                  subtitle={`${session.app} • ${session.time}`}
                  icon={MessageSquare}
                />
              ))}
            </div>
          </div>
        </div>

        <div className="p-4 border-t border-slate-800">
          <button onClick={() => setShowSettings(true)} className="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-slate-400 hover:bg-slate-800 hover:text-white transition-colors text-sm">
            <Settings size={18} />
            <span>Settings</span>
          </button>
        </div>
      </aside>

      {/* --- Center: Main Chat Interface --- */}
      <main className="flex-1 flex flex-col min-w-0 bg-slate-950 relative">
        {/* Header */}
        <header className="h-16 border-b border-slate-800 bg-slate-900/50 backdrop-blur-md flex items-center justify-between px-6 sticky top-0 z-10">
          <div className="flex items-center gap-4">
            <div className="flex flex-col">
              <h2 className="text-base font-semibold text-white flex items-center gap-2">
                Chimera AI Assistant
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
                  {provider.toUpperCase()}
                </span>
              </h2>
              <span className="text-xs text-slate-500 flex items-center gap-1">
                <span className={`w-1.5 h-1.5 rounded-full ${status.plugins.length > 0 ? 'bg-green-500' : 'bg-red-500'}`}></span>
                {status.plugins.length > 0 ? `Connected • ${status.plugins.length} plugins loaded` : 'Connecting...'}
              </span>
            </div>
          </div>
          <div className="flex items-center gap-3">
             <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors">
               <MoreVertical size={20} />
             </button>
          </div>
        </header>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto p-6 scroll-smooth custom-scrollbar">
          <div className="max-w-3xl mx-auto">
            {messages.map(msg => <MessageBubble key={msg.id} message={msg} />)}
            {isLoading && (
              <div className="flex gap-4 mb-6">
                <div className="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center bg-indigo-600">
                  <Bot size={20} className="text-white" />
                </div>
                <div className="flex items-center gap-2 p-4 bg-slate-800 rounded-2xl rounded-tl-none">
                  <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="p-6 pt-2">
          <div className="max-w-3xl mx-auto relative bg-slate-900 rounded-2xl border border-slate-700 shadow-2xl focus-within:border-indigo-500/50 focus-within:ring-1 focus-within:ring-indigo-500/50 transition-all">
            <div className="flex items-center gap-2 p-2 border-b border-slate-800/50">
               <button onClick={captureScreen} className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${isCapturing ? 'bg-red-500/20 text-red-400 animate-pulse' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}>
                 <Camera size={14} />
                 {isCapturing ? 'Capturing...' : 'Capture Screen'}
               </button>
               <div className="h-4 w-px bg-slate-800 mx-1"></div>
               <button className="p-1.5 text-slate-400 hover:text-indigo-400 rounded-md hover:bg-slate-800">
                 <ImageIcon size={16} />
               </button>
               <button className="p-1.5 text-slate-400 hover:text-indigo-400 rounded-md hover:bg-slate-800">
                 <Code size={16} />
               </button>
            </div>
            <div className="flex items-end p-3 gap-3">
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSendMessage())}
                placeholder="Ask Chimera about your screen..."
                className="flex-1 bg-transparent border-none outline-none text-slate-200 placeholder:text-slate-600 resize-none max-h-32 min-h-[44px] py-2 text-sm"
                rows={1}
                disabled={isLoading}
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputText.trim() || isLoading}
                className={`p-2.5 rounded-xl transition-all ${inputText.trim() && !isLoading ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20 hover:scale-105' : 'bg-slate-800 text-slate-600 cursor-not-allowed'}`}
              >
                <Send size={18} />
              </button>
            </div>
          </div>
          <p className="text-center text-xs text-slate-600 mt-3">
            Chimera can make mistakes. Please verify important information.
          </p>
        </div>
      </main>

      {/* --- Right Panel: Live Context & Tools --- */}
      <aside className="w-[320px] bg-slate-900 border-l border-slate-800 flex flex-col z-20">
        <div className="p-4 border-b border-slate-800">
          <h3 className="text-sm font-bold text-slate-200 mb-3 flex items-center gap-2">
            <Monitor size={16} className="text-indigo-500" />
            Live Context
          </h3>

          <div className="relative group rounded-xl overflow-hidden border border-slate-700 bg-slate-950 aspect-video mb-4">
            {/* Live Browser Sessions */}
            {status.active_sessions.length > 0 ? (
              <div className="grid gap-2">
                {status.active_sessions.map(s => (
                  <div key={s.name} className="relative">
                    <img
                      src={s.screenshot + '?t=' + Date.now()}
                      alt={s.name}
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute bottom-2 left-2 px-2 py-1 bg-black/60 backdrop-blur text-[10px] text-white rounded font-mono">
                      {s.name}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="absolute inset-0 bg-slate-800 flex items-center justify-center">
                <div className="text-center text-slate-500 text-xs p-4">
                  No active sessions. Spawn a browser head to see live feed.
                </div>
              </div>
            )}

            {isCapturing && (
              <div className="absolute inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm">
                <div className="w-8 h-8 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              </div>
            )}
          </div>

          <div className="grid grid-cols-3 gap-2 mb-2">
            <button onClick={captureScreen} className="flex flex-col items-center justify-center gap-1 p-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-slate-600 rounded-lg transition-all group">
              <Maximize2 size={16} className="text-slate-400 group-hover:text-indigo-400" />
              <span className="text-[10px] text-slate-400">Full Screen</span>
            </button>
            <button onClick={captureScreen} className="flex flex-col items-center justify-center gap-1 p-2 bg-indigo-600/10 border border-indigo-500/30 rounded-lg transition-all">
              <Layers size={16} className="text-indigo-400" />
              <span className="text-[10px] text-indigo-300 font-medium">Active Window</span>
            </button>
            <button onClick={captureScreen} className="flex flex-col items-center justify-center gap-1 p-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-slate-600 rounded-lg transition-all group">
              <Minimize2 size={16} className="text-slate-400 group-hover:text-indigo-400" />
              <span className="text-[10px] text-slate-400">Region</span>
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          {/* Plugins Section */}
          <div>
             <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Available Plugins</h4>
             <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-800 space-y-2">
                {status.plugins.length > 0 ? status.plugins.map(plugin => (
                  <div key={plugin} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span className="text-xs font-medium text-slate-300 capitalize">{plugin}</span>
                    </div>
                    <button
                      onClick={() => setProvider(plugin)}
                      className={`text-[10px] px-2 py-0.5 rounded ${provider === plugin ? 'bg-indigo-600 text-white' : 'bg-slate-700 text-slate-400 hover:bg-slate-600'}`}
                    >
                      {provider === plugin ? 'Active' : 'Use'}
                    </button>
                  </div>
                )) : (
                  <div className="text-xs text-slate-500">Loading plugins...</div>
                )}
             </div>
          </div>

          {/* Quick Actions */}
          <div>
             <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Quick Actions</h4>
             <div className="space-y-2">
               <button className="w-full text-left px-3 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs text-slate-300 border border-slate-700 transition-colors flex items-center justify-between group">
                 <span>Explain this code block</span>
                 <ChevronRight size={14} className="text-slate-500 group-hover:text-white" />
               </button>
               <button className="w-full text-left px-3 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs text-slate-300 border border-slate-700 transition-colors flex items-center justify-between group">
                 <span>Find definition</span>
                 <ChevronRight size={14} className="text-slate-500 group-hover:text-white" />
               </button>
               <button className="w-full text-left px-3 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs text-slate-300 border border-slate-700 transition-colors flex items-center justify-between group">
                 <span>Generate Unit Tests</span>
                 <ChevronRight size={14} className="text-slate-500 group-hover:text-white" />
               </button>
             </div>
          </div>
        </div>

        {/* System Status Footer */}
        <div className="p-3 bg-slate-900 border-t border-slate-800 text-[10px] text-slate-500 flex justify-between items-center">
          <span>Plugins: {status.plugins.length}</span>
          <div className="flex items-center gap-1">
             <div className={`w-1.5 h-1.5 rounded-full ${status.plugins.length > 0 ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
             <span>{status.plugins.length > 0 ? 'Server Online' : 'Offline'}</span>
          </div>
        </div>
      </aside>

      <SettingsModal
        isOpen={showSettings}
        onClose={() => setShowSettings(false)}
        status={status}
        provider={provider}
        setProvider={setProvider}
      />

      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
          height: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #334155;
          border-radius: 3px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #475569;
        }
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
          animation: fade-in 0.3s ease-out forwards;
        }
      `}</style>
    </div>
  );
}
