import { useState, useEffect } from 'react';

const LiveMetrics = () => {
  const [metrics, setMetrics] = useState({
    activeUsers: 342,
    queriesPerMinute: 12,
    avgResponseTime: 1.2,
    systemLoad: 45
  });

  const [isLive, setIsLive] = useState(true);

  // Simulate real-time updates
  useEffect(() => {
    if (!isLive) return;

    const interval = setInterval(() => {
      setMetrics(prev => ({
        activeUsers: prev.activeUsers + Math.floor(Math.random() * 10 - 5),
        queriesPerMinute: Math.max(5, prev.queriesPerMinute + Math.floor(Math.random() * 6 - 3)),
        avgResponseTime: Math.max(0.8, Math.min(2.5, prev.avgResponseTime + (Math.random() * 0.4 - 0.2))),
        systemLoad: Math.max(20, Math.min(80, prev.systemLoad + Math.floor(Math.random() * 10 - 5)))
      }));
    }, 2000); // Update every 2 seconds

    return () => clearInterval(interval);
  }, [isLive]);

  const getLoadColor = (load) => {
    if (load < 40) return 'text-green-600 bg-green-100';
    if (load < 70) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <h3 className="text-lg font-bold text-gray-900">Live System Metrics</h3>
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${isLive ? 'bg-green-500 animate-pulse' : 'bg-gray-400'}`}></div>
            <span className="text-xs font-medium text-gray-600">{isLive ? 'LIVE' : 'PAUSED'}</span>
          </div>
        </div>
        <button
          onClick={() => setIsLive(!isLive)}
          className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
            isLive 
              ? 'bg-red-100 text-red-600 hover:bg-red-200' 
              : 'bg-green-100 text-green-600 hover:bg-green-200'
          }`}
        >
          {isLive ? 'Pause' : 'Resume'}
        </button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Active Users */}
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4 border border-blue-200">
          <div className="flex items-center justify-between mb-2">
            <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <span className="text-xs font-semibold text-blue-600">LIVE</span>
          </div>
          <p className="text-2xl font-bold text-gray-900 mb-1">{metrics.activeUsers}</p>
          <p className="text-xs text-gray-600">Active Users</p>
        </div>

        {/* Queries Per Minute */}
        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-4 border border-green-200">
          <div className="flex items-center justify-between mb-2">
            <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <span className="text-xs font-semibold text-green-600">QPM</span>
          </div>
          <p className="text-2xl font-bold text-gray-900 mb-1">{metrics.queriesPerMinute}</p>
          <p className="text-xs text-gray-600">Queries/Min</p>
        </div>

        {/* Response Time */}
        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-4 border border-purple-200">
          <div className="flex items-center justify-between mb-2">
            <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-xs font-semibold text-purple-600">AVG</span>
          </div>
          <p className="text-2xl font-bold text-gray-900 mb-1">{metrics.avgResponseTime.toFixed(2)}s</p>
          <p className="text-xs text-gray-600">Response Time</p>
        </div>

        {/* System Load */}
        <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg p-4 border border-orange-200">
          <div className="flex items-center justify-between mb-2">
            <svg className="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
            </svg>
            <span className={`text-xs font-semibold px-2 py-0.5 rounded ${getLoadColor(metrics.systemLoad)}`}>
              {metrics.systemLoad}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
            <div
              className={`h-2 rounded-full transition-all duration-500 ${
                metrics.systemLoad < 40 ? 'bg-green-600' :
                metrics.systemLoad < 70 ? 'bg-yellow-600' : 'bg-red-600'
              }`}
              style={{ width: `${metrics.systemLoad}%` }}
            ></div>
          </div>
          <p className="text-xs text-gray-600">System Load</p>
        </div>
      </div>

      <div className="mt-4 text-xs text-gray-500 text-center">
        Updates every 2 seconds • Last updated: {new Date().toLocaleTimeString()}
      </div>
    </div>
  );
};

export default LiveMetrics;
