import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { ExternalLink, Info } from 'lucide-react';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from './ui/tooltip';
import type { Alert } from '../mockApi';

interface AlertsTableProps {
  alerts: Alert[];
  loading: boolean;
  onViewProduct: (sku: string) => void;
}

export function AlertsTable({ alerts, loading, onViewProduct }: AlertsTableProps) {
  if (loading) {
    return (
      <div className="border rounded-lg p-6 animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-1/4 mb-4"></div>
        <div className="space-y-3">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-12 bg-gray-200 rounded"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="border rounded-lg overflow-hidden">
      <div className="p-4 bg-gray-50 border-b">
        <h3>Priority Alerts</h3>
        <p className="text-sm text-gray-600 mt-1">
          {alerts.length} SKU{alerts.length !== 1 ? 's' : ''} requiring attention
        </p>
      </div>
      
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>SKU</TableHead>
              <TableHead>Product Name</TableHead>
              <TableHead>Issue Type</TableHead>
              <TableHead>Days of Supply</TableHead>
              <TableHead>Recommended Action</TableHead>
              <TableHead>Confidence</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {alerts.map(alert => (
              <TableRow key={alert.id}>
                <TableCell>
                  <code className="px-2 py-1 bg-gray-100 rounded text-sm">{alert.sku}</code>
                </TableCell>
                <TableCell>{alert.productName}</TableCell>
                <TableCell>
                  <Badge 
                    variant={alert.issueType === 'stockout_risk' ? 'destructive' : 'default'}
                    className={alert.issueType === 'overstock' ? 'bg-amber-500 hover:bg-amber-600' : ''}
                  >
                    {alert.issueType === 'stockout_risk' ? 'Stockout Risk' : 'Overstock'}
                  </Badge>
                </TableCell>
                <TableCell>
                  <span className={
                    alert.daysOfSupply < 7 
                      ? 'text-red-600' 
                      : alert.daysOfSupply > 60 
                      ? 'text-amber-600' 
                      : 'text-green-600'
                  }>
                    {alert.daysOfSupply} days
                  </span>
                </TableCell>
                <TableCell>
                  <div className="space-y-1">
                    <div>
                      {alert.recommendedAction.reorderQty > 0 ? (
                        <>
                          <span>Reorder {alert.recommendedAction.reorderQty} units</span>
                          <br />
                          <span className="text-sm text-gray-500">
                            by {new Date(alert.recommendedAction.byDate).toLocaleDateString()}
                          </span>
                        </>
                      ) : (
                        <span className="text-gray-600">No reorder needed until {new Date(alert.recommendedAction.byDate).toLocaleDateString()}</span>
                      )}
                    </div>
                    {alert.linkedEvents && alert.linkedEvents.length > 0 && (
                      <Badge variant="outline" className="text-xs">
                        {alert.linkedEvents.length} linked event{alert.linkedEvents.length !== 1 ? 's' : ''}
                      </Badge>
                    )}
                  </div>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <div className="w-12 bg-gray-200 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${
                          alert.recommendedAction.confidence >= 90 
                            ? 'bg-green-500' 
                            : alert.recommendedAction.confidence >= 75 
                            ? 'bg-blue-500' 
                            : 'bg-amber-500'
                        }`}
                        style={{ width: `${alert.recommendedAction.confidence}%` }}
                      ></div>
                    </div>
                    <span className="text-sm">{alert.recommendedAction.confidence}%</span>
                    <TooltipProvider>
                      <Tooltip>
                        <TooltipTrigger>
                          <Info className="w-4 h-4 text-gray-400" />
                        </TooltipTrigger>
                        <TooltipContent className="max-w-xs">
                          <p className="text-sm">{alert.reasoning}</p>
                        </TooltipContent>
                      </Tooltip>
                    </TooltipProvider>
                  </div>
                </TableCell>
                <TableCell>
                  <Button 
                    variant="ghost" 
                    size="sm"
                    onClick={() => onViewProduct(alert.sku)}
                  >
                    <ExternalLink className="w-4 h-4 mr-1" />
                    Details
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
