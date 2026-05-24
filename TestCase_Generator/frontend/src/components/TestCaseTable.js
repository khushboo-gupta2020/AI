import React, { useState } from 'react';

const TestCaseTable = ({ testCases, storyData, onNotify }) => {
  const [expandedId, setExpandedId] = useState(null);

  const copyToClipboard = () => {
    const text = testCases
      .map(
        (tc) =>
          `**${tc.test_case_id}**: ${tc.test_scenario}\n\n` +
          `**Priority:** ${tc.priority}\n` +
          `**Preconditions:** ${tc.preconditions}\n` +
          `**Test Steps:**\n${tc.test_steps}\n` +
          `**Expected Result:** ${tc.expected_result}`
      )
      .join('\n\n---\n\n');

    navigator.clipboard.writeText(text);
    onNotify({ type: 'success', message: 'Copied to clipboard!' });
  };

  const exportToMarkdown = () => {
    let md = `# Test Cases for ${storyData?.key || 'Jira Story'}\n\n`;
    md += `**Summary:** ${storyData?.summary || ''}\n`;
    md += `**Priority:** ${storyData?.priority || ''}\n`;
    md += `**Status:** ${storyData?.status || ''}\n\n`;
    md += `---\n\n`;

    testCases.forEach((tc) => {
      md += `## ${tc.test_case_id}: ${tc.test_scenario}\n\n`;
      md += `| Field | Details |\n`;
      md += `|-------|--------|\n`;
      md += `| **Priority** | ${tc.priority} |\n`;
      md += `| **Preconditions** | ${tc.preconditions} |\n`;
      md += `| **Test Steps** | ${tc.test_steps.replace(/\n/g, '<br>')} |\n`;
      md += `| **Expected Result** | ${tc.expected_result} |\n\n`;
      md += `---\n\n`;
    });

    downloadFile(md, 'test-cases.md', 'text/markdown');
    onNotify({ type: 'success', message: 'Markdown file downloaded!' });
  };

  const exportToCSV = () => {
    const headers = ['Test Case ID', 'Test Scenario', 'Priority', 'Preconditions', 'Test Steps', 'Expected Result'];
    const rows = testCases.map((tc) => [
      tc.test_case_id,
      tc.test_scenario,
      tc.priority,
      tc.preconditions,
      tc.test_steps.replace(/\n/g, ' | '),
      tc.expected_result,
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map((row) => row.map((cell) => `"${cell.replace(/"/g, '""')}"`).join(',')),
    ].join('\n');

    downloadFile(csvContent, 'test-cases.csv', 'text/csv');
    onNotify({ type: 'success', message: 'CSV file downloaded!' });
  };

  const downloadFile = (content, filename, type) => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const getPriorityColor = (priority) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (!testCases || testCases.length === 0) {
    return null;
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-800">
          Generated Test Cases ({testCases.length})
        </h2>
        <div className="flex gap-2">
          <button
            onClick={copyToClipboard}
            className="bg-gray-100 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-200 transition text-sm font-medium flex items-center gap-1"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
            </svg>
            Copy
          </button>
          <button
            onClick={exportToMarkdown}
            className="bg-gray-100 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-200 transition text-sm font-medium flex items-center gap-1"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Markdown
          </button>
          <button
            onClick={exportToCSV}
            className="bg-gray-100 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-200 transition text-sm font-medium flex items-center gap-1"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            CSV
          </button>
        </div>
      </div>

      {storyData && (
        <div className="bg-blue-50 border border-blue-200 rounded-md p-4 mb-4">
          <h3 className="font-medium text-blue-900">{storyData.key}: {storyData.summary}</h3>
          <div className="flex gap-4 mt-2 text-sm text-blue-700">
            <span>Status: {storyData.status}</span>
            <span>Priority: {storyData.priority}</span>
            <span>Type: {storyData.issuetype}</span>
          </div>
        </div>
      )}

      <div className="space-y-3">
        {testCases.map((tc) => (
          <div
            key={tc.test_case_id}
            className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition"
          >
            <div
              className="flex items-center justify-between p-4 bg-white cursor-pointer"
              onClick={() => setExpandedId(expandedId === tc.test_case_id ? null : tc.test_case_id)}
            >
              <div className="flex items-center gap-3">
                <span className="font-mono text-sm font-semibold text-blue-600 bg-blue-50 px-2 py-1 rounded">
                  {tc.test_case_id}
                </span>
                <span className="font-medium text-gray-800">{tc.test_scenario}</span>
              </div>
              <div className="flex items-center gap-3">
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(tc.priority)}`}>
                  {tc.priority}
                </span>
                <svg
                  className={`w-5 h-5 text-gray-400 transform transition-transform ${expandedId === tc.test_case_id ? 'rotate-180' : ''}`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>

            {expandedId === tc.test_case_id && (
              <div className="bg-gray-50 px-4 py-3 border-t border-gray-200">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="font-medium text-gray-700 mb-1">Preconditions:</p>
                    <p className="text-gray-600">{tc.preconditions}</p>
                  </div>
                  <div>
                    <p className="font-medium text-gray-700 mb-1">Expected Result:</p>
                    <p className="text-gray-600">{tc.expected_result}</p>
                  </div>
                  <div className="md:col-span-2">
                    <p className="font-medium text-gray-700 mb-1">Test Steps:</p>
                    <pre className="text-gray-600 whitespace-pre-wrap font-sans">{tc.test_steps}</pre>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default TestCaseTable;
