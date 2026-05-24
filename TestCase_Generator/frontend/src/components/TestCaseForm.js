import React, { useState } from 'react';
import { generateTestCases } from '../services/api';

const TestCaseForm = ({ config, onNotify, onTestCasesGenerated }) => {
  const [issueId, setIssueId] = useState('');
  const [generating, setGenerating] = useState(false);

  const handleGenerate = async () => {
    if (!issueId.trim()) {
      onNotify({ type: 'error', message: 'Please enter a Jira Story ID' });
      return;
    }

    if (!config.base_url || !config.email || !config.api_token) {
      onNotify({ type: 'error', message: 'Please configure Jira connection first' });
      return;
    }

    setGenerating(true);
    try {
      const result = await generateTestCases(config, issueId.trim());
      onNotify({ type: 'success', message: result.message });
      onTestCasesGenerated(result);
    } catch (error) {
      onNotify({
        type: 'error',
        message: error.response?.data?.detail || 'Failed to generate test cases',
      });
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Generate Test Cases</h2>

      <div className="flex gap-3">
        <input
          type="text"
          value={issueId}
          onChange={(e) => setIssueId(e.target.value)}
          placeholder="Enter Jira Story ID (e.g., PROJ-123)"
          className="flex-1 px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-base"
          onKeyPress={(e) => e.key === 'Enter' && handleGenerate()}
        />
        <button
          onClick={handleGenerate}
          disabled={generating}
          className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 disabled:bg-blue-300 transition font-medium flex items-center gap-2"
        >
          {generating ? (
            <>
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Generating...
            </>
          ) : (
            'Generate Test Cases'
          )}
        </button>
      </div>
    </div>
  );
};

export default TestCaseForm;
