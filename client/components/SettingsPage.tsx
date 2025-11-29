import { useEffect, useState } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Switch } from './ui/switch';
import { Separator } from './ui/separator';
import { Save, Plus, Trash2 } from 'lucide-react';
import { toast } from 'sonner';
import { apiService, type Settings } from '../mockApi';

export function SettingsPage() {
  const [settings, setSettings] = useState<Settings | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadSettings();
  }, []);

  async function loadSettings() {
    setLoading(true);
    try {
      const data = await apiService.getSettings();
      setSettings(data);
    } catch (error) {
      console.error('Failed to load settings:', error);
      toast.error('Failed to load settings');
    } finally {
      setLoading(false);
    }
  }

  async function handleSave() {
    if (!settings) return;
    
    setSaving(true);
    try {
      await apiService.updateSettings(settings);
      toast.success('Settings saved successfully');
    } catch (error) {
      console.error('Failed to save settings:', error);
      toast.error('Failed to save settings');
    } finally {
      setSaving(false);
    }
  }

  function addSupplier() {
    if (!settings) return;
    
    setSettings({
      ...settings,
      supplierLeadTimes: [
        ...settings.supplierLeadTimes,
        { supplier: '', leadTimeDays: 14 }
      ]
    });
  }

  function removeSupplier(index: number) {
    if (!settings) return;
    
    setSettings({
      ...settings,
      supplierLeadTimes: settings.supplierLeadTimes.filter((_, i) => i !== index)
    });
  }

  function updateSupplier(index: number, field: 'supplier' | 'leadTimeDays', value: string | number) {
    if (!settings) return;
    
    const updated = [...settings.supplierLeadTimes];
    updated[index] = {
      ...updated[index],
      [field]: value
    };
    
    setSettings({
      ...settings,
      supplierLeadTimes: updated
    });
  }

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/3"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (!settings) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <p className="text-gray-600">Failed to load settings</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-6">
        <h1>Settings</h1>
        <p className="text-gray-600 mt-1">
          Configure thresholds, supplier lead times, and notification preferences
        </p>
      </div>

      {/* Inventory Thresholds */}
      <Card className="p-6 mb-6">
        <h3 className="mb-4">Inventory Thresholds</h3>
        <p className="text-sm text-gray-600 mb-6">
          Define when SKUs are flagged as at-risk or excess
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <Label htmlFor="stockout-days">Stockout Risk Threshold (Days)</Label>
            <Input
              id="stockout-days"
              type="number"
              min="1"
              value={settings.thresholds.stockoutDays}
              onChange={(e) => setSettings({
                ...settings,
                thresholds: {
                  ...settings.thresholds,
                  stockoutDays: parseInt(e.target.value) || 7
                }
              })}
              className="mt-2"
            />
            <p className="text-sm text-gray-500 mt-1">
              Alert when days of supply falls below this value
            </p>
          </div>

          <div>
            <Label htmlFor="excess-days">Excess Inventory Threshold (Days)</Label>
            <Input
              id="excess-days"
              type="number"
              min="1"
              value={settings.thresholds.excessDays}
              onChange={(e) => setSettings({
                ...settings,
                thresholds: {
                  ...settings.thresholds,
                  excessDays: parseInt(e.target.value) || 60
                }
              })}
              className="mt-2"
            />
            <p className="text-sm text-gray-500 mt-1">
              Alert when days of supply exceeds this value
            </p>
          </div>
        </div>
      </Card>

      {/* Supplier Lead Times */}
      <Card className="p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3>Supplier Lead Times</h3>
            <p className="text-sm text-gray-600 mt-1">
              Configure expected delivery times for each supplier
            </p>
          </div>
          <Button onClick={addSupplier} variant="outline" size="sm">
            <Plus className="w-4 h-4 mr-2" />
            Add Supplier
          </Button>
        </div>

        <div className="space-y-4">
          {settings.supplierLeadTimes.map((supplier, index) => (
            <div key={index} className="flex items-end gap-4 p-4 border rounded-lg">
              <div className="flex-1">
                <Label htmlFor={`supplier-${index}`}>Supplier Name</Label>
                <Input
                  id={`supplier-${index}`}
                  value={supplier.supplier}
                  onChange={(e) => updateSupplier(index, 'supplier', e.target.value)}
                  placeholder="Enter supplier name"
                  className="mt-2"
                />
              </div>
              <div className="w-48">
                <Label htmlFor={`leadtime-${index}`}>Lead Time (Days)</Label>
                <Input
                  id={`leadtime-${index}`}
                  type="number"
                  min="1"
                  value={supplier.leadTimeDays}
                  onChange={(e) => updateSupplier(index, 'leadTimeDays', parseInt(e.target.value) || 14)}
                  className="mt-2"
                />
              </div>
              <Button 
                variant="ghost" 
                size="sm"
                onClick={() => removeSupplier(index)}
              >
                <Trash2 className="w-4 h-4 text-red-500" />
              </Button>
            </div>
          ))}
        </div>
      </Card>

      {/* Notifications */}
      <Card className="p-6 mb-6">
        <h3 className="mb-4">Notification Preferences</h3>
        <p className="text-sm text-gray-600 mb-6">
          Choose how you want to receive alerts
        </p>

        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <Label htmlFor="email-notif">Email Notifications</Label>
              <p className="text-sm text-gray-500 mt-1">
                Receive alerts via email
              </p>
            </div>
            <Switch
              id="email-notif"
              checked={settings.notifications.email}
              onCheckedChange={(checked) => setSettings({
                ...settings,
                notifications: {
                  ...settings.notifications,
                  email: checked
                }
              })}
            />
          </div>

          {settings.notifications.email && (
            <div>
              <Label htmlFor="email-address">Email Address</Label>
              <Input
                id="email-address"
                type="email"
                value={settings.notifications.emailAddress || ''}
                onChange={(e) => setSettings({
                  ...settings,
                  notifications: {
                    ...settings.notifications,
                    emailAddress: e.target.value
                  }
                })}
                placeholder="your@email.com"
                className="mt-2"
              />
            </div>
          )}

          <Separator />

          <div className="flex items-center justify-between">
            <div>
              <Label htmlFor="inapp-notif">In-App Notifications</Label>
              <p className="text-sm text-gray-500 mt-1">
                Show alerts within the app
              </p>
            </div>
            <Switch
              id="inapp-notif"
              checked={settings.notifications.inApp}
              onCheckedChange={(checked) => setSettings({
                ...settings,
                notifications: {
                  ...settings.notifications,
                  inApp: checked
                }
              })}
            />
          </div>
        </div>
      </Card>

      {/* Save Button */}
      <div className="flex justify-end">
        <Button onClick={handleSave} disabled={saving}>
          <Save className="w-4 h-4 mr-2" />
          {saving ? 'Saving...' : 'Save Settings'}
        </Button>
      </div>
    </div>
  );
}
