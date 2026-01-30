import { useState, useRef, useEffect } from 'react';
import { queryLoanInsights } from '../services/loanInsightsApi';

const ChatMessage = ({ message, isUser }) => {
    const isGoldenKB = message.source === 'golden_kb';

    return (
        <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-fadeIn`}>
            {/* Message Bubble Container */}
            <div className={`group flex ${isUser ? 'flex-row-reverse' : 'flex-row'} items-end max-w-[85%] lg:max-w-[70%]`}>

                {/* Avatar */}
                <div className={`flex-shrink-0 mb-1 ${isUser ? 'hidden' : 'mr-3'}`}>
                    <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shadow-md">
                        <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                        </svg>
                    </div>
                </div>

                {/* Bubble */}
                <div
                    className={`relative px-5 py-3.5 shadow-sm text-sm md:text-[15px] leading-relaxed 
                    ${isUser
                            ? 'bg-blue-600 text-white rounded-2xl rounded-br-sm'
                            : isGoldenKB
                                ? 'bg-gradient-to-b from-yellow-50 to-white text-gray-800 border border-yellow-200 rounded-2xl rounded-bl-sm'
                                : 'bg-white text-gray-800 border border-gray-100 rounded-2xl rounded-bl-sm'
                        }`}
                >
                    {/* Golden KB Badge */}
                    {isGoldenKB && (
                        <div className="flex items-center space-x-1.5 mb-2 pb-2 border-b border-yellow-200/60">
                            <svg className="w-3.5 h-3.5 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                            </svg>
                            <span className="text-[10px] font-bold uppercase tracking-wider text-yellow-700">Verified Answer</span>
                        </div>
                    )}

                    {/* Content */}
                    <div className="whitespace-pre-wrap">{message.content}</div>

                    {/* Evidence Points */}
                    {message.evidence_points && message.evidence_points.length > 0 && (
                        <div className="mt-3 pt-2 space-y-1">
                            {message.evidence_points.slice(0, 3).map((point, idx) => (
                                <div key={idx} className="flex items-start text-xs text-gray-600 bg-gray-50/50 p-1.5 rounded">
                                    <span className="text-blue-500 mr-2 mt-0.5">●</span>
                                    <span>{point}</span>
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Risk Factors */}
                    {message.risk_notes && message.risk_notes.length > 0 && (
                        <div className="mt-2 pt-2 border-t border-red-100">
                            <div className="flex items-center text-xs font-bold text-red-600 mb-1">
                                <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                                Risk Factors
                            </div>
                            {message.risk_notes.slice(0, 2).map((note, idx) => (
                                <div key={idx} className="text-xs text-red-600/90 pl-4 relative">
                                    <span className="absolute left-0 top-1.5 w-1 h-1 bg-red-400 rounded-full"></span>
                                    {note}
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Timestamp */}
                    <div className={`text-[10px] mt-1.5 text-right opacity-60 ${isUser ? 'text-white' : 'text-gray-500'}`}>
                        {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                </div>
            </div>
        </div>
    );
};

const ConversationalChat = () => {
    const [messages, setMessages] = useState([
        {
            id: 1,
            content: "Hello! I'm your Loan Insight Assistant. I can help you understand loan approval patterns, analyze rejection reasons, and provide insights based on historical data. What would you like to know?",
            isUser: false,
            timestamp: new Date(),
            source: 'system'
        }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const suggestedQuestions = [
        "What is a good CIBIL score?",
        "Why are home loans rejected?",
        "What factors affect loan approval?",
        "How is DTI ratio calculated?"
    ];

    const handleSend = async (messageText = inputValue) => {
        if (!messageText.trim() || isLoading) return;

        const userMessage = {
            id: messages.length + 1,
            content: messageText.trim(),
            isUser: true,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            // Prepare conversation history (last 5 messages for context)
            const conversationHistory = messages.slice(-5).map(msg => ({
                role: msg.isUser ? 'user' : 'assistant',
                content: msg.content
            }));

            const response = await queryLoanInsights(messageText, conversationHistory);

            const assistantMessage = {
                id: messages.length + 2,
                content: response.answer || response.explanation,
                isUser: false,
                timestamp: new Date(),
                evidence_points: response.evidence_points,
                risk_notes: response.risk_notes,
                source: response.source || 'rag'
            };

            setMessages(prev => [...prev, assistantMessage]);
        } catch (error) {
            const errorMessage = {
                id: messages.length + 2,
                content: "I apologize, but I encountered an error processing your request. Please try again.",
                isUser: false,
                timestamp: new Date(),
                source: 'error'
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
            inputRef.current?.focus();
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const handleClearChat = () => {
        setMessages([
            {
                id: 1,
                content: "Chat cleared! How can I help you today?",
                isUser: false,
                timestamp: new Date(),
                source: 'system'
            }
        ]);
    };

    return (
        <div className="flex flex-col h-[calc(100vh-200px)] bg-gradient-to-br from-gray-50 to-blue-50 rounded-2xl shadow-xl overflow-hidden">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-4 shadow-lg">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm">
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                            </svg>
                        </div>
                        <div>
                            <h2 className="text-lg font-bold">AI Loan Assistant</h2>
                            <p className="text-xs text-blue-100">Powered by RAG & Golden KB</p>
                        </div>
                    </div>
                    <button
                        onClick={handleClearChat}
                        className="px-3 py-1.5 bg-white/20 hover:bg-white/30 rounded-lg text-sm font-medium transition-colors backdrop-blur-sm"
                    >
                        Clear Chat
                    </button>
                </div>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
                {messages.map((message) => (
                    <ChatMessage key={message.id} message={message} isUser={message.isUser} />
                ))}

                {isLoading && (
                    <div className="flex justify-start mb-4">
                        <div className="bg-white border border-gray-200 rounded-2xl px-5 py-3 shadow-md">
                            <div className="flex space-x-2">
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Suggested Questions (show when no messages except welcome) */}
            {messages.length === 1 && (
                <div className="px-6 py-3 bg-white/50 backdrop-blur-sm border-t border-gray-200">
                    <p className="text-xs font-semibold text-gray-600 mb-2">Suggested Questions:</p>
                    <div className="flex flex-wrap gap-2">
                        {suggestedQuestions.map((question, idx) => (
                            <button
                                key={idx}
                                onClick={() => handleSend(question)}
                                className="px-3 py-1.5 bg-white hover:bg-blue-50 border border-gray-300 hover:border-blue-400 rounded-full text-xs text-gray-700 hover:text-blue-700 transition-all shadow-sm hover:shadow"
                            >
                                {question}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* Input Area */}
            <div className="bg-white border-t border-gray-200 px-6 py-4">
                <div className="flex items-end space-x-3">
                    <div className="flex-1 relative">
                        <textarea
                            ref={inputRef}
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Ask about loan approvals, rejections, CIBIL scores..."
                            rows={1}
                            disabled={isLoading}
                            className="w-full px-4 py-3 pr-12 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none disabled:bg-gray-100 disabled:cursor-not-allowed text-sm"
                            style={{ minHeight: '48px', maxHeight: '120px' }}
                        />
                        <div className="absolute right-3 bottom-3 text-xs text-gray-400">
                            {inputValue.length > 0 && `${inputValue.length} chars`}
                        </div>
                    </div>
                    <button
                        onClick={() => handleSend()}
                        disabled={!inputValue.trim() || isLoading}
                        className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-xl font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl flex items-center space-x-2"
                    >
                        <span>Send</span>
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                        </svg>
                    </button>
                </div>
                <p className="text-xs text-gray-500 mt-2">
                    Press Enter to send • Shift+Enter for new line
                </p>
            </div>
        </div>
    );
};

export default ConversationalChat;
