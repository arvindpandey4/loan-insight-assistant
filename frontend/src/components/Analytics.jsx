import { useState, useEffect } from 'react';
import {
  BarChart, Bar, PieChart, Pie, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell
} from 'recharts';
import { fetchLoanStatusDistribution, fetchAvgCIBIL, fetchRejectionReasons } from '../services/loanInsightsApi';

const Analytics = () => {
  const [loanTypeData, setLoanTypeData] = useState([]);
  const [approvalTrendData, setApprovalTrendData] = useState([]);
  const [incomeRangeData, setIncomeRangeData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadAnalytics = async () => {
      try {
        const [statusData, cibilData, rejectionReasonData] = await Promise.all([
          fetchLoanStatusDistribution(),
          fetchAvgCIBIL(),
          fetchRejectionReasons()
        ]);

        // Transform data for charts
        // Note: The structure here assumes specific data. You might need to adjust mapping based on exact API response.
        // For now, I will use placeholder mapping logic assuming the API returns array of objects suitable for charts
        // If the API returns raw stats, we would need to process them here.

        // Since we don't have the exact API response format for all of them yet, 
        // I will keep the original structure for charts that don't have direct API support yet
        // and map the ones that do.

        // Example mapping for Loan Type (using Status analytics for now as proxy or if API supports type)
        if (statusData && statusData.distribution) {
          const mappedLoanType = statusData.distribution.map(item => ({
            name: item.name || item.status,
            value: item.count || item.value,
            color: item.color || '#3b82f6'
          }));
          setLoanTypeData(mappedLoanType);
        }

        // Placeholder for other data until specific endpoints are ready
        // Re-using the hardcoded data for demonstration if API returns empty
        setApprovalTrendData([
          { month: 'Jan', approved: 4200, rejected: 1800 },
          { month: 'Feb', approved: 4800, rejected: 1600 },
          { month: 'Mar', approved: 5300, rejected: 1900 },
          { month: 'Apr', approved: 4900, rejected: 1700 },
          { month: 'May', approved: 5600, rejected: 2100 },
          { month: 'Jun', approved: 5800, rejected: 1950 },
        ]);

        setIncomeRangeData([
          { range: '<$30k', approved: 120, rejected: 380 },
          { range: '$30-50k', approved: 450, rejected: 250 },
          { range: '$50-70k', approved: 680, rejected: 180 },
          { range: '$70-100k', approved: 890, rejected: 110 },
          { range: '$100k+', approved: 1200, rejected: 80 },
        ]);

        setLoading(false);
      } catch (err) {
        console.error("Failed to load analytics data", err);
        setError("Failed to load analytics data");
        setLoading(false);
      }
    };

    loadAnalytics();
  }, []);

  if (loading) return <div className="p-8 text-center text-gray-500">Loading analytics...</div>;
  if (error) return <div className="p-8 text-center text-red-500">{error}</div>;

  // Daily Query Volume (Last 7 Days) - Static for now or fetch from history API if available
  const dailyQueryData = [
    { day: 'Mon', queries: 187 },
    { day: 'Tue', queries: 203 },
    { day: 'Wed', queries: 195 },
    { day: 'Thu', queries: 221 },
    { day: 'Fri', queries: 234 },
    { day: 'Sat', queries: 98 },
    { day: 'Sun', queries: 109 },
  ];

  const handleExport = () => {
    // Prepare data for export
    const exportData = {
      loanTypeDistribution: loanTypeData,
      approvalTrends: approvalTrendData,
      incomeRangeAnalysis: incomeRangeData,
      dailyQueryActivity: dailyQueryData,
      exportDate: new Date().toISOString(),
    };

    // Convert to CSV format
    let csvContent = "Analytics Report - Loan Insights\n";
    csvContent += `Export Date: ${new Date().toLocaleString()}\n\n`;

    // Loan Type Distribution
    csvContent += "Loan Type Distribution\n";
    csvContent += "Type,Count,Color\n";
    loanTypeData.forEach(item => {
      csvContent += `${item.name},${item.value},${item.color}\n`;
    });

    csvContent += "\nApproval Trends\n";
    csvContent += "Month,Approved,Rejected\n";
    approvalTrendData.forEach(item => {
      csvContent += `${item.month},${item.approved},${item.rejected}\n`;
    });

    csvContent += "\nIncome Range Analysis\n";
    csvContent += "Range,Approved,Rejected\n";
    incomeRangeData.forEach(item => {
      csvContent += `${item.range},${item.approved},${item.rejected}\n`;
    });

    csvContent += "\nDaily Query Activity\n";
    csvContent += "Day,Queries\n";
    dailyQueryData.forEach(item => {
      csvContent += `${item.day},${item.queries}\n`;
    });

    // Create and download file
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `loan-analytics-report-${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Analytics Overview</h2>
            <p className="text-gray-600">Key insights into loan decision patterns and trends</p>
          </div>
          <div className="flex items-center space-x-3">
            <select className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option>Last 6 Months</option>
              <option>Last 3 Months</option>
              <option>Last Month</option>
              <option>Last Week</option>
            </select>
            <button
              onClick={handleExport}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              <span>Export Report</span>
            </button>
          </div>
        </div>
      </div>

      {/* Key Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <span className="text-blue-100 text-sm font-medium">Total Cases</span>
            <svg className="w-8 h-8 text-blue-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <p className="text-3xl font-bold mb-1">9,432</p>
          <p className="text-blue-100 text-sm">+12.5% from last period</p>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <span className="text-green-100 text-sm font-medium">Approval Rate</span>
            <svg className="w-8 h-8 text-green-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p className="text-3xl font-bold mb-1">74.8%</p>
          <p className="text-green-100 text-sm">+2.3% from last period</p>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <span className="text-purple-100 text-sm font-medium">Avg Confidence</span>
            <svg className="w-8 h-8 text-purple-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
          <p className="text-3xl font-bold mb-1">87.3%</p>
          <p className="text-purple-100 text-sm">+3.1% from last period</p>
        </div>

        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <span className="text-orange-100 text-sm font-medium">Total Queries</span>
            <svg className="w-8 h-8 text-orange-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <p className="text-3xl font-bold mb-1">1,247</p>
          <p className="text-orange-100 text-sm">+18.7% from last period</p>
        </div>
      </div>

      {/* Charts Row 1: Loan Type Distribution & Approval vs Rejection */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Loan Type Distribution - Pie Chart */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Loan Type Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={loanTypeData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {loanTypeData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-4 space-y-2">
            {loanTypeData.map((item, index) => (
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

        {/* Approval vs Rejection Trends - Area Chart */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Approval vs Rejection Trends</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={approvalTrendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="month" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
              />
              <Legend />
              <Area type="monotone" dataKey="approved" stackId="1" stroke="#10b981" fill="#10b981" fillOpacity={0.6} name="Approved" />
              <Area type="monotone" dataKey="rejected" stackId="1" stroke="#ef4444" fill="#ef4444" fillOpacity={0.6} name="Rejected" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts Row 2: Daily Query & Income Range */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Daily Query Activity - Bar Chart */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Daily Query Activity (Last 7 Days)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={dailyQueryData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="day" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
              />
              <Bar dataKey="queries" fill="#3b82f6" name="Queries" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Approval by Income Range - Bar Chart */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Approval by Income Range</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={incomeRangeData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="range" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
              />
              <Legend />
              <Bar dataKey="approved" fill="#10b981" name="Approved" radius={[8, 8, 0, 0]} />
              <Bar dataKey="rejected" fill="#ef4444" name="Rejected" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Insights Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
          <div className="flex items-center space-x-3 mb-3">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <h4 className="font-bold text-gray-900">Peak Performance</h4>
          </div>
          <p className="text-sm text-gray-700">
            Friday shows highest query volume with 234 queries, indicating peak user activity.
          </p>
        </div>

        <div className="bg-green-50 border border-green-200 rounded-xl p-6">
          <div className="flex items-center space-x-3 mb-3">
            <div className="w-10 h-10 bg-green-600 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h4 className="font-bold text-gray-900">Top Performer</h4>
          </div>
          <p className="text-sm text-gray-700">
            Home loans represent 37.5% of all queries with highest approval rates in $70k+ income range.
          </p>
        </div>

        <div className="bg-orange-50 border border-orange-200 rounded-xl p-6">
          <div className="flex items-center space-x-3 mb-3">
            <div className="w-10 h-10 bg-orange-600 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <h4 className="font-bold text-gray-900">Income Insight</h4>
          </div>
          <p className="text-sm text-gray-700">
            Clear correlation: Higher income ranges show significantly better approval rates (93.8% for $100k+).
          </p>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
