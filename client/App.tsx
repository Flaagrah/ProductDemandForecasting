import { useState } from 'react';
import { Dashboard } from './components/Dashboard';
import { ProductDetailPage } from './components/ProductDetail';
import { SettingsPage } from './components/SettingsPage';
import { Button } from './components/ui/button';
import { LayoutDashboard, Settings, Package } from 'lucide-react';
import { Toaster } from './components/ui/sonner';

type Page = 'dashboard' | 'product' | 'settings';

export default function App() {
  const [currentPage, setCurrentPage] = useState<Page>('dashboard');
  const [selectedSku, setSelectedSku] = useState<string>('');

  function navigateToProduct(sku: string) {
    setSelectedSku(sku);
    setCurrentPage('product');
  }

  function navigateToDashboard() {
    setCurrentPage('dashboard');
  }

  function navigateToSettings() {
    setCurrentPage('settings');
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header / Navigation */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Package className="w-6 h-6 text-blue-600" />
              <h2 className="text-blue-600">Inventory Forecasting</h2>
            </div>
            
            <nav className="flex items-center gap-2">
              <Button
                variant={currentPage === 'dashboard' ? 'default' : 'ghost'}
                onClick={navigateToDashboard}
                className="flex items-center gap-2"
              >
                <LayoutDashboard className="w-4 h-4" />
                Dashboard
              </Button>
              <Button
                variant={currentPage === 'settings' ? 'default' : 'ghost'}
                onClick={navigateToSettings}
                className="flex items-center gap-2"
              >
                <Settings className="w-4 h-4" />
                Settings
              </Button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main>
        {currentPage === 'dashboard' && (
          <Dashboard onNavigateToProduct={navigateToProduct} />
        )}
        {currentPage === 'product' && (
          <ProductDetailPage sku={selectedSku} onBack={navigateToDashboard} />
        )}
        {currentPage === 'settings' && (
          <SettingsPage />
        )}
      </main>

      <Toaster />
    </div>
  );
}
