import { useState, useEffect } from 'react';
import { Settings, FileText, Loader2, CheckCircle, AlertCircle, Copy, Download, ChevronDown, ChevronUp, TestTube } from 'lucide-react';
import { testConnection, generateTestCases } from './services/api';

function App() {
  const [jiraConfig, setJiraConfig] = useState({
    jira_base_url: '',
    jira_email: '',
    jira_api_token: '',
    jira_project_key: '',
  });
  const [storyId, setStoryId] = useState('');
  const [connectionStatus, setConnectionStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [testCases, setTestCases] = useState([]);
  const [story, setStory] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [expandedCases, setExpandedCases] = useState({});

  useEffect(() => {
    const saved = localStorage.getItem('jiraConfig');
    if (saved) {
      try {
        setJiraConfig(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to parse saved config');
      }
    }
  }, []);

  const handleConfigChange = (e) => {
    setJiraConfig({ ...jiraConfig, [e.target.name]: e.target.value });
  };

  const handleTestConnection = async () => {
    setLoading(true);
    setError('');
    setSuccess('');
    setConnectionStatus(null);
    try {
      const result = await testConnection(jiraConfig);
      setConnectionStatus(result);
      setSuccess(`Connected as ${result.user}`);
      localStorage.setItem('jiraConfig', JSON.stringify(jiraConfig));
    } catch (err) {
      setError(err.response?.data?.detail || 'Connection failed');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    if (!storyId.trim()) {
      setError('Please enter a Jira Story ID');
      return;
    }
    setGenerating(true);
    setError('');
    setSuccess('');
    setTestCases([]);
    setStory(null);
    try {
      const result = await generateTestCases({
        story_id: storyId.trim(),
        jira_base_url: jiraConfig.jira_base_url,
        jira_email: jiraConfig.jira_email,
        jira_api_token: jiraConfig.jira_api_token,
      });
      setStory(result.story);
      setTestCases(result.test_cases);
      setSuccess(`Generated ${result.test_cases.length} test cases`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate test cases');
    } finally {
      setGenerating(false);
    }
  };

  const toggleExpand = (id) => {
    setExpandedCases({ ...expandedCases, [id]: !expandedCases[id] });
  };

  const copyToClipboard = () => {
    const text = testCases.map((tc) => {
      return `**${tc.test_case_id}: ${tc.test_scenario}**\n\n- **Preconditions:** ${tc.preconditions}\n- **Test Steps:** ${tc.test_steps}\n- **Expected Result:** ${tc.expected_result}\n- **Priority:** ${tc.priority}\n`;
    }).join('\n---\n\n');
    navigator.clipboard.writeText(text);
    setSuccess('Copied to clipboard!');
    setTimeout(() => setSuccess(''), 3000);
  };

  const exportToMarkdown = () => {
    if (!story || testCases.length === 0) return;

    let md = `# Test Cases for ${story.key}: ${story.summary}\n\n`;
    md += `## Story Details\n\n`;
    md += `- **Key:** ${story.key}\n`;
    md += `- **Type:** ${story.issue_type}\n`;
    md += `- **Priority:** ${story.priority || 'N/A'}\n`;
    md += `- **Status:** ${story.status}\n`;
    md += `- **Labels:** ${story.labels.join(', ') || 'None'}\n\n`;

    if (story.description) {
      md += `## Description\n\n${story.description}\n\n`;
    }
    if (story.acceptance_criteria) {
      md += `## Acceptance Criteria\n\n${story.acceptance_criteria}\n\n`;
    }

    md += `---\n\n`;
    md += `## Generated Test Cases\n\n`;

    testCases.forEach((tc) => {
      md += `### ${tc.test_case_id}: ${tc.test_scenario}\n\n`;
      md += `| Field | Details |\n`;
      md += `|-------|---------|\n`;
      md += `| **Preconditions** | ${tc.preconditions} |\n`;
      md += `| **Test Steps** | ${tc.test_steps.replace(/\n/g, '<br>')} |\n`;
      md += `| **Expected Result** | ${tc.expected_result} |\n`;
      md += `| **Priority** | ${tc.priority} |\n\n`;
      md += `---\n\n`;
    });

    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `test-cases-${story.key}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const exportToCSV = () => {
    if (!story || testCases.length === 0) return;

    const headers = ['Test Case ID', 'Test Scenario', 'Preconditions', 'Test Steps', 'Expected Result', 'Priority'];
    const rows = testCases.map((tc) => [
      tc.test_case_id,
      tc.test_scenario,
      tc.preconditions,
      tc.test_steps.replace(/\n/g, ' | '),
      tc.expected_result,
      tc.priority,
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map((row) => row.map((cell) => `"${String(cell).replace(/"/g, '""')}"`).join(',')),
    ].join('\n');

    const BOM = '\uFEFF';
    const blob = new Blob([BOM + csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `test-cases-${story.key}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const getPriorityColor = (priority) => {
    switch (priority.toLowerCase()) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="min-h-screen flex bg-slate-50">
      {/* Sidebar */}
      <aside className={`${sidebarOpen ? 'w-80' : 'w-0'} bg-white border-r border-slate-200 transition-all duration-300 overflow-hidden flex-shrink-0`}>
        <div className="p-6 w-80">
          <div className="flex items-center gap-2 mb-6">
            <Settings className="w-5 h-5 text-slate-600" />
            <h2 className="text-lg font-semibold text-slate-800">Jira Connection</h2>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Jira Base URL</label>
              <input
                type="url"
                name="jira_base_url"
                value={jiraConfig.jira_base_url}
                onChange={handleConfigChange}
                placeholder="https://your-domain.atlassian.net"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
              <input
                type="email"
                name="jira_email"
                value={jiraConfig.jira_email}
                onChange={handleConfigChange}
                placeholder="your-email@example.com"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">API Token</label>
              <input
                type="password"
                name="jira_api_token"
                value={jiraConfig.jira_api_token}
                onChange={handleConfigChange}
                placeholder="Your API token"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Project Key (Optional)</label>
              <input
                type="text"
                name="jira_project_key"
                value={jiraConfig.jira_project_key}
                onChange={handleConfigChange}
                placeholder="PROJ"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
              />
            </div>

            <button
              onClick={handleTestConnection}
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition font-medium text-sm"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle className="w-4 h-4" />}
              {loading ? 'Testing...' : 'Test Connection'}
            </button>

            {connectionStatus && (
              <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-sm text-green-800">Connected as: <strong>{connectionStatus.user}</strong></p>
                <p className="text-xs text-green-600 mt-1">{connectionStatus.email}</p>
              </div>
            )}
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover:bg-slate-100 rounded-lg transition"
            >
              <Settings className="w-5 h-5 text-slate-600" />
            </button>
            <div className="flex items-center gap-2">
              <TestTube className="w-6 h-6 text-blue-600" />
              <h1 className="text-xl font-bold text-slate-800">Jira Test Case Generator</h1>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <div className="flex-1 p-6 overflow-auto">
          {/* Input Section */}
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mb-6">
            <div className="flex items-center gap-2 mb-4">
              <FileText className="w-5 h-5 text-slate-600" />
              <h2 className="text-lg font-semibold text-slate-800">Generate Test Cases</h2>
            </div>

            <div className="flex gap-3">
              <input
                type="text"
                value={storyId}
                onChange={(e) => setStoryId(e.target.value)}
                placeholder="Enter Jira Story ID (e.g., PROJ-123)"
                className="flex-1 px-4 py-3 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
                onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
              />
              <button
                onClick={handleGenerate}
                disabled={generating}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition font-medium text-sm flex items-center gap-2"
              >
                {generating ? <Loader2 className="w-4 h-4 animate-spin" /> : <TestTube className="w-4 h-4" />}
                {generating ? 'Generating...' : 'Generate Test Cases'}
              </button>
            </div>
          </div>

          {/* Notifications */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-3">
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          {success && (
            <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center gap-3">
              <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
              <p className="text-sm text-green-800">{success}</p>
            </div>
          )}

          {/* Story Details */}
          {story && (
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mb-6">
              <h3 className="text-lg font-semibold text-slate-800 mb-3">{story.key}: {story.summary}</h3>
              <div className="flex flex-wrap gap-2 mb-4">
                {story.issue_type && (
                  <span className="px-2.5 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">{story.issue_type}</span>
                )}
                {story.priority && (
                  <span className={`px-2.5 py-1 text-xs font-medium rounded-full border ${getPriorityColor(story.priority)}`}>{story.priority}</span>
                )}
                {story.status && (
                  <span className="px-2.5 py-1 bg-slate-100 text-slate-700 text-xs font-medium rounded-full">{story.status}</span>
                )}
                {story.labels.map((label, i) => (
                  <span key={i} className="px-2.5 py-1 bg-purple-100 text-purple-700 text-xs font-medium rounded-full">{label}</span>
                ))}
              </div>
              {story.description && (
                <div className="mb-3">
                  <h4 className="text-sm font-medium text-slate-700 mb-1">Description</h4>
                  <p className="text-sm text-slate-600 whitespace-pre-wrap">{story.description}</p>
                </div>
              )}
              {story.acceptance_criteria && (
                <div>
                  <h4 className="text-sm font-medium text-slate-700 mb-1">Acceptance Criteria</h4>
                  <p className="text-sm text-slate-600 whitespace-pre-wrap">{story.acceptance_criteria}</p>
                </div>
              )}
            </div>
          )}

          {/* Test Cases */}
          {testCases.length > 0 && (
            <div className="bg-white rounded-xl shadow-sm border border-slate-200">
              <div className="p-6 border-b border-slate-200 flex items-center justify-between">
                <h3 className="text-lg font-semibold text-slate-800">Generated Test Cases ({testCases.length})</h3>
                <div className="flex gap-2">
                  <button
                    onClick={copyToClipboard}
                    className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-700 bg-slate-100 rounded-lg hover:bg-slate-200 transition"
                  >
                    <Copy className="w-4 h-4" />
                    Copy
                  </button>
                  <button
                    onClick={exportToMarkdown}
                    className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-700 bg-slate-100 rounded-lg hover:bg-slate-200 transition"
                  >
                    <Download className="w-4 h-4" />
                    Markdown
                  </button>
                  <button
                    onClick={exportToCSV}
                    className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-700 bg-slate-100 rounded-lg hover:bg-slate-200 transition"
                  >
                    <Download className="w-4 h-4" />
                    CSV
                  </button>
                </div>
              </div>

              <div className="divide-y divide-slate-200">
                {testCases.map((tc) => (
                  <div key={tc.test_case_id} className="p-4 hover:bg-slate-50 transition">
                    <div
                      className="flex items-center justify-between cursor-pointer"
                      onClick={() => toggleExpand(tc.test_case_id)}
                    >
                      <div className="flex items-center gap-3 flex-1 min-w-0">
                        <span className="text-xs font-mono font-semibold text-blue-600 bg-blue-50 px-2 py-1 rounded">{tc.test_case_id}</span>
                        <span className="text-sm font-medium text-slate-800 truncate">{tc.test_scenario}</span>
                      </div>
                      <div className="flex items-center gap-3 flex-shrink-0">
                        <span className={`px-2.5 py-1 text-xs font-medium rounded-full border ${getPriorityColor(tc.priority)}`}>
                          {tc.priority}
                        </span>
                        {expandedCases[tc.test_case_id] ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
                      </div>
                    </div>

                    {expandedCases[tc.test_case_id] && (
                      <div className="mt-4 ml-2 pl-4 border-l-2 border-slate-200 space-y-3">
                        <div>
                          <h5 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1">Preconditions</h5>
                          <p className="text-sm text-slate-700">{tc.preconditions}</p>
                        </div>
                        <div>
                          <h5 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1">Test Steps</h5>
                          <p className="text-sm text-slate-700 whitespace-pre-wrap">{tc.test_steps}</p>
                        </div>
                        <div>
                          <h5 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1">Expected Result</h5>
                          <p className="text-sm text-slate-700">{tc.expected_result}</p>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
