import StatsCard from './StatsCard';
import LiveMetrics from './LiveMetrics';
import InteractiveFilters from './InteractiveFilters';
import LiveSearchTable from './LiveSearchTable';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const Dashboard = () => {
  const stats = [
    {
      title: 'Total Queries',
      value: '1,247',
      change: '+12.5%',
      icon: 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z',
      color: 'blue'
    },
    {
      title: 'Cases Analyzed',
      value: '8,432',
      change: '+8.2%',
      icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
      color: 'green'
    },
    {
      title: 'Avg Confidence',
      value: '87.3%',
      change: '+3.1%',
      icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
      color: 'purple'
    },
    {
      title: 'Active Users',
      value: '342',
      change: '+18.7%',
      icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z',
      color: 'orange'
    }
  ];

  const recentQueries = [
    { query: 'Why are home loans rejected for income $50k-$70k?', time: '5 min ago', confidence: 89, user: 'John D.' },
    { query: 'Common risk factors for auto loan rejections', time: '12 min ago', confidence: 92, user: 'Sarah M.' },
    { query: 'Historical trend for business loans in Q4', time: '28 min ago', confidence: 85, user: 'Mike R.' },
    { query: 'Credit score impact on personal loan approval', time: '1 hour ago', confidence: 91, user: 'Emily K.' },
  ];

  const riskFactors = [
    { factor: 'Low Credit Score', count: 342, percentage: 28, trend: 'up' },
    { factor: 'High Debt-to-Income', count: 289, percentage: 24, trend: 'down' },
    { factor: 'Insufficient Income', count: 256, percentage: 21, trend: 'up' },
    { factor: 'Employment History', count: 198, percentage: 16, trend: 'stable' },
    { factor: 'Other Factors', count: 132, percentage: 11, trend: 'down' },
  ];

  // Weekly trend data
  const weeklyTrendData = [
    { day: 'Mon', queries: 187 },
    { day: 'Tue', queries: 203 },
    { day: 'Wed', queries: 195 },
    { day: 'Thu', queries: 221 },
    { day: 'Fri', queries: 234 },
    { day: 'Sat', queries: 98 },
    { day: 'Sun', queries: 109 },
  ];

  // Loan status distribution
  const loanStatusData = [
    { name: 'Approved', value: 5800, color: '#10b981' },
    { name: 'Rejected', value: 1950, color: '#ef4444' },
    { name: 'Pending', value: 280, color: '#f59e0b' },
  ];

  return (
    <div className="space-y-6">
      {/* Live Metrics - Real-time updates */}
      <LiveMetrics />

      {/* Interactive Filters */}
      <InteractiveFilters onFilterChange={(filters) => console.log('Filters changed:', filters)} />

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <StatsCard key={index} {...stat} />
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Weekly Query Trend */}
        <div className="lg:col-span-2 bg-white rounded-xl border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-900">Weekly Query Trend</h2>
            <span className="text-sm text-gray-500">Last 7 days</span>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={weeklyTrendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="day" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
              />
              <Bar dataKey="queries" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Loan Status Distribution */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Loan Status</h2>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={loanStatusData}
                cx="50%"
                cy="50%"
                innerRadius={50}
                outerRadius={80}
                fill="#8884d8"
                paddingAngle={5}
                dataKey="value"
              >
                {loanStatusData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-4 space-y-2">
            {loanStatusData.map((item, index) => (
              <div key={index} className="flex items-center justify-between text-sm">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></div>
                  <span className="text-gray-700">{item.name}</span>
                </div>
                <span className="font-semibold text-gray-900">{item.value.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Queries */}
        <div className="lg:col-span-2 bg-white rounded-xl border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900">Recent Queries</h2>
            <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
              View All →
            </button>
          </div>
          <div className="space-y-4">
            {recentQueries.map((item, index) => (
              <div key={index} className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer">
                <div className="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                  </svg>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 mb-1">{item.query}</p>
                  <div className="flex items-center space-x-4">
                    <span className="text-xs text-gray-500">{item.time}</span>
                    <span className="text-xs text-gray-500">by {item.user}</span>
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                      {item.confidence}% confidence
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Risk Factors */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Top Risk Factors</h2>
          <div className="space-y-4">
            {riskFactors.map((item, index) => (
              <div key={index}>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-gray-700">{item.factor}</span>
                    {item.trend === 'up' && (
                      <svg className="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
                      </svg>
                    )}
                    {item.trend === 'down' && (
                      <svg className="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 012 0v11.586l2.293-2.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    )}
                  </div>
                  <span className="text-sm font-semibold text-gray-900">{item.count}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all"
                    style={{ width: `${item.percentage}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* System Health & Alerts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* System Health */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">System Health</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-gray-700">API Response Time</span>
              </div>
              <span className="text-sm font-semibold text-green-600">1.2s</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-gray-700">Database Connection</span>
              </div>
              <span className="text-sm font-semibold text-green-600">Healthy</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-gray-700">FAISS Index</span>
              </div>
              <span className="text-sm font-semibold text-green-600">Optimized</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-gray-700">Cache Hit Rate</span>
              </div>
              <span className="text-sm font-semibold text-yellow-600">78%</span>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-6 text-white">
          <h2 className="text-xl font-bold mb-2">Ready to analyze?</h2>
          <p className="text-blue-100 mb-6">Ask questions and get AI-powered insights from historical loan data</p>
          <div className="flex space-x-3">
            <button className="flex-1 bg-white text-blue-600 px-4 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors">
              Start Query
            </button>
            <button className="flex-1 bg-blue-700 text-white px-4 py-3 rounded-lg font-semibold hover:bg-blue-800 transition-colors">
              View Analytics
            </button>
          </div>
        </div>
      </div>

      {/* Live Search Table */}
      <LiveSearchTable />
    </div>
  );
};

export default Dashboard;
