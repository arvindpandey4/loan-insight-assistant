import { useState } from 'react';

const InteractiveFilters = ({ onFilterChange }) => {
  const [filters, setFilters] = useState({
    dateRange: 'last7days',
    loanType: 'all',
    status: 'all',
    confidenceMin: 0,
    department: 'all'
  });

  const [isExpanded, setIsExpanded] = useState(false);

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilterChange?.(newFilters);
  };

  const resetFilters = () => {
    const defaultFilters = {
      dateRange: 'last7days',
      loanType: 'all',
      status: 'all',
      confidenceMin: 0,
      department: 'all'
    };
    setFilters(defaultFilters);
    onFilterChange?.(defaultFilters);
  };

  const activeFilterCount = Object.values(filters).filter(
    (value, index) => {
      const defaults = ['last7days', 'all', 'all', 0, 'all'];
      return value !== defaults[index];
    }
  ).length;

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <h3 className="text-lg font-bold text-gray-900">Filters</h3>
          {activeFilterCount > 0 && (
            <span className="px-2 py-1 bg-blue-100 text-blue-600 text-xs font-semibold rounded-full">
              {activeFilterCount} active
            </span>
          )}
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={resetFilters}
            className="text-sm text-gray-600 hover:text-gray-900 font-medium"
          >
            Reset All
          </button>
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg
              className={`w-5 h-5 text-gray-600 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
        </div>
      </div>

      {/* Quick Filters - Always Visible */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
        {/* Date Range */}
        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">Date Range</label>
          <select
            value={filters.dateRange}
            onChange={(e) => handleFilterChange('dateRange', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="today">Today</option>
            <option value="last7days">Last 7 Days</option>
            <option value="last30days">Last 30 Days</option>
            <option value="last3months">Last 3 Months</option>
            <option value="last6months">Last 6 Months</option>
            <option value="lastyear">Last Year</option>
          </select>
        </div>

        {/* Loan Type */}
        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">Loan Type</label>
          <select
            value={filters.loanType}
            onChange={(e) => handleFilterChange('loanType', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Types</option>
            <option value="home">Home Loans</option>
            <option value="auto">Auto Loans</option>
            <option value="personal">Personal Loans</option>
            <option value="business">Business Loans</option>
            <option value="education">Education Loans</option>
          </select>
        </div>

        {/* Status */}
        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">Status</label>
          <select
            value={filters.status}
            onChange={(e) => handleFilterChange('status', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Status</option>
            <option value="approved">Approved</option>
            <option value="rejected">Rejected</option>
            <option value="pending">Pending</option>
          </select>
        </div>

        {/* Department */}
        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">Department</label>
          <select
            value={filters.department}
            onChange={(e) => handleFilterChange('department', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Departments</option>
            <option value="retail">Retail Banking</option>
            <option value="corporate">Corporate Loans</option>
            <option value="risk">Risk Analysis</option>
            <option value="compliance">Compliance</option>
          </select>
        </div>
      </div>

      {/* Advanced Filters - Expandable */}
      {isExpanded && (
        <div className="border-t border-gray-200 pt-4 animate-fadeIn">
          <h4 className="text-sm font-semibold text-gray-900 mb-3">Advanced Filters</h4>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Confidence Score Range */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-2">
                Minimum Confidence Score: {filters.confidenceMin}%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                step="5"
                value={filters.confidenceMin}
                onChange={(e) => handleFilterChange('confidenceMin', parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>0%</span>
                <span>50%</span>
                <span>100%</span>
              </div>
            </div>

            {/* Quick Date Presets */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-2">Quick Presets</label>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => handleFilterChange('dateRange', 'today')}
                  className="px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs font-medium rounded-lg transition-colors"
                >
                  Today
                </button>
                <button
                  onClick={() => handleFilterChange('dateRange', 'last7days')}
                  className="px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs font-medium rounded-lg transition-colors"
                >
                  This Week
                </button>
                <button
                  onClick={() => handleFilterChange('dateRange', 'last30days')}
                  className="px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs font-medium rounded-lg transition-colors"
                >
                  This Month
                </button>
                <button
                  onClick={() => handleFilterChange('dateRange', 'last3months')}
                  className="px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs font-medium rounded-lg transition-colors"
                >
                  This Quarter
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Active Filters Display */}
      {activeFilterCount > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="flex items-center flex-wrap gap-2">
            <span className="text-xs font-medium text-gray-600">Active:</span>
            {filters.dateRange !== 'last7days' && (
              <span className="inline-flex items-center px-2 py-1 bg-blue-100 text-blue-700 text-xs font-medium rounded">
                {filters.dateRange.replace(/([A-Z])/g, ' $1').trim()}
                <button
                  onClick={() => handleFilterChange('dateRange', 'last7days')}
                  className="ml-1 hover:text-blue-900"
                >
                  ×
                </button>
              </span>
            )}
            {filters.loanType !== 'all' && (
              <span className="inline-flex items-center px-2 py-1 bg-green-100 text-green-700 text-xs font-medium rounded">
                {filters.loanType} loans
                <button
                  onClick={() => handleFilterChange('loanType', 'all')}
                  className="ml-1 hover:text-green-900"
                >
                  ×
                </button>
              </span>
            )}
            {filters.status !== 'all' && (
              <span className="inline-flex items-center px-2 py-1 bg-purple-100 text-purple-700 text-xs font-medium rounded">
                {filters.status}
                <button
                  onClick={() => handleFilterChange('status', 'all')}
                  className="ml-1 hover:text-purple-900"
                >
                  ×
                </button>
              </span>
            )}
            {filters.confidenceMin > 0 && (
              <span className="inline-flex items-center px-2 py-1 bg-orange-100 text-orange-700 text-xs font-medium rounded">
                Confidence ≥ {filters.confidenceMin}%
                <button
                  onClick={() => handleFilterChange('confidenceMin', 0)}
                  className="ml-1 hover:text-orange-900"
                >
                  ×
                </button>
              </span>
            )}
            {filters.department !== 'all' && (
              <span className="inline-flex items-center px-2 py-1 bg-pink-100 text-pink-700 text-xs font-medium rounded">
                {filters.department}
                <button
                  onClick={() => handleFilterChange('department', 'all')}
                  className="ml-1 hover:text-pink-900"
                >
                  ×
                </button>
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default InteractiveFilters;
