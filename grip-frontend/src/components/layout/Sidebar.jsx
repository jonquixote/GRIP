import { useState } from 'react';
import { 
  Home, 
  BarChart3, 
  TrendingUp, 
  AlertTriangle, 
  Settings, 
  Moon, 
  Sun,
  Menu,
  X
} from 'lucide-react';

const Sidebar = ({ darkMode, setDarkMode }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const navigation = [
    { name: 'Dashboard', href: '#', icon: Home, current: true },
    { name: 'Analytics', href: '#', icon: BarChart3, current: false },
    { name: 'Predictions', href: '#', icon: TrendingUp, current: false },
    { name: 'Risk Alerts', href: '#', icon: AlertTriangle, current: false },
    { name: 'Settings', href: '#', icon: Settings, current: false },
  ];

  return (
    <>
      {/* Mobile sidebar toggle button */}
      <div className="md:hidden fixed top-4 left-4 z-30">
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="p-2 rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 focus:outline-none"
        >
          {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Sidebar - hidden on mobile by default, visible on desktop */}
      <div 
        className={`fixed inset-y-0 left-0 z-20 w-64 bg-white dark:bg-gray-800 shadow-lg transform transition-transform duration-300 ease-in-out md:translate-x-0 md:static md:transform-none ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex flex-col h-full">
          {/* Sidebar header */}
          <div className="flex items-center justify-between h-16 px-4 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center">
              <div className="bg-blue-600 text-white p-2 rounded-lg">
                <BarChart3 size={24} />
              </div>
              <span className="ml-3 text-xl font-bold text-gray-900 dark:text-white">GRIP</span>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="md:hidden text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
            >
              <X size={24} />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-2 py-4 space-y-1">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <a
                  key={item.name}
                  href={item.href}
                  className={`flex items-center px-4 py-3 text-base font-medium rounded-lg ${
                    item.current
                      ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100'
                      : 'text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
                  }`}
                >
                  <Icon className="mr-3 h-5 w-5" />
                  {item.name}
                </a>
              );
            })}
          </nav>

          {/* Dark mode toggle */}
          <div className="p-4 border-t border-gray-200 dark:border-gray-700">
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="w-full flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md text-gray-700 bg-gray-100 hover:bg-gray-200 dark:text-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600"
            >
              {darkMode ? (
                <>
                  <Sun className="mr-2 h-5 w-5" />
                  Light Mode
                </>
              ) : (
                <>
                  <Moon className="mr-2 h-5 w-5" />
                  Dark Mode
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-10 bg-black bg-opacity-50 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </>
  );
};

export default Sidebar;