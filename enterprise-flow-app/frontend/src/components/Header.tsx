/**
 * Header Component
 * Enterprise branding and navigation
 */

import React from 'react';
import { Sparkles } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="bg-gradient-to-r from-ibm-blue to-ibm-blue-dark text-white shadow-lg">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Sparkles className="w-8 h-8" />
            <div>
              <h1 className="text-2xl font-bold">Universal CrewAI Flow Generator</h1>
              <p className="text-sm text-blue-100">Enterprise AI Architecture Platform</p>
            </div>
          </div>
          <div className="text-sm text-blue-100">
            <span className="font-semibold">Powered by</span> IBM Watsonx + Langflow
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
