// Mock API service layer for inventory forecasting app

export interface KPISummary {
  skusAtRisk: number;
  healthySkusPercent: number;
  forecastedDemand30Days: number;
  demandChange: number;
  excessInventorySkus: number;
}

export interface Alert {
  id: string;
  sku: string;
  productName: string;
  issueType: 'stockout_risk' | 'overstock';
  daysOfSupply: number;
  recommendedAction: {
    reorderQty: number;
    byDate: string;
    confidence: number;
  };
  reasoning: string;
  linkedEvents?: string[];
}

export interface ExternalEvent {
  id: string;
  description: string;
  type: 'tariff' | 'holiday' | 'shipping_issue' | 'supplier_issue' | 'other';
  impactedSkus: string[];
  suggestedAction: string;
  startDate: string;
  endDate?: string;
}

export interface ProductDetail {
  sku: string;
  productName: string;
  supplier: string;
  currentInventory: {
    onHand: number;
    inbound: number;
  };
  forecastedDemand30Days: number;
  recommendedReorder: {
    qty: number;
    byDate: string;
    confidence: number;
  };
  reasoning: string;
  linkedEvents: string[];
  historicalSales: Array<{ date: string; quantity: number }>;
}

export interface Settings {
  thresholds: {
    stockoutDays: number;
    excessDays: number;
  };
  supplierLeadTimes: Array<{
    supplier: string;
    leadTimeDays: number;
  }>;
  notifications: {
    email: boolean;
    inApp: boolean;
    emailAddress?: string;
  };
}

// Mock data
const mockKPISummary: KPISummary = {
  skusAtRisk: 12,
  healthySkusPercent: 78,
  forecastedDemand30Days: 4850,
  demandChange: 12.5,
  excessInventorySkus: 8,
};

const mockAlerts: Alert[] = [
  {
    id: '1',
    sku: 'WH-BLK-M',
    productName: 'Wireless Headphones - Black Medium',
    issueType: 'stockout_risk',
    daysOfSupply: 3,
    recommendedAction: {
      reorderQty: 150,
      byDate: '2025-10-29',
      confidence: 92,
    },
    reasoning: 'Current inventory will deplete in 3 days based on 30-day moving average demand. Holiday season approaching.',
    linkedEvents: ['event-1'],
  },
  {
    id: '2',
    sku: 'TB-WHT-L',
    productName: 'Tote Bag - White Large',
    issueType: 'stockout_risk',
    daysOfSupply: 5,
    recommendedAction: {
      reorderQty: 200,
      byDate: '2025-11-01',
      confidence: 88,
    },
    reasoning: 'Increased demand detected due to seasonal trends. Supplier lead time is 14 days.',
    linkedEvents: ['event-2'],
  },
  {
    id: '3',
    sku: 'KB-MEC-BL',
    productName: 'Mechanical Keyboard - Blue Switches',
    issueType: 'overstock',
    daysOfSupply: 95,
    recommendedAction: {
      reorderQty: 0,
      byDate: '2025-12-15',
      confidence: 85,
    },
    reasoning: 'Current inventory exceeds 90 days of supply. Consider promotional campaigns to reduce excess stock.',
    linkedEvents: [],
  },
  {
    id: '4',
    sku: 'MS-WRL-BK',
    productName: 'Wireless Mouse - Black',
    issueType: 'stockout_risk',
    daysOfSupply: 7,
    recommendedAction: {
      reorderQty: 300,
      byDate: '2025-11-05',
      confidence: 90,
    },
    reasoning: 'Steady demand with holiday season approaching. Maintain safety stock levels.',
    linkedEvents: ['event-1'],
  },
  {
    id: '5',
    sku: 'LP-SLV-13',
    productName: 'Laptop Sleeve - Silver 13"',
    issueType: 'overstock',
    daysOfSupply: 68,
    recommendedAction: {
      reorderQty: 0,
      byDate: '2025-12-01',
      confidence: 82,
    },
    reasoning: 'Demand has decreased by 15% over the last 30 days. Excess inventory detected.',
    linkedEvents: [],
  },
];

const mockEvents: ExternalEvent[] = [
  {
    id: 'event-1',
    description: 'Holiday Season 2025 - Expected 40% increase in electronics demand',
    type: 'holiday',
    impactedSkus: ['WH-BLK-M', 'MS-WRL-BK', 'KB-MEC-BL'],
    suggestedAction: 'Increase safety stock for electronics category by 30%',
    startDate: '2025-11-20',
    endDate: '2025-12-31',
  },
  {
    id: 'event-2',
    description: 'Tariff increase on textile imports - 15% cost increase expected',
    type: 'tariff',
    impactedSkus: ['TB-WHT-L', 'BP-BLK-M'],
    suggestedAction: 'Consider alternative suppliers or adjust pricing strategy',
    startDate: '2025-11-01',
  },
  {
    id: 'event-3',
    description: 'Shipping delays from Asia Pacific - 7-10 day delays reported',
    type: 'shipping_issue',
    impactedSkus: ['WH-BLK-M', 'MS-WRL-BK', 'KB-MEC-BL'],
    suggestedAction: 'Add 10 days to lead time estimates for affected SKUs',
    startDate: '2025-10-20',
    endDate: '2025-11-15',
  },
];

