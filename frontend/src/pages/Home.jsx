import { useState } from "react";
import Sidebar from "../components/Sidebar";
import Dashboard from "../components/Dashboard";
import Analytics from "../components/Analytics";
import QueryInput from "../components/QueryInput";
import ResponseCard from "../components/ResponseCard";
import ConversationalChat from "../components/ConversationalChat";
import { queryLoanInsights } from "../services/loanInsightsApi";

const Home = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  const handleSubmit = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setError("");
    setResponse(null);

    try {
      const data = await queryLoanInsights(question);
      setResponse(data);
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'analytics':
        return <Analytics />;
      case 'query':
        return (
          <div className="space-y-6 h-[calc(100vh-140px)]">
            <ConversationalChat />
          </div>
        );
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen mesh-gradient">
      {/* Mobile Sidebar Overlay */}
      {isMobileSidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-70 z-20 lg:hidden backdrop-blur-sm"
          onClick={() => setIsMobileSidebarOpen(false)}
        ></div>
      )}

      {/* Sidebar */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={(tab) => {
          setActiveTab(tab);
          setIsMobileSidebarOpen(false);
        }}
        isOpen={isMobileSidebarOpen}
      />

      {/* Main Content */}
      <div className="lg:ml-64 transition-all duration-200">
        {/* Top Bar */}
        <div className="glass-dark border-b border-white/10 px-4 md:px-8 py-4 sticky top-0 z-10">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              {/* Mobile Menu Button */}
              <button
                className="mr-4 lg:hidden p-2 rounded-lg hover:bg-white/10 transition-colors"
                onClick={() => setIsMobileSidebarOpen(true)}
              >
                <svg className="w-6 h-6 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>

              <div>
                <h1 className="text-xl md:text-2xl font-bold gradient-text">
                  {activeTab === 'dashboard' && 'Dashboard'}
                  {activeTab === 'analytics' && 'Analytics'}
                  {activeTab === 'query' && 'Query Assistant'}
                </h1>
                <p className="text-xs md:text-sm text-gray-400 mt-1 hidden md:block">
                  {new Date().toLocaleDateString('en-US', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </p>
              </div>
            </div>


          </div>
        </div>

        {/* Page Content */}
        <div className="p-4 md:p-8">
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default Home;
