import { useEffect, useState } from 'react';
import { KPICards } from './KPICards';
import { AlertsTable } from './AlertsTable';
import { EventsList } from './EventsList';
import { apiService, type KPISummary, type Alert, type ExternalEvent } from '../mockApi';

interface DashboardProps {
  onNavigateToProduct: (sku: string) => void;
}

export function Dashboard({ onNavigateToProduct }: DashboardProps) {
  const [kpiData, setKpiData] = useState<KPISummary | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [events, setEvents] = useState<ExternalEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  async function loadDashboardData() {
    setLoading(true);
    try {
      const [kpiResponse, alertsResponse, eventsResponse] = await Promise.all([
        apiService.getDashboardSummary(),
        apiService.getDashboardAlerts(),
        apiService.getEvents(),
      ]);
      
      setKpiData(kpiResponse);
      setAlerts(alertsResponse);
      setEvents(eventsResponse);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="mb-6">
        <h1>Inventory & Demand Forecasting</h1>
        <p className="text-gray-600 mt-1">
          Real-time insights and recommendations for your inventory
        </p>
      </div>

      <KPICards data={kpiData} loading={loading} />
      
      <div className="mb-6">
        <AlertsTable 
          alerts={alerts} 
          loading={loading}
          onViewProduct={onNavigateToProduct}
        />
      </div>

      <EventsList events={events} loading={loading} />
    </div>
  );
}
