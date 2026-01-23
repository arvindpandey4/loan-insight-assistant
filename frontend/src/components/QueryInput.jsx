const QueryInput = ({ question, setQuestion, onSubmit, loading }) => {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey) && !loading && question.trim()) {
      onSubmit();
    }
  };

  return (
    <div>
      <label htmlFor="question-input" className="block text-sm font-medium text-gray-700 mb-2">
        Your Question
      </label>
      
      <textarea
        id="question-input"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="e.g., Why are home loans rejected for applicants with income between $50k-$70k?"
        rows={5}
        disabled={loading}
        className="w-full border-2 border-gray-300 rounded-lg p-4 text-base
                   focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                   disabled:bg-gray-100 disabled:cursor-not-allowed
                   transition-all duration-200 resize-y"
        style={{ minHeight: '120px', maxHeight: '400px' }}
      />

      <div className="flex items-center justify-between mt-2">
        <span className="text-xs text-gray-500">
          {question.length} characters
          {question.trim() && ' • Press Ctrl+Enter to submit'}
        </span>
        {question.length > 500 && (
          <span className="text-xs text-amber-600">
            Consider keeping your question concise
          </span>
        )}
      </div>

      <button
        onClick={onSubmit}
        disabled={loading || !question.trim()}
        className="mt-4 w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold text-base
                   hover:bg-blue-700 active:bg-blue-800
                   focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
                   disabled:bg-gray-300 disabled:cursor-not-allowed
                   transition-all duration-200
                   shadow-md hover:shadow-lg"
      >
        {loading ? (
          <span className="flex items-center justify-center">
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Analyzing...
          </span>
        ) : (
          'Get Insights'
        )}
      </button>
    </div>
  );
};

export default QueryInput;