const mockProductDetails: Record<string, ProductDetail> = {
  'WH-BLK-M': {
    sku: 'WH-BLK-M',
    productName: 'Wireless Headphones - Black Medium',
    supplier: 'AudioTech International',
    currentInventory: {
      onHand: 45,
      inbound: 100,
    },
    forecastedDemand30Days: 180,
    recommendedReorder: {
      qty: 150,
      byDate: '2025-10-29',
      confidence: 92,
    },
    reasoning: 'Current inventory will deplete in 3 days based on 30-day moving average demand. Holiday season approaching with expected 40% demand increase.',
    linkedEvents: ['event-1', 'event-3'],
    historicalSales: [
      { date: '2025-09-26', quantity: 12 },
      { date: '2025-09-27', quantity: 15 },
      { date: '2025-09-28', quantity: 18 },
      { date: '2025-09-29', quantity: 14 },
      { date: '2025-09-30', quantity: 16 },
      { date: '2025-10-01', quantity: 19 },
      { date: '2025-10-02', quantity: 22 },
      { date: '2025-10-03', quantity: 17 },
      { date: '2025-10-04', quantity: 20 },
      { date: '2025-10-05', quantity: 18 },
      { date: '2025-10-06', quantity: 21 },
      { date: '2025-10-07', quantity: 16 },
      { date: '2025-10-08', quantity: 19 },
      { date: '2025-10-09', quantity: 23 },
      { date: '2025-10-10', quantity: 25 },
    ],
  },
  'TB-WHT-L': {
    sku: 'TB-WHT-L',
    productName: 'Tote Bag - White Large',
    supplier: 'FashionCraft Co.',
    currentInventory: {
      onHand: 80,
      inbound: 50,
    },
    forecastedDemand30Days: 240,
    recommendedReorder: {
      qty: 200,
      byDate: '2025-11-01',
      confidence: 88,
    },
    reasoning: 'Increased demand detected due to seasonal trends. Supplier lead time is 14 days. Tariff increase may affect future costs.',
    linkedEvents: ['event-2'],
    historicalSales: [
      { date: '2025-09-26', quantity: 8 },
      { date: '2025-09-27', quantity: 9 },
      { date: '2025-09-28', quantity: 7 },
      { date: '2025-09-29', quantity: 10 },
      { date: '2025-09-30', quantity: 11 },
      { date: '2025-10-01', quantity: 12 },
      { date: '2025-10-02', quantity: 14 },
      { date: '2025-10-03', quantity: 13 },
      { date: '2025-10-04', quantity: 15 },
      { date: '2025-10-05', quantity: 16 },
      { date: '2025-10-06', quantity: 18 },
      { date: '2025-10-07', quantity: 17 },
      { date: '2025-10-08', quantity: 19 },
      { date: '2025-10-09', quantity: 20 },
      { date: '2025-10-10', quantity: 22 },
    ],
  },
};

const mockSettings: Settings = {
  thresholds: {
    stockoutDays: 7,
    excessDays: 60,
  },
  supplierLeadTimes: [
    { supplier: 'AudioTech International', leadTimeDays: 21 },
    { supplier: 'FashionCraft Co.', leadTimeDays: 14 },
    { supplier: 'TechSupply Corp', leadTimeDays: 28 },
  ],
  notifications: {
    email: true,
    inApp: true,
    emailAddress: 'merchant@store.com',
  },
};

// API functions with simulated delays
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const apiService = {
  async getDashboardSummary(): Promise<KPISummary> {
    await delay(300);
    return mockKPISummary;
  },

  async getDashboardAlerts(): Promise<Alert[]> {
    await delay(400);
    return mockAlerts;
  },

  async getEvents(): Promise<ExternalEvent[]> {
    await delay(350);
    return mockEvents;
  },

  async getProductDetail(sku: string): Promise<ProductDetail | null> {
    await delay(300);
    return mockProductDetails[sku] || null;
  },

  async getSettings(): Promise<Settings> {
    await delay(250);
    return mockSettings;
  },

  async updateSettings(settings: Settings): Promise<Settings> {
    await delay(400);
    Object.assign(mockSettings, settings);
    return mockSettings;
  },

  async getAllProducts(): Promise<Array<{ sku: string; productName: string }>> {
    await delay(300);
    return Object.values(mockProductDetails).map(p => ({
      sku: p.sku,
      productName: p.productName,
    }));
  },
};
