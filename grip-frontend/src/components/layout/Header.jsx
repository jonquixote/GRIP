import { useState } from 'react';
import { Search, Bell, RefreshCw, User } from 'lucide-react';

const Header = ({ darkMode, setDarkMode, refreshData }) => {
  const [searchOpen, setSearchOpen] = useState(false);

  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm">
      <div className="flex items-center justify-between px-4 py-3 sm:px-6">
        {/* Left side - Title and Live indicator */}
        <div className="flex items-center">
          <h1 className="text-xl font-bold text-gray-900 dark:text-white">Global Resource Intelligence Platform</h1>
          <div className="ml-4 flex items-center">
            <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse"></div>
            <span className="ml-2 text-sm text-green-600 dark:text-green-400">Live</span>
          </div>
        </div>

        {/* Right side - Controls */}
        <div className="flex items-center space-x-4">
          {/* Search */}
          <div className="relative">
            {searchOpen ? (
              <input
                type="text"
                placeholder="Search commodities..."
                className="w-40 md:w-64 px-4 py-2 text-sm rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                onBlur={() => setSearchOpen(false)}
                autoFocus
              />
            ) : (
              <button
                onClick={() => setSearchOpen(true)}
                className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
              >
                <Search size={20} />
              </button>
            )}
          </div>

          {/* Refresh button */}
          <button
            onClick={refreshData}
            className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
          >
            <RefreshCw size={20} />
          </button>

          {/* Notifications */}
          <button className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300 relative">
            <Bell size={20} />
            <span className="absolute top-0 right-0 h-2 w-2 bg-red-500 rounded-full"></span>
          </button>

          {/* User profile */}
          <div className="flex items-center">
            <div className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center text-white">
              <User size={20} />
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;