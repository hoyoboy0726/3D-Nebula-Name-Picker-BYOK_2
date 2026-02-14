import React, { useState, useEffect } from 'react';
import { Key, Eye, EyeOff, CheckCircle2, AlertCircle } from 'lucide-react';

interface ApiKeyInputProps {
  onApiKeyChange: (key: string) => void;
}

const ApiKeyInput: React.FC<ApiKeyInputProps> = ({ onApiKeyChange }) => {
  const [apiKey, setApiKey] = useState('');
  const [isVisible, setIsVisible] = useState(false);
  const [isSaved, setIsSaved] = useState(false);

  useEffect(() => {
    const savedKey = localStorage.getItem('gemini_api_key') || '';
    setApiKey(savedKey);
    onApiKeyChange(savedKey);
  }, [onApiKeyChange]);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    localStorage.setItem('gemini_api_key', apiKey);
    onApiKeyChange(apiKey);
    setIsSaved(true);
    setTimeout(() => setIsSaved(false), 2000);
  };

  return (
    <div className="flex flex-col items-end gap-2 group">
      <form 
        onSubmit={handleSave}
        className="flex items-center gap-2 bg-zinc-900/60 backdrop-blur-md px-3 py-2 rounded-2xl border border-white/10 shadow-xl transition-all duration-300 hover:border-blue-500/50"
      >
        <Key className={`w-4 h-4 ${apiKey ? 'text-blue-400' : 'text-gray-500'}`} />
        <div className="relative flex items-center">
          <input
            type={isVisible ? 'text' : 'password'}
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Gemini API Key"
            className="bg-transparent border-none outline-none text-xs text-gray-200 placeholder:text-gray-600 w-32 md:w-48 transition-all focus:w-40 md:focus:w-64"
          />
          <button
            type="button"
            onClick={() => setIsVisible(!isVisible)}
            className="absolute right-0 text-gray-500 hover:text-gray-300 transition-colors"
          >
            {isVisible ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
          </button>
        </div>
        <button
          type="submit"
          className={`p-1.5 rounded-lg transition-all ${
            isSaved ? 'bg-green-500/20 text-green-400' : 'hover:bg-white/10 text-gray-400 hover:text-white'
          }`}
        >
          {isSaved ? <CheckCircle2 className="w-4 h-4" /> : <span className="text-[10px] font-bold px-1">SAVE</span>}
        </button>
      </form>
      
      {!apiKey && (
        <div className="flex items-center gap-1.5 px-2 text-[10px] text-orange-400/80 font-medium animate-pulse">
          <AlertCircle className="w-3 h-3" />
          未輸入金鑰：將使用低階發音功能
        </div>
      )}
      {apiKey && (
        <div className="flex items-center gap-1.5 px-2 text-[10px] text-blue-400/80 font-medium">
          <div className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse" />
          AI 語音功能已啟用
        </div>
      )}
    </div>
  );
};

export default ApiKeyInput;
