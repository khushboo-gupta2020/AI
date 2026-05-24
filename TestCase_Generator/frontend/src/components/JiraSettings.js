import React, { useState } from 'react';
import { testConnection } from '../services/api';

const JiraSettings = ({ config, setConfig, onNotify }) => {
  const [testing, setTesting] = useState(false);

  const handleChange = (e) => {
    setConfig({ ...config, [e.target.name]: e.target.value });
  };

  const handleTestConnection = async () => {
    if (!config.base_url || !config.email || !config.api_token) {
      onNotify({ type: 'error', message: 'Please fill in all required fields' });
      return;
    }

    setTesting(true);
    try {
      const result = await testConnection(config);
      onNotify({ type: 'success', message: result.message });
    } catch (error) {
      onNotify({
        type: 'error',
        message: error.response?.data?.detail || 'Connection failed',
      });
    } finally {
      setTesting(false);
    }
  };

  const handleSave = () => {
    localStorage.setItem('jiraConfig', JSON.stringify(config));
    onNotify({ type: 'success', message: 'Configuration saved' });
  };

  return (
    <div className="p-4">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">Jira Connection Settings</h2>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Jira Base URL *
          </label>
          <input
            type="text"
            name="base_url"
            value={config.base_url}
            onChange={handleChange}
            placeholder="https://your-domain.atlassian.net"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Email / Username *
          </label>
          <input
            type="email"
            name="email"
            value={config.email}
            onChange={handleChange}
            placeholder="your-email@example.com"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            API Token *
          </label>
          <input
            type="password"
            name="api_token"
            value={config.api_token}
            onChange={handleChange}
            placeholder="Enter API token"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Project Key (Optional)
          </label>
          <input
            type="text"
            name="project_key"
            value={config.project_key}
            onChange={handleChange}
            placeholder="e.g., PROJ"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          />
        </div>

        <div className="flex gap-2 pt-2">
          <button
            onClick={handleTestConnection}
            disabled={testing}
            className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-blue-300 transition text-sm font-medium"
          >
            {testing ? 'Testing...' : 'Test Connection'}
          </button>
          <button
            onClick={handleSave}
            className="flex-1 bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition text-sm font-medium"
          >
            Save Config
          </button>
        </div>
      </div>
    </div>
  );
};

export default JiraSettings;
