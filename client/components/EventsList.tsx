import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { AlertCircle, Calendar, Ship, DollarSign, Sparkles } from 'lucide-react';
import type { ExternalEvent } from '../mockApi';

interface EventsListProps {
  events: ExternalEvent[];
  loading: boolean;
}

const eventIcons = {
  tariff: DollarSign,
  holiday: Sparkles,
  shipping_issue: Ship,
  supplier_issue: AlertCircle,
  other: Calendar,
};

const eventColors = {
  tariff: 'bg-purple-100 text-purple-700 border-purple-200',
  holiday: 'bg-green-100 text-green-700 border-green-200',
  shipping_issue: 'bg-red-100 text-red-700 border-red-200',
  supplier_issue: 'bg-amber-100 text-amber-700 border-amber-200',
  other: 'bg-blue-100 text-blue-700 border-blue-200',
};

export function EventsList({ events, loading }: EventsListProps) {
  if (loading) {
    return (
      <div>
        <h3 className="mb-4">External Events</h3>
        <div className="space-y-3">
          {[1, 2, 3].map(i => (
            <Card key={i} className="p-4 animate-pulse">
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-3 bg-gray-200 rounded w-1/2"></div>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div>
      <h3 className="mb-4">External Events</h3>
      <p className="text-sm text-gray-600 mb-4">
        Events that may impact inventory and demand forecasting
      </p>
      
      <div className="space-y-3">
        {events.map(event => {
          const Icon = eventIcons[event.type];
          return (
            <Card key={event.id} className={`p-4 border-l-4 ${eventColors[event.type]}`}>
              <div className="flex items-start gap-3">
                <div className="mt-1">
                  <Icon className="w-5 h-5" />
                </div>
                <div className="flex-1">
                  <div className="flex items-start justify-between mb-2">
                    <h4>{event.description}</h4>
                    <Badge variant="outline" className="ml-2">
                      {event.type.replace('_', ' ')}
                    </Badge>
                  </div>
                  
                  <div className="text-sm text-gray-600 mb-3">
                    <div className="flex items-center gap-2 mb-1">
                      <Calendar className="w-4 h-4" />
                      <span>
                        {new Date(event.startDate).toLocaleDateString()}
                        {event.endDate && ` - ${new Date(event.endDate).toLocaleDateString()}`}
                      </span>
                    </div>
                    <div>
                      <span className="font-medium">Impacted SKUs:</span> {event.impactedSkus.join(', ')}
                    </div>
                  </div>
                  
                  <div className="bg-white bg-opacity-60 rounded p-3 border border-gray-200">
                    <p className="text-sm">
                      <span className="font-medium">Suggested Action:</span> {event.suggestedAction}
                    </p>
                  </div>
                </div>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
