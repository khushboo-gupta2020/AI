import React, { useState, useEffect } from 'react';
import JiraSettings from './components/JiraSettings';
import TestCaseForm from './components/TestCaseForm';
import TestCaseTable from './components/TestCaseTable';
import Notification from './components/Notification';

function App() {
  const [config, setConfig] = useState({
    base_url: '',
    email: '',
    api_token: '',
    project_key: '',
  });
  const [notification, setNotification] = useState(null);
  const [testCases, setTestCases] = useState([]);
  const [storyData, setStoryData] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem('jiraConfig');
    if (saved) {
      setConfig(JSON.parse(saved));
    }
  }, []);

  const handleNotify = (notif) => {
    setNotification(notif);
  };

  const handleTestCasesGenerated = (result) => {
    setTestCases(result.test_cases || []);
    setStoryData(result.story_data || null);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex">
      <Notification notification={notification} onClose={() => setNotification(null)} />

      {/* Mobile sidebar toggle */}
      <button
        className="lg:hidden fixed top-4 left-4 z-40 bg-white p-2 rounded-md shadow-md"
        onClick={() => setSidebarOpen(!sidebarOpen)}
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      {/* Left Sidebar */}
      <aside
        className={`fixed lg:static inset-y-0 left-0 z-30 w-80 bg-white shadow-lg transform transition-transform duration-200 ease-in-out ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="h-full overflow-y-auto">
          <div className="p-4 border-b border-gray-200">
            <h1 className="text-xl font-bold text-gray-800 flex items-center gap-2">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
              Test Case Generator
            </h1>
          </div>
          <JiraSettings config={config} setConfig={setConfig} onNotify={handleNotify} />
        </div>
      </aside>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-6xl mx-auto">
          <div className="bg-white shadow-sm rounded-lg mt-4 mx-4 lg:mx-0">
            <TestCaseForm
              config={config}
              onNotify={handleNotify}
              onTestCasesGenerated={handleTestCasesGenerated}
            />
          </div>

          <div className="bg-white shadow-sm rounded-lg mt-4 mx-4 lg:mx-0 mb-8">
            <TestCaseTable
              testCases={testCases}
              storyData={storyData}
              onNotify={handleNotify}
            />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
