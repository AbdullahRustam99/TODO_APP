'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useTheme } from '@/context/ThemeContext';
import { Sidebar } from '@/components/UI/Sidebar';
import { Button } from '@/components/UI/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/UI/Card';
import { Input } from '@/components/UI/Input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/UI/Select';
import { Switch } from '@/components/UI/Switch';
import { Label } from '@/components/UI/Label';
import { useTaskContext } from '@/context/TaskContext';
import { Task, Theme } from '@/lib/types';
import { useRouter } from 'next/navigation';
import { cn } from '@/lib/utils';

export default function SettingsPage() {
  const { user, logout } = useAuth();
  const { theme, setTheme, toggleTheme } = useTheme();
  const router = useRouter();
  const { setCurrentView } = useTaskContext();

  const handleLogout = () => {
    logout();
    router.replace('/');
  };
  const [isVisible, setIsVisible] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [profile, setProfile] = useState({
    name: user?.name || '',
    email: user?.email || '',
    notifications: true,
    taskReminders: true,
    weeklyReports: false,
    theme: 'system' as 'light' | 'dark' | 'system',
  });

  useEffect(() => {
    setIsVisible(true);
    // Set current view to list for the settings page (since settings view doesn't exist in context)
    setCurrentView('list');
  }, []); // Empty dependency array to run only once on mount


  const handleSaveProfile = (e: React.FormEvent) => {
    e.preventDefault();
    // In a real app, this would save to the backend
    console.log('Saving profile:', profile);
    alert('Profile settings saved successfully!');
  };

  const handleInputChange = (field: keyof typeof profile, value: string | boolean) => {
    setProfile(prev => ({
      ...prev,
      [field]: value
    }));
  };

  if (!user) {
    return null;
  }

  return (
    <div className="h-full bg-[#0F0F0F] text-white flex">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Header */}
        <header className="border-b border-gray-700 bg-[#1C1C1C] backdrop-blur-sm sticky top-0 z-10 animate-fade-in">
          <div className="flex items-center justify-between px-6 py-4">
            <div className="flex items-center">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="lg:hidden mr-4 text-gray-400 hover:text-white focus:outline-none"
                aria-label="Toggle sidebar"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              <h1 className="text-xl font-bold">Settings</h1>
            </div>

            <div className="flex items-center space-x-4">
              {/* Notifications */}
              <button className="text-gray-400 hover:text-white relative" aria-label="Notifications">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span>
              </button>

              {/* User Profile */}
              <div className="flex items-center">
                <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center">
                  <span className="text-sm font-medium">U</span>
                </div>
                <span className="ml-2 text-sm hidden md:block">{user?.name || user?.email}</span>
              </div>

              <Button
                variant="outline"
                onClick={handleLogout}
                className="ml-4 animate-scale"
                aria-label="Logout"
              >
                Logout
              </Button>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main id="main-content" className="flex-1 overflow-y-auto p-6 focus:outline-none" tabIndex={-1}>
          <div className={`max-w-4xl mx-auto animate-fade-in ${isVisible ? 'opacity-100' : 'opacity-0'}`}>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Profile Settings */}
              <div className="lg:col-span-2">
                <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm animate-slide-in-left">
                  <CardHeader>
                    <CardTitle className="text-xl">Profile Settings</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <form onSubmit={handleSaveProfile} className="space-y-6">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                          <Label htmlFor="name" className="text-gray-300">Name</Label>
                          <Input
                            id="name"
                            type="text"
                            value={profile.name}
                            onChange={(e) => handleInputChange('name', e.target.value)}
                            className="bg-gray-800/50 border-gray-700 text-white"
                            aria-label="Your name"
                          />
                        </div>
                        <div>
                          <Label htmlFor="email" className="text-gray-300">Email</Label>
                          <Input
                            id="email"
                            type="email"
                            value={profile.email}
                            onChange={(e) => handleInputChange('email', e.target.value)}
                            className="bg-gray-800/50 border-gray-700 text-white"
                            aria-label="Your email address"
                          />
                        </div>
                      </div>

                      <div className="flex justify-end">
                        <Button type="submit" className="bg-gradient-to-r from-orange-500 to-yellow-500 hover:from-orange-600 hover:to-yellow-600 text-white">
                          Save Profile
                        </Button>
                      </div>
                    </form>
                  </CardContent>
                </Card>

                {/* Notification Settings */}
                <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm animate-slide-in-up delay-150 mt-6">
                  <CardHeader>
                    <CardTitle className="text-xl">Notification Settings</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <Label className="text-gray-300">Email Notifications</Label>
                          <p className="text-sm text-gray-500">Receive emails about account activity</p>
                        </div>
                        <Switch
                          checked={profile.notifications}
                          onCheckedChange={(checked) => handleInputChange('notifications', checked)}
                          aria-label="Toggle email notifications"
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <div>
                          <Label className="text-gray-300">Task Reminders</Label>
                          <p className="text-sm text-gray-500">Get reminders for upcoming tasks</p>
                        </div>
                        <Switch
                          checked={profile.taskReminders}
                          onCheckedChange={(checked) => handleInputChange('taskReminders', checked)}
                          aria-label="Toggle task reminders"
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <div>
                          <Label className="text-gray-300">Weekly Reports</Label>
                          <p className="text-sm text-gray-500">Receive weekly productivity reports</p>
                        </div>
                        <Switch
                          checked={profile.weeklyReports}
                          onCheckedChange={(checked) => handleInputChange('weeklyReports', checked)}
                          aria-label="Toggle weekly reports"
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Theme and App Settings */}
              <div>
                <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm animate-slide-in-right">
                  <CardHeader>
                    <CardTitle className="text-xl">Appearance</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <Label className="text-gray-300">Theme</Label>
                        <Select value={theme} onValueChange={(value: string) => setTheme(value as Theme)}>
                          <SelectTrigger className="w-full bg-gray-800/50 border-gray-700 text-white">
                            <SelectValue placeholder="Select theme" />
                          </SelectTrigger>
                          <SelectContent className="bg-[#1C1C1C] border-gray-700">
                            <SelectItem value="light">Light</SelectItem>
                            <SelectItem value="dark">Dark</SelectItem>
                            <SelectItem value="system">System</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="flex items-center justify-between pt-4">
                        <div>
                          <Label className="text-gray-300">Compact Mode</Label>
                          <p className="text-sm text-gray-500">Use compact spacing in lists</p>
                        </div>
                        <Switch
                          aria-label="Toggle compact mode"
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <div>
                          <Label className="text-gray-300">Reduced Motion</Label>
                          <p className="text-sm text-gray-500">Minimize animations</p>
                        </div>
                        <Switch
                          aria-label="Toggle reduced motion"
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Account Actions */}
                <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm animate-slide-in-right delay-150 mt-6">
                  <CardHeader>
                    <CardTitle className="text-xl">Account Actions</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <Button variant="outline" className="w-full justify-start">
                        Change Password
                      </Button>
                      <Button variant="outline" className="w-full justify-start">
                        Export Data
                      </Button>
                      <Button variant="outline" className="w-full justify-start text-red-500 hover:text-red-400 border-red-500/30 hover:bg-red-500/10">
                        Delete Account
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}