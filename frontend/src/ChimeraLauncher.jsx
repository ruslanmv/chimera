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
  Key,
  Server,
  Shield,
  Play,
  Pause,
  FileText,
  Table,
  Presentation,
  Film,
  Palette,
  Database,
  Terminal
} from 'lucide-react';

// --- Mock Data ---

const MOCK_SESSIONS = [
  { id: 1, title: 'Debugging React Component', app: 'VS Code', time: '2m ago' },
  { id: 2, title: 'Excel Pivot Table Help', app: 'Excel', time: '2h ago' },
  { id: 3, title: 'PowerPoint Animation', app: 'PowerPoint', time: '1h ago' },
  { id: 4, title: 'Browser DevTools Debugging', app: 'Chrome', time: 'Yesterday' },
];

const MOCK_MESSAGES = [
  {
    id: 1,
    sender: 'user',
    text: "I'm trying to center this div vertically but flexbox isn't behaving as I expect. Here is what I have.",
    image: "https://images.unsplash.com/photo-1555099962-4199c345e5dd?q=80&w=1000&auto=format&fit=crop",
    timestamp: '10:42 AM'
  },
  {
    id: 2,
    sender: 'ai',
    text: "I see the issue. You have `align-items: center` set, but the parent container doesn't have a defined height. \n\nTry adding `height: 100vh` to the parent `div`. Also, ensure `flex-direction` is correct.",
    code: "div.parent {\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 100vh; /* Add this */\n}",
    timestamp: '10:43 AM'
  }
];

const APP_CONTEXTS = [
  { id: 'vscode', name: 'VS Code', icon: Code, color: 'text-blue-500', desc: 'Code editor' },
  { id: 'browser', name: 'Browser', icon: Globe, color: 'text-orange-500', desc: 'Web browsing' },
  { id: 'office-word', name: 'Word', icon: FileText, color: 'text-blue-600', desc: 'Document editing' },
  { id: 'office-excel', name: 'Excel', icon: Table, color: 'text-green-600', desc: 'Spreadsheets' },
  { id: 'office-powerpoint', name: 'PowerPoint', icon: Presentation, color: 'text-red-600', desc: 'Presentations' },
  { id: 'design', name: 'Design Tools', icon: Palette, color: 'text-purple-500', desc: 'Photoshop, Figma, etc.' },
  { id: '3d', name: '3D Software', icon: Layers, color: 'text-cyan-500', desc: 'Blender, UE5, Unity' },
  { id: 'video', name: 'Video Editing', icon: Film, color: 'text-pink-500', desc: 'Premiere, DaVinci' },
  { id: 'database', name: 'Database Tools', icon: Database, color: 'text-yellow-600', desc: 'SQL tools' },
  { id: 'terminal', name: 'Terminal', icon: Terminal, color: 'text-green-400', desc: 'Command line' },
];

// Mock available screens/monitors
const MOCK_SCREENS = [
  { id: 'screen-0', name: 'Primary Monitor', resolution: '2560x1440', isPrimary: true },
  { id: 'screen-1', name: 'Secondary Monitor', resolution: '1920x1080', isPrimary: false },
  { id: 'screen-2', name: 'Laptop Screen', resolution: '1920x1200', isPrimary: false },
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

const SettingsModal = ({ isOpen, onClose, selectedScreen, setSelectedScreen }) => {
  const [activeTab, setActiveTab] = useState('General');
  const [provider, setProvider] = useState('chimera');

  if (!isOpen) return null;

  const renderContent = () => {
    switch (activeTab) {
      case 'General':
        return (
          <div className="space-y-6 animate-fade-in">
            <h3 className="text-sm uppercase tracking-wider text-slate-500 font-bold mb-4">Application Settings</h3>

            {/* Screen Selection */}
            <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800 space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-300 flex items-center gap-2">
                  <Monitor size={14} className="text-indigo-400" /> Monitor/Screen Selection
                </label>
                <select
                  value={selectedScreen}
                  onChange={(e) => setSelectedScreen(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:ring-2 focus:ring-indigo-500 outline-none"
                >
                  {MOCK_SCREENS.map(screen => (
                    <option key={screen.id} value={screen.id}>
                      {screen.name} - {screen.resolution} {screen.isPrimary ? '(Primary)' : ''}
                    </option>
                  ))}
                </select>
                <p className="text-xs text-slate-500">Choose which monitor Chimera should analyze</p>
              </div>

              <div className="p-3 bg-indigo-600/10 border border-indigo-500/30 rounded-lg">
                <div className="flex items-start gap-2">
                  <Shield size={16} className="text-indigo-400 mt-0.5 flex-shrink-0" />
                  <div className="text-xs text-slate-300">
                    <span className="font-medium text-indigo-300">Green border indicator:</span> When active, a subtle green border will appear around the selected screen to show Chimera is monitoring.
                  </div>
                </div>
              </div>
            </div>

            {/* Auto-Context Settings */}
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-slate-950/50 rounded-xl border border-slate-800">
                <div>
                  <h4 className="text-sm font-medium text-slate-200">Auto-Context Detection</h4>
                  <p className="text-xs text-slate-500">Automatically detect active application</p>
                </div>
                <div className="w-11 h-6 bg-indigo-600 rounded-full relative cursor-pointer">
                  <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full shadow-sm"></div>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 bg-slate-950/50 rounded-xl border border-slate-800">
                <div>
                  <h4 className="text-sm font-medium text-slate-200">Continuous Monitoring</h4>
                  <p className="text-xs text-slate-500">Keep analyzing screen in background</p>
                </div>
                <div className="w-11 h-6 bg-slate-700 rounded-full relative cursor-pointer">
                  <div className="absolute left-1 top-1 w-4 h-4 bg-white rounded-full shadow-sm"></div>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 bg-slate-950/50 rounded-xl border border-slate-800">
                <div>
                  <h4 className="text-sm font-medium text-slate-200">Show Green Border</h4>
                  <p className="text-xs text-slate-500">Visual indicator when monitoring</p>
                </div>
                <div className="w-11 h-6 bg-indigo-600 rounded-full relative cursor-pointer">
                  <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full shadow-sm"></div>
                </div>
              </div>
            </div>

            {/* Capture Settings */}
            <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800 space-y-3">
              <h4 className="text-sm font-medium text-slate-200">Capture Mode</h4>
              <div className="grid grid-cols-2 gap-2">
                <button className="p-3 bg-indigo-600/10 border border-indigo-500/50 rounded-lg text-left">
                  <div className="text-xs font-bold text-indigo-300">Active Window</div>
                  <div className="text-[10px] text-slate-400">Capture focused app only</div>
                </button>
                <button className="p-3 bg-slate-800 border border-slate-700 rounded-lg text-left opacity-60">
                  <div className="text-xs font-bold text-slate-300">Full Screen</div>
                  <div className="text-[10px] text-slate-500">Entire monitor</div>
                </button>
              </div>
            </div>
          </div>
        );

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
                  <option value="chimera">Chimera Server (Default - No setup required)</option>
                  <option value="openai">OpenAI (GPT-4o)</option>
                  <option value="anthropic">Anthropic (Claude 3.5)</option>
                  <option value="google">Google (Gemini 1.5 Pro)</option>
                  <option value="local">Local (Ollama / LM Studio)</option>
                </select>
              </div>

              {provider === 'chimera' && (
                <div className="bg-indigo-600/10 border border-indigo-500/30 rounded-lg p-4">
                  <div className="flex items-start gap-3">
                    <Shield size={20} className="text-indigo-400 mt-0.5" />
                    <div>
                      <h4 className="text-sm font-medium text-indigo-200 mb-1">Using Chimera Server</h4>
                      <p className="text-xs text-slate-400 leading-relaxed">
                        Your requests are processed by our managed infrastructure. No API keys needed.
                        Works with any desktop application - from VS Code to PowerPoint.
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {provider === 'local' ? (
                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-300 flex items-center gap-2">
                    <Globe size={14} className="text-emerald-400" /> Base URL
                  </label>
                  <input
                    type="text"
                    placeholder="http://localhost:11434"
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:ring-2 focus:ring-indigo-500 outline-none"
                  />
                  <p className="text-xs text-slate-500">Point to your local inference server (Ollama, LM Studio, etc.)</p>
                </div>
              ) : provider !== 'chimera' ? (
                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-300 flex items-center gap-2">
                    <Key size={14} className="text-amber-400" /> API Key
                  </label>
                  <div className="relative">
                    <input
                      type="password"
                      placeholder={`Your ${provider} API key`}
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:ring-2 focus:ring-indigo-500 outline-none pr-10"
                    />
                    <div className="absolute right-3 top-2.5 text-slate-500 text-xs">HIDDEN</div>
                  </div>
                  <p className="text-xs text-slate-500">Your key is stored locally and encrypted.</p>
                </div>
              ) : null}
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">Vision Model (for screenshot analysis)</label>
              <div className="grid grid-cols-2 gap-3">
                <div className="p-3 bg-indigo-600/10 border border-indigo-500/50 rounded-lg cursor-pointer">
                  <div className="text-xs font-bold text-indigo-300">GPT-4o</div>
                  <div className="text-[10px] text-slate-400">Best for code & UI analysis</div>
                </div>
                <div className="p-3 bg-slate-800 border border-slate-700 rounded-lg cursor-pointer opacity-60">
                  <div className="text-xs font-bold text-slate-300">Claude 3.5</div>
                  <div className="text-[10px] text-slate-500">Strong reasoning</div>
                </div>
              </div>
            </div>
          </div>
        );

      case 'Privacy':
        return (
          <div className="space-y-6 animate-fade-in">
            <h3 className="text-sm uppercase tracking-wider text-slate-500 font-bold mb-4">Privacy & Data</h3>
            <div className="space-y-4">
              <div className="bg-slate-950/50 rounded-xl border border-slate-800 p-4">
                <h4 className="text-sm font-medium text-slate-200 mb-3 flex items-center gap-2">
                  <Shield size={16} className="text-indigo-400" />
                  Screenshot Handling
                </h4>
                <div className="space-y-3">
                  <label className="flex items-center justify-between">
                    <span className="text-sm text-slate-300">Never store screenshots on server</span>
                    <input type="checkbox" defaultChecked className="rounded" />
                  </label>
                  <label className="flex items-center justify-between">
                    <span className="text-sm text-slate-300">Delete screenshots after analysis</span>
                    <input type="checkbox" defaultChecked className="rounded" />
                  </label>
                  <label className="flex items-center justify-between">
                    <span className="text-sm text-slate-300">Blur sensitive areas (experimental)</span>
                    <input type="checkbox" className="rounded" />
                  </label>
                </div>
              </div>
              <div className="bg-indigo-600/10 border border-indigo-500/30 rounded-lg p-4">
                <p className="text-xs text-slate-400 leading-relaxed">
                  Chimera is designed with privacy in mind. Screenshots are processed temporarily for analysis and immediately discarded.
                  We do not train models on your data or retain any application information.
                </p>
              </div>
            </div>
          </div>
        );

      case 'Shortcuts':
        return (
          <div className="space-y-6 animate-fade-in">
            <h3 className="text-sm uppercase tracking-wider text-slate-500 font-bold mb-4">Keyboard Shortcuts</h3>
            <div className="space-y-2">
              {[
                { key: 'Ctrl+Shift+C', action: 'Capture active window' },
                { key: 'Ctrl+Shift+V', action: 'Toggle Chimera visibility' },
                { key: 'Ctrl+Shift+A', action: 'Quick ask with last screenshot' },
                { key: 'Esc', action: 'Close overlay/widget' },
              ].map(({ key, action }) => (
                <div key={key} className="flex items-center justify-between p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                  <span className="text-sm text-slate-300">{action}</span>
                  <kbd className="px-2 py-1 text-xs font-mono bg-slate-800 border border-slate-700 rounded">{key}</kbd>
                </div>
              ))}
            </div>
          </div>
        );

      case 'About':
        return (
          <div className="space-y-6 animate-fade-in">
            <h3 className="text-sm uppercase tracking-wider text-slate-500 font-bold mb-4">About Chimera</h3>
            <div className="text-center py-8">
              <div className="flex justify-center mb-4">
                <div className="w-16 h-16 bg-indigo-600 rounded-2xl flex items-center justify-center">
                  <Cpu size={32} className="text-white" />
                </div>
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Chimera Desktop Assistant</h3>
              <p className="text-sm text-slate-400 mb-4">Version 1.0.0</p>
              <p className="text-xs text-slate-500 max-w-md mx-auto leading-relaxed">
                Universal AI assistant for any desktop application. Take a screenshot, ask a question, get instant help.
              </p>
              <div className="mt-6 pt-6 border-t border-slate-800">
                <p className="text-xs text-slate-600">
                  Made with ❤️ by the Chimera Team
                </p>
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
            {['General', 'Providers', 'Privacy', 'Shortcuts', 'About'].map((item) => (
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

// Green Border Overlay Component
const GreenBorderOverlay = ({ isMonitoring, selectedScreen }) => {
  if (!isMonitoring) return null;

  return (
    <div className="fixed inset-0 pointer-events-none z-[9999]">
      {/* Green border indicator */}
      <div className="absolute inset-0 border-4 border-green-500/60 shadow-[inset_0_0_20px_rgba(34,197,94,0.3)] animate-pulse-border"></div>

      {/* Top indicator badge */}
      <div className="absolute top-4 left-1/2 transform -translate-x-1/2 bg-green-500/90 backdrop-blur-sm px-4 py-2 rounded-full shadow-lg">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
          <span className="text-xs font-bold text-white">CHIMERA MONITORING</span>
        </div>
      </div>
    </div>
  );
};

// --- Main App Component ---

export default function ChimeraLauncher() {
  const [showSettings, setShowSettings] = useState(false);
  const [messages, setMessages] = useState(MOCK_MESSAGES);
  const [inputText, setInputText] = useState('');
  const [isCapturing, setIsCapturing] = useState(false);
  const [selectedContext, setSelectedContext] = useState('vscode');
  const [widgetExpanded, setWidgetExpanded] = useState(false);
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [selectedScreen, setSelectedScreen] = useState('screen-0');

  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const newMsg = {
      id: messages.length + 1,
      sender: 'user',
      text: inputText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages([...messages, newMsg]);
    setInputText('');

    // TODO: Replace with actual API call
    setTimeout(() => {
      setMessages(prev => [...prev, {
        id: prev.length + 1,
        sender: 'ai',
        text: "I've analyzed your screen. Based on what I see, here's what you can do:\n\nStep 1: Check the syntax on the highlighted line\nStep 2: Ensure all imports are correct\nStep 3: Verify the function signature matches usage",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    }, 1500);
  };

  const captureScreen = async () => {
    setIsCapturing(true);

    try {
      // TODO: Implement actual screen capture based on selectedScreen
      // For web: navigator.mediaDevices.getDisplayMedia()
      // For desktop (Tauri/Electron): use native APIs

      setTimeout(() => setIsCapturing(false), 800);
    } catch (error) {
      console.error('Screen capture failed:', error);
      setIsCapturing(false);
    }
  };

  const toggleMonitoring = () => {
    setIsMonitoring(!isMonitoring);
  };

  // Get currently selected screen info
  const currentScreen = MOCK_SCREENS.find(s => s.id === selectedScreen) || MOCK_SCREENS[0];

  return (
    <div className="flex h-screen bg-slate-950 text-slate-200 font-sans selection:bg-indigo-500/30 overflow-hidden">
      {/* Green Border Overlay */}
      <GreenBorderOverlay isMonitoring={isMonitoring} selectedScreen={selectedScreen} />

      {/* --- Left Sidebar: Navigation & History --- */}
      <aside className="w-[280px] bg-slate-900 border-r border-slate-800 flex flex-col flex-shrink-0 z-20">
        <div className="h-16 flex items-center px-6 border-b border-slate-800">
          <div className="flex items-center gap-2 text-indigo-400">
            <Cpu size={24} className="animate-pulse-slow" />
            <h1 className="text-xl font-bold tracking-tight text-white">CHIMERA</h1>
          </div>
        </div>

        <div className="p-4">
          <button className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white py-3 rounded-xl transition-all shadow-lg shadow-indigo-900/20 font-medium">
            <Monitor size={18} />
            <span>New Session</span>
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-4 pb-4 space-y-6 custom-scrollbar">
          <div>
            <div className="flex items-center justify-between mb-3 px-2">
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Application Contexts</h3>
            </div>
            <div className="space-y-1 max-h-64 overflow-y-auto custom-scrollbar">
              {APP_CONTEXTS.map((app) => (
                <div
                  key={app.id}
                  onClick={() => setSelectedContext(app.id)}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer text-sm transition-colors ${selectedContext === app.id ? 'bg-slate-800 text-white ring-1 ring-slate-700' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'}`}
                  title={app.desc}
                >
                  <app.icon size={16} className={selectedContext === app.id ? app.color : 'text-slate-500'} />
                  <span className="flex-1 truncate">{app.name}</span>
                  {selectedContext === app.id && <div className="w-1.5 h-1.5 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]"></div>}
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
                {MOCK_SESSIONS[0].title}
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-500/20 text-blue-400 border border-blue-500/30">
                  {MOCK_SESSIONS[0].app.toUpperCase()}
                </span>
              </h2>
              <span className="text-xs text-slate-500 flex items-center gap-1">
                <span className={`w-1.5 h-1.5 rounded-full ${isMonitoring ? 'bg-green-500 animate-pulse' : 'bg-slate-600'}`}></span>
                {isMonitoring ? `Monitoring ${currentScreen.name}` : 'Idle'}
              </span>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={toggleMonitoring}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                isMonitoring
                  ? 'bg-green-600 text-white hover:bg-green-500'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              {isMonitoring ? <Pause size={16} /> : <Play size={16} />}
              {isMonitoring ? 'Stop' : 'Start'} Monitoring
            </button>
            <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors">
              <MoreVertical size={20} />
            </button>
          </div>
        </header>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto p-6 scroll-smooth custom-scrollbar">
          <div className="max-w-3xl mx-auto">
            {messages.map(msg => <MessageBubble key={msg.id} message={msg} />)}
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
              <button className="p-1.5 text-slate-400 hover:text-indigo-400 rounded-md hover:bg-slate-800" title="Upload image">
                <ImageIcon size={16} />
              </button>
              <button className="p-1.5 text-slate-400 hover:text-indigo-400 rounded-md hover:bg-slate-800" title="Share code snippet">
                <Code size={16} />
              </button>
              <div className="ml-auto text-[10px] text-slate-600 flex items-center gap-2">
                <Monitor size={12} />
                {currentScreen.name}
              </div>
            </div>
            <div className="flex items-end p-3 gap-3">
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSendMessage())}
                placeholder="Ask Chimera about your screen... (works with any app!)"
                className="flex-1 bg-transparent border-none outline-none text-slate-200 placeholder:text-slate-600 resize-none max-h-32 min-h-[44px] py-2 text-sm"
                rows={1}
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputText.trim()}
                className={`p-2.5 rounded-xl transition-all ${inputText.trim() ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20 hover:scale-105' : 'bg-slate-800 text-slate-600 cursor-not-allowed'}`}
              >
                <Send size={18} />
              </button>
            </div>
          </div>
          <p className="text-center text-xs text-slate-600 mt-3">
            Chimera works with any desktop app - VS Code, Office, browsers, design tools, and more.
          </p>
        </div>
      </main>

      {/* --- Right Panel: Live Context & Tools --- */}
      <aside className="w-[320px] bg-slate-900 border-l border-slate-800 flex flex-col z-20">
        <div className="p-4 border-b border-slate-800">
          <h3 className="text-sm font-bold text-slate-200 mb-3 flex items-center gap-2">
            <Monitor size={16} className="text-indigo-500" />
            Live Preview
          </h3>

          <div className="relative group rounded-xl overflow-hidden border border-slate-700 bg-slate-950 aspect-video mb-4">
            {/* Simulated Screen Preview */}
            <div className="absolute inset-0 bg-slate-800 flex items-center justify-center">
              <img
                src="https://images.unsplash.com/photo-1587620962725-abab7fe55159?q=80&w=1000&auto=format&fit=crop"
                className={`w-full h-full object-cover transition-opacity duration-300 ${isCapturing ? 'opacity-50' : 'opacity-80'}`}
                alt="Screen Context"
              />
              {isCapturing && (
                <div className="absolute inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm">
                  <div className="w-8 h-8 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                </div>
              )}
              {isMonitoring && (
                <div className="absolute top-2 left-2 bg-green-500/90 px-2 py-1 rounded-full flex items-center gap-1">
                  <div className="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></div>
                  <span className="text-[9px] font-bold text-white">LIVE</span>
                </div>
              )}
            </div>

            <div className="absolute bottom-2 right-2 flex gap-1">
              <span className="px-2 py-1 bg-black/60 backdrop-blur text-[10px] text-white rounded font-mono">{currentScreen.resolution}</span>
            </div>
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
          {/* Analysis Section */}
          <div>
            <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">AI Analysis</h4>
            <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-800 space-y-3">
              <div className="flex items-start gap-3">
                <div className="mt-1 p-1 bg-blue-500/20 rounded text-blue-400"><Code size={14} /></div>
                <div>
                  <div className="text-xs font-medium text-slate-300">Context Detected</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">
                    {APP_CONTEXTS.find(a => a.id === selectedContext)?.name || 'Unknown App'}
                  </div>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="mt-1 p-1 bg-orange-500/20 rounded text-orange-400"><Zap size={14} /></div>
                <div>
                  <div className="text-xs font-medium text-slate-300">Ready to Assist</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">Ask anything about your screen</div>
                </div>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div>
            <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Quick Actions</h4>
            <div className="space-y-2">
              <button className="w-full text-left px-3 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs text-slate-300 border border-slate-700 transition-colors flex items-center justify-between group">
                <span>Explain what's on screen</span>
                <ChevronRight size={14} className="text-slate-500 group-hover:text-white" />
              </button>
              <button className="w-full text-left px-3 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs text-slate-300 border border-slate-700 transition-colors flex items-center justify-between group">
                <span>Find errors or issues</span>
                <ChevronRight size={14} className="text-slate-500 group-hover:text-white" />
              </button>
              <button className="w-full text-left px-3 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs text-slate-300 border border-slate-700 transition-colors flex items-center justify-between group">
                <span>Suggest improvements</span>
                <ChevronRight size={14} className="text-slate-500 group-hover:text-white" />
              </button>
            </div>
          </div>
        </div>

        {/* System Status Footer */}
        <div className="p-3 bg-slate-900 border-t border-slate-800 text-[10px] text-slate-500 flex justify-between items-center">
          <span>Memory: 1.2GB / 16GB</span>
          <div className="flex items-center gap-1">
            <div className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></div>
            <span>Server Online</span>
          </div>
        </div>
      </aside>

      {/* --- Floating Companion Widget --- */}
      <div className="fixed bottom-6 right-8 z-50 flex flex-col items-end pointer-events-none">
        <div className={`bg-slate-800 border border-slate-700 rounded-2xl shadow-2xl mb-4 overflow-hidden transition-all duration-300 origin-bottom-right pointer-events-auto ${widgetExpanded ? 'w-80 opacity-100 scale-100' : 'w-0 h-0 opacity-0 scale-95'}`}>
          <div className="p-3 bg-slate-900 border-b border-slate-700 flex justify-between items-center">
            <span className="text-xs font-bold text-white flex items-center gap-2">
              <Bot size={14} className="text-indigo-500" /> Quick Assist
            </span>
            <button onClick={() => setWidgetExpanded(false)} className="text-slate-500 hover:text-white">
              <X size={14} />
            </button>
          </div>
          <div className="p-4 space-y-3">
            <div className="bg-slate-900 rounded-lg p-2 border border-slate-700 h-24 flex items-center justify-center text-slate-600 text-xs">
              Drag screenshot here
            </div>
            <textarea className="w-full bg-slate-900 border-slate-700 rounded-lg p-2 text-xs text-slate-200 resize-none focus:ring-1 focus:ring-indigo-500 outline-none" rows={2} placeholder="Quick question..."></textarea>
            <button className="w-full bg-indigo-600 hover:bg-indigo-500 text-white py-1.5 rounded-lg text-xs font-medium transition-colors">
              Ask Chimera
            </button>
          </div>
        </div>

        <button
          onClick={() => setWidgetExpanded(!widgetExpanded)}
          className={`pointer-events-auto w-12 h-12 rounded-full shadow-lg shadow-indigo-900/40 flex items-center justify-center transition-all duration-300 hover:scale-110 ${widgetExpanded ? 'bg-slate-700 text-white rotate-45' : 'bg-indigo-600 text-white rotate-0'}`}
        >
          {widgetExpanded ? <X size={24} /> : <Bot size={24} />}
        </button>
      </div>

      <SettingsModal
        isOpen={showSettings}
        onClose={() => setShowSettings(false)}
        selectedScreen={selectedScreen}
        setSelectedScreen={setSelectedScreen}
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
        @keyframes pulse-border {
          0%, 100% {
            opacity: 0.6;
            box-shadow: inset 0 0 20px rgba(34, 197, 94, 0.3);
          }
          50% {
            opacity: 0.8;
            box-shadow: inset 0 0 30px rgba(34, 197, 94, 0.5);
          }
        }
        .animate-pulse-border {
          animation: pulse-border 2s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
}
