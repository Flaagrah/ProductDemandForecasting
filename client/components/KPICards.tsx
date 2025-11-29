import { Card } from './ui/card';
import { TrendingUp, TrendingDown, Package, AlertTriangle, CheckCircle2, PackageX } from 'lucide-react';
import type { KPISummary } from '../mockApi';

interface KPICardsProps {
  data: KPISummary | null;
  loading: boolean;
}

export function KPICards({ data, loading }: KPICardsProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {[1, 2, 3, 4].map(i => (
          <Card key={i} className="p-6 animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
            <div className="h-8 bg-gray-200 rounded w-3/4"></div>
          </Card>
        ))}
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {/* SKUs at Risk */}
      <Card className="p-6 border-l-4 border-l-red-500">
        <div className="flex items-start justify-between mb-2">
          <span className="text-gray-600">SKUs at Risk of Stockout</span>
          <AlertTriangle className="w-5 h-5 text-red-500" />
        </div>
        <div className="text-red-600">{data.skusAtRisk}</div>
        <p className="text-sm text-gray-500 mt-1">Immediate attention required</p>
      </Card>

      {/* Healthy SKUs */}
      <Card className="p-6 border-l-4 border-l-green-500">
        <div className="flex items-start justify-between mb-2">
          <span className="text-gray-600">Healthy SKUs</span>
          <CheckCircle2 className="w-5 h-5 text-green-500" />
        </div>
        <div className="text-green-600">{data.healthySkusPercent}%</div>
        <p className="text-sm text-gray-500 mt-1">Operating within target range</p>
      </Card>

      {/* Forecasted Demand */}
      <Card className="p-6 border-l-4 border-l-blue-500">
        <div className="flex items-start justify-between mb-2">
          <span className="text-gray-600">Forecasted Demand (30d)</span>
          <Package className="w-5 h-5 text-blue-500" />
        </div>
        <div className="text-blue-600">{data.forecastedDemand30Days.toLocaleString()}</div>
        <div className="flex items-center text-sm mt-1">
          {data.demandChange >= 0 ? (
            <>
              <TrendingUp className="w-4 h-4 text-green-500 mr-1" />
              <span className="text-green-600">+{data.demandChange}%</span>
            </>
          ) : (
            <>
              <TrendingDown className="w-4 h-4 text-red-500 mr-1" />
              <span className="text-red-600">{data.demandChange}%</span>
            </>
          )}
          <span className="text-gray-500 ml-1">vs last 30d</span>
        </div>
      </Card>

      {/* Excess Inventory */}
      <Card className="p-6 border-l-4 border-l-amber-500">
        <div className="flex items-start justify-between mb-2">
          <span className="text-gray-600">Excess Inventory SKUs</span>
          <PackageX className="w-5 h-5 text-amber-500" />
        </div>
        <div className="text-amber-600">{data.excessInventorySkus}</div>
        <p className="text-sm text-gray-500 mt-1">Consider promotional action</p>
      </Card>
    </div>
  );
}
