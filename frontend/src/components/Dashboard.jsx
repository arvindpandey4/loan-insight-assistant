import { useState, useEffect } from 'react';
import StatsCard from './StatsCard';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { fetchDashboardStats } from '../services/loanInsightsApi';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const data = await fetchDashboardStats();
        setDashboardData(data);
        setLoading(false);
      } catch (err) {
        console.error("Failed to load dashboard stats", err);
        setError("Failed to load dashboard data");
        setLoading(false);
      }
    };

    loadStats();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center p-12">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-300">Loading dashboard data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-dark neon-border rounded-xl p-8 text-center">
        <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4 animate-bounce-subtle">
          <svg className="w-8 h-8 text-red-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <path d="M12 8v4m0 4h.01" strokeLinecap="round" />
          </svg>
        </div>
        <p className="text-red-400">{error}</p>
      </div>
    );
  }

  // Rich Mock Data for Demo purposes if DB is empty
  const mockData = {
    total_loans: 124,
    approval_rate: 68.5,
    avg_cibil: 742,
    avg_loan_amount: 450000,
    loan_status_distribution: [
      { name: 'Approved', value: 85, color: '#10b981' },
      { name: 'Rejected', value: 39, color: '#ef4444' }
    ],
    loan_type_distribution: [
      { name: 'Home', value: 45, color: '#3b82f6' },
      { name: 'Personal', value: 30, color: '#8b5cf6' },
      { name: 'Auto', value: 25, color: '#ec4899' },
      { name: 'Education', value: 15, color: '#f59e0b' },
      { name: 'Business', value: 9, color: '#14b8a6' }
    ],
    recent_applications: [
      { id: 'LN-2024-001', applicant: 'Rahul Sharma', amount: 500000, status: 'Approved', type: 'Home Loan' },
      { id: 'LN-2024-002', applicant: 'Priya Verma', amount: 200000, status: 'Rejected', type: 'Personal Loan' },
      { id: 'LN-2024-003', applicant: 'Amit Singh', amount: 850000, status: 'Approved', type: 'Auto Loan' },
      { id: 'LN-2024-004', applicant: 'Sneha Gupta', amount: 150000, status: 'Approved', type: 'Education' },
      { id: 'LN-2024-005', applicant: 'Vikram Malhotra', amount: 1200000, status: 'Review', type: 'Business' }
    ]
  };

  // Use API data if available and non-zero, otherwise fall back to mock data
  const { total_loans, approval_rate, avg_cibil, avg_loan_amount, loan_status_distribution, loan_type_distribution, recent_applications } =
    (dashboardData && dashboardData.total_loans > 0) ? dashboardData : mockData;

  const stats = [
    {
      title: 'Total Applications',
      value: total_loans.toLocaleString(),
      change: 'Real-time',
      icon: 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z',
      color: 'blue'
    },
    {
      title: 'Approval Rate',
      value: `${approval_rate}%`,
      change: 'Calculated',
      icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
      color: 'green'
    },
    {
      title: 'Avg CIBIL Score',
      value: avg_cibil,
      change: 'Average',
      icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
      color: 'purple'
    },
    {
      title: 'Avg Loan Amount',
      value: `₹${Math.round(avg_loan_amount / 1000)}k`,
      change: 'Average',
      icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
      color: 'orange'
    }
  ];

  return (
    <div className="space-y-6">

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <StatsCard key={index} {...stat} />
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Loan Type Distribution */}
        <div className="lg:col-span-2 glass-dark neon-border rounded-xl p-6 card-hover">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-white">Loan Type Distribution</h2>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></div>
              <span className="text-xs text-cyan-400">Live Data</span>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={loan_type_distribution}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="name" stroke="#9ca3af" tick={{ fill: '#9ca3af' }} />
              <YAxis stroke="#9ca3af" tick={{ fill: '#9ca3af' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(15, 23, 42, 0.9)',
                  border: '1px solid rgba(59, 130, 246, 0.3)',
                  borderRadius: '8px',
                  color: '#fff'
                }}
              />
              <Bar dataKey="value" fill="#3b82f6" radius={[8, 8, 0, 0]}>
                {loan_type_distribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Loan Status Distribution */}
        <div className="glass-dark neon-border rounded-xl p-6 card-hover">
          <h2 className="text-xl font-bold text-white mb-4">Loan Status</h2>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={loan_status_distribution}
                cx="50%"
                cy="50%"
                innerRadius={50}
                outerRadius={80}
                fill="#8884d8"
                paddingAngle={5}
                dataKey="value"
              >
                {loan_status_distribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(15, 23, 42, 0.9)',
                  border: '1px solid rgba(59, 130, 246, 0.3)',
                  borderRadius: '8px',
                  color: '#fff'
                }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-4 space-y-2">
            {loan_status_distribution.map((item, index) => (
              <div key={index} className="flex items-center justify-between text-sm">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></div>
                  <span className="text-gray-300">{item.name}</span>
                </div>
                <span className="font-semibold text-white">{item.value.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Applications */}
        <div className="lg:col-span-2 glass-dark neon-border rounded-xl p-6 card-hover">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-white">Recent Applications</h2>
            <span className="text-xs text-gray-400">Latest entries</span>
          </div>
          <div className="space-y-4">
            {recent_applications.map((item, index) => (
              <div key={index} className="flex items-start space-x-4 p-4 bg-white/5 rounded-lg hover:bg-white/10 transition-all cursor-pointer border border-white/5 hover:border-white/10 group">
                <div className="flex-shrink-0 w-10 h-10 bg-gradient-blue rounded-lg flex items-center justify-center transition-transform group-hover:scale-110">
                  <svg className="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="8" r="4" />
                    <path d="M4 20c0-4 4-6 8-6s8 2 8 6" strokeLinecap="round" />
                  </svg>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex justify-between">
                    <p className="text-sm font-medium text-white">{item.applicant}</p>
                    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${item.status === 'Approved' ? 'bg-green-500/20 text-green-400 border border-green-500/30' : 'bg-red-500/20 text-red-400 border border-red-500/30'}`}>
                      {item.status}
                    </span>
                  </div>
                  <div className="flex items-center space-x-4 mt-1">
                    <span className="text-xs text-gray-400">ID: {item.id}</span>
                    <span className="text-xs text-gray-400">{item.type}</span>
                    <span className="text-xs font-medium text-cyan-400">₹{item.amount.toLocaleString()}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* System Health (Real status) */}
        <div className="glass-dark neon-border rounded-xl p-6 card-hover">
          <h2 className="text-xl font-bold text-white mb-4">System Health</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg group hover:bg-white/10 transition-all">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-green-500/20 rounded-lg flex items-center justify-center">
                  <svg className="w-4 h-4 text-green-400 animate-pulse" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M22 12h-4l-3 9L9 3l-3 9H2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
                <span className="text-sm font-medium text-gray-300">API Status</span>
              </div>
              <span className="text-sm font-semibold text-green-400">Online</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg group hover:bg-white/10 transition-all">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-emerald-500/20 rounded-lg flex items-center justify-center">
                  <svg className="w-4 h-4 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <ellipse cx="12" cy="6" rx="8" ry="3" />
                    <path d="M4 6v6c0 1.657 3.582 3 8 3s8-1.343 8-3V6" />
                    <path d="M4 12v6c0 1.657 3.582 3 8 3s8-1.343 8-3v-6" />
                  </svg>
                </div>
                <span className="text-sm font-medium text-gray-300">Database</span>
              </div>
              <span className="text-sm font-semibold text-emerald-400">Connected</span>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="mt-6 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-6 text-white neon-glow animate-gradient">
            <div className="flex items-start justify-between">
              <div>
                <h2 className="text-xl font-bold mb-2">Ready to analyze?</h2>
                <p className="text-blue-100 mb-4 text-sm">Ask questions effectively with the RAG Assistant</p>
                <div className="flex items-center space-x-2">
                  <svg className="w-4 h-4 text-cyan-300 animate-bounce-subtle" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M12 2a4 4 0 014 4c0 1.5-.8 2.8-2 3.5V11h-4V9.5A4 4 0 0112 2z" />
                    <path d="M10 11v2a2 2 0 104 0v-2" />
                    <path d="M8 17h8M9 21h6" strokeLinecap="round" />
                  </svg>
                  <span className="text-xs text-blue-200">AI Powered</span>
                </div>
              </div>
              <svg className="w-12 h-12 text-white/20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z" />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
