import { useEffect, useState } from 'react';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { ArrowLeft, Package, TrendingUp, AlertCircle, ExternalLink } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as ChartTooltip, ResponsiveContainer } from 'recharts';
import { apiService, type ProductDetail, type ExternalEvent } from '../mockApi';

interface ProductDetailProps {
  sku: string;
  onBack: () => void;
}

export function ProductDetailPage({ sku, onBack }: ProductDetailProps) {
  const [product, setProduct] = useState<ProductDetail | null>(null);
  const [events, setEvents] = useState<ExternalEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProductData();
  }, [sku]);

  async function loadProductData() {
    setLoading(true);
    try {
      const [productData, eventsData] = await Promise.all([
        apiService.getProductDetail(sku),
        apiService.getEvents(),
      ]);
      
      setProduct(productData);
      
      // Filter events linked to this product
      if (productData && productData.linkedEvents) {
        const linkedEvents = eventsData.filter(e => 
          productData.linkedEvents.includes(e.id)
        );
        setEvents(linkedEvents);
      }
    } catch (error) {
      console.error('Failed to load product data:', error);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/3"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="max-w-7xl mx-auto p-6">
        <Button variant="ghost" onClick={onBack} className="mb-4">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Dashboard
        </Button>
        <Card className="p-6 text-center">
          <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-2" />
          <p className="text-gray-600">Product not found</p>
        </Card>
      </div>
    );
  }

  const totalInventory = product.currentInventory.onHand + product.currentInventory.inbound;

  return (
    <div className="max-w-7xl mx-auto p-6">
      <Button variant="ghost" onClick={onBack} className="mb-4">
        <ArrowLeft className="w-4 h-4 mr-2" />
        Back to Dashboard
      </Button>

      <div className="mb-6">
        <div className="flex items-start justify-between">
          <div>
            <h1>{product.productName}</h1>
            <div className="flex items-center gap-3 mt-2">
              <code className="px-3 py-1 bg-gray-100 rounded">{product.sku}</code>
              <span className="text-gray-600">Supplier: {product.supplier}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <Card className="p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-gray-600">Current Inventory</span>
            <Package className="w-5 h-5 text-blue-500" />
          </div>
          <div className="text-blue-600">{totalInventory} units</div>
          <div className="text-sm text-gray-500 mt-1">
            {product.currentInventory.onHand} on hand + {product.currentInventory.inbound} inbound
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-gray-600">Forecasted Demand (30d)</span>
            <TrendingUp className="w-5 h-5 text-green-500" />
          </div>
          <div className="text-green-600">{product.forecastedDemand30Days} units</div>
          <div className="text-sm text-gray-500 mt-1">
            ~{Math.round(product.forecastedDemand30Days / 30)} units/day
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-gray-600">Days of Supply</span>
            <AlertCircle className="w-5 h-5 text-amber-500" />
          </div>
          <div className="text-amber-600">
            {Math.round((totalInventory / product.forecastedDemand30Days) * 30)} days
          </div>
          <div className="text-sm text-gray-500 mt-1">
            At current demand rate
          </div>
        </Card>
      </div>

      {/* Recommendation Card */}
      <Card className="p-6 mb-6 border-l-4 border-l-blue-500">
        <h3 className="mb-4">Recommendation</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <div className="mb-4">
              <div className="text-sm text-gray-600 mb-1">Recommended Reorder</div>
              <div className="text-blue-600">
                {product.recommendedReorder.qty} units
              </div>
            </div>
            
            <div className="mb-4">
              <div className="text-sm text-gray-600 mb-1">Order By Date</div>
              <div>
                {new Date(product.recommendedReorder.byDate).toLocaleDateString('en-US', {
                  weekday: 'long',
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </div>
            </div>

            <div>
              <div className="text-sm text-gray-600 mb-2">Confidence Level</div>
              <div className="flex items-center gap-3">
                <div className="flex-1 bg-gray-200 rounded-full h-3">
                  <div 
                    className="bg-blue-500 h-3 rounded-full"
                    style={{ width: `${product.recommendedReorder.confidence}%` }}
                  ></div>
                </div>
                <span>{product.recommendedReorder.confidence}%</span>
              </div>
            </div>
          </div>

          <div>
            <div className="text-sm text-gray-600 mb-2">Reasoning</div>
            <p className="text-gray-700">{product.reasoning}</p>
          </div>
        </div>
      </Card>

      {/* Historical Sales Chart */}
      <Card className="p-6 mb-6">
        <h3 className="mb-4">Historical Sales (Last 15 Days)</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={product.historicalSales}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
            />
            <YAxis />
            <ChartTooltip 
              labelFormatter={(value) => new Date(value).toLocaleDateString()}
              formatter={(value: number) => [`${value} units`, 'Sales']}
            />
            <Line 
              type="monotone" 
              dataKey="quantity" 
              stroke="#3b82f6" 
              strokeWidth={2}
              dot={{ fill: '#3b82f6', r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </Card>

      {/* Linked Events */}
      {events.length > 0 && (
        <Card className="p-6">
          <h3 className="mb-4">Linked External Events</h3>
          <div className="space-y-3">
            {events.map(event => (
              <div key={event.id} className="border rounded-lg p-4">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <h4>{event.description}</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      {new Date(event.startDate).toLocaleDateString()}
                      {event.endDate && ` - ${new Date(event.endDate).toLocaleDateString()}`}
                    </p>
                  </div>
                  <Badge variant="outline">{event.type.replace('_', ' ')}</Badge>
                </div>
                <div className="bg-gray-50 rounded p-3 mt-2">
                  <p className="text-sm">
                    <span className="font-medium">Suggested Action:</span> {event.suggestedAction}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}
