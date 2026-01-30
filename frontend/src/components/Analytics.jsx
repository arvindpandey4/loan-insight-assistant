import {
  BarChart, Bar, PieChart, Pie, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell
} from 'recharts';
import { useState, useEffect } from 'react';
import { fetchLoanStatusDistribution, fetchAvgCIBIL } from '../services/loanInsightsApi';

const Analytics = () => {
  // Initialize directly with fallback/mock data to prevent initial empty state white-screen
  const [loanTypeData, setLoanTypeData] = useState([
    { name: 'Home', value: 35, color: '#3b82f6' },
    { name: 'Personal', value: 25, color: '#8b5cf6' },
    { name: 'Auto', value: 20, color: '#10b981' },
    { name: 'Education', value: 15, color: '#f59e0b' },
    { name: 'Business', value: 5, color: '#ec4899' },
  ]);
  const [loading, setLoading] = useState(false);

  const [trendData, setTrendData] = useState([
    { month: 'Jan', approved: 65, rejected: 35 },
    { month: 'Feb', approved: 72, rejected: 28 },
    { month: 'Mar', approved: 68, rejected: 32 },
    { month: 'Apr', approved: 85, rejected: 15 },
    { month: 'May', approved: 78, rejected: 22 },
    { month: 'Jun', approved: 82, rejected: 18 },
  ]);

  const [incomeData, setIncomeData] = useState([
    { range: '<30k', approved: 20, rejected: 80 },
    { range: '30-50k', approved: 45, rejected: 55 },
    { range: '50-80k', approved: 75, rejected: 25 },
    { range: '80k+', approved: 92, rejected: 8 },
  ]);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        // Attempt to fetch real data
        const statusData = await fetchLoanStatusDistribution().catch(() => null);

        if (statusData && Array.isArray(statusData.distribution)) {
          setLoanTypeData(statusData.distribution);
        }
        // If fetch fails, we simply keep the initial mock data
      } catch (err) {
        console.error("Analytics Load Error", err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  const handleExport = () => {
    try {
      if (!loanTypeData || loanTypeData.length === 0) return;
      const csvContent = "data:text/csv;charset=utf-8,"
        + "Metric,Value\n"
        + loanTypeData.map(e => `${e.name},${e.value}`).join("\n");

      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "analytics_report.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (e) {
      console.error("Export failed", e);
    }
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-slate-800/95 border border-slate-700 p-3 rounded-lg shadow-xl backdrop-blur-sm">
          <p className="text-gray-300 text-xs mb-1">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} className="text-sm font-semibold" style={{ color: entry.color }}>
              {entry.name}: {entry.value}%
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <div className="relative w-20 h-20">
          <div className="absolute top-0 left-0 w-full h-full border-4 border-blue-500/30 rounded-full animate-ping"></div>
          <div className="absolute top-0 left-0 w-full h-full border-4 border-t-blue-500 rounded-full animate-spin"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fadeIn">

      {/* Header Section */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-blue-200">
            Analytics & Trends
          </h1>
          <p className="text-slate-400 mt-1">Deep dive into loan performance metrics</p>
        </div>

        <button
          onClick={handleExport}
          className="px-5 py-2.5 bg-white/10 hover:bg-white/20 border border-white/10 rounded-xl text-sm font-medium text-white transition-all flex items-center gap-2 group backdrop-blur-md"
        >
          <svg className="w-4 h-4 text-blue-400 group-hover:text-blue-300 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Export CSV
        </button>
      </div>

      {/* Primary KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'Approval Rate', value: '72.4%', change: '+5.2%', color: 'from-green-500 to-emerald-700', icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' },
          { label: 'Avg Risk Score', value: 'Low', change: '-1.4%', color: 'from-blue-500 to-indigo-700', icon: 'M13 10V3L4 14h7v7l9-11h-7z' },
          { label: 'Total Volume', value: '1.2k', change: '+12%', color: 'from-purple-500 to-fuchsia-700', icon: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10' },
          { label: 'Processing Time', value: '24h', change: '-8%', color: 'from-orange-500 to-amber-700', icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z' }
        ].map((stat, i) => (
          <div key={i} className="group relative overflow-hidden bg-slate-800/40 border border-slate-700/50 p-5 rounded-2xl hover:bg-slate-800/60 transition-all duration-300">
            <div className={`absolute top-0 right-0 p-3 opacity-10 group-hover:opacity-20 transition-opacity`}>
              <div className={`w-16 h-16 rounded-full bg-gradient-to-br ${stat.color} blur-xl`}></div>
            </div>

            <div className="flex justify-between items-start mb-4">
              <div className={`p-2.5 rounded-xl bg-gradient-to-br ${stat.color} shadow-lg shadow-black/20`}>
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={stat.icon} />
                </svg>
              </div>
              <span className={`text-xs font-semibold px-2 py-1 rounded-full ${stat.change.startsWith('+') ? 'bg-green-500/10 text-green-400' : 'bg-blue-500/10 text-blue-400'}`}>
                {stat.change}
              </span>
            </div>

            <h3 className="text-2xl font-bold text-white mb-1">{stat.value}</h3>
            <p className="text-slate-400 text-sm font-medium">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Main Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Trend Analysis */}
        <div className="lg:col-span-2 bg-slate-800/40 border border-slate-700/50 rounded-2xl p-6 backdrop-blur-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-white">Approval Trends (6 Months)</h3>
            <div className="flex gap-2">
              <span className="flex items-center text-xs text-slate-400"><span className="w-2 h-2 rounded-full bg-emerald-500 mr-2"></span>Approved</span>
              <span className="flex items-center text-xs text-slate-400"><span className="w-2 h-2 rounded-full bg-rose-500 mr-2"></span>Rejected</span>
            </div>
          </div>

          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trendData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorApproved" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorRejected" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#f43f5e" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                <XAxis dataKey="month" stroke="#64748b" tick={{ fontSize: 12 }} tickLine={false} axisLine={false} />
                <YAxis stroke="#64748b" tick={{ fontSize: 12 }} tickLine={false} axisLine={false} />
                <Tooltip content={<CustomTooltip />} />
                <Area type="monotone" dataKey="approved" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorApproved)" name="Approved" />
                <Area type="monotone" dataKey="rejected" stroke="#f43f5e" strokeWidth={3} fillOpacity={1} fill="url(#colorRejected)" name="Rejected" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Loan Distribution */}
        <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-6 backdrop-blur-sm">
          <h3 className="text-lg font-semibold text-white mb-6">Portfolio Distribution</h3>

          <div className="h-[220px] w-full relative">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={loanTypeData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {loanTypeData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} stroke="rgba(0,0,0,0)" />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
              </PieChart>
            </ResponsiveContainer>

            {/* Center Stats */}
            <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
              <span className="text-3xl font-bold text-white">100%</span>
              <span className="text-xs text-slate-400 uppercase tracking-widest">Holdings</span>
            </div>
          </div>

          <div className="mt-6 space-y-3">
            {loanTypeData.map((item, idx) => (
              <div key={idx} className="flex items-center justify-between text-sm group">
                <div className="flex items-center gap-3">
                  <div className="w-2.5 h-2.5 rounded-full ring-2 ring-opacity-50 ring-offset-2 ring-offset-slate-900 transition-all group-hover:scale-125" style={{ backgroundColor: item.color, '--tw-ring-color': item.color }}></div>
                  <span className="text-slate-300 group-hover:text-white transition-colors">{item.name}</span>
                </div>
                <span className="font-semibold text-slate-400 group-hover:text-white transition-colors">{item.value}%</span>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Secondary Analysis Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* Income vs Approval */}
        <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-6">
          <h3 className="text-lg font-semibold text-white mb-6">Income Bracket Analysis</h3>
          <div className="h-[250px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={incomeData} layout="vertical" margin={{ left: 0, right: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" horizontal={false} />
                <XAxis type="number" stroke="#64748b" hide />
                <YAxis dataKey="range" type="category" stroke="#94a3b8" tick={{ fontSize: 12 }} width={60} tickLine={false} axisLine={false} />
                <Tooltip cursor={{ fill: 'rgba(255,255,255,0.05)' }} content={<CustomTooltip />} />
                <Bar dataKey="approved" name="Approved" stackId="a" fill="#3b82f6" radius={[0, 4, 4, 0]} barSize={20} />
                <Bar dataKey="rejected" name="Rejected" stackId="a" fill="#1e293b" radius={[0, 4, 4, 0]} barSize={20} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* AI Insights Summary */}
        <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl p-6 relative overflow-hidden">
          {/* Decorative Background */}
          <div className="absolute -right-10 -top-10 w-40 h-40 bg-white/10 rounded-full blur-3xl"></div>
          <div className="absolute -left-10 -bottom-10 w-40 h-40 bg-black/20 rounded-full blur-3xl"></div>

          <div className="relative z-10 h-full flex flex-col justify-between">
            <div>
              <h3 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
                <svg className="w-5 h-5 text-blue-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                AI Executive Summary
              </h3>
              <p className="text-blue-100 text-sm leading-relaxed opacity-90">
                Based on recent patterns, <strong>Home Loans</strong> are performing exceptionally well with a <strong>5.2% increase</strong> in approval rates. However, rejection rates for <span className="underline decoration-blue-300/50">low-income brackets</span> (&lt;30k) remain high due to DTI constraints.
              </p>
            </div>

            <div className="mt-6 pt-6 border-t border-white/10 grid grid-cols-2 gap-4">
              <div>
                <span className="block text-xs text-blue-200 uppercase tracking-wider mb-1">Top Opportunity</span>
                <span className="text-lg font-bold text-white">Mid-Market Auto</span>
              </div>
              <div>
                <span className="block text-xs text-blue-200 uppercase tracking-wider mb-1">Key Risk</span>
                <span className="text-lg font-bold text-white">Unsecured Personal</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
