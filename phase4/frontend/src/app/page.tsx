'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/UI/Button';
import { useAuth } from '@/context/AuthContext';
import { Chatbot } from './Chatbot';

export default function Home() {
  const { user } = useAuth();
  const router = useRouter();
  const [isHovered, setIsHovered] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const [isChatbotOpen, setIsChatbotOpen] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const handleGetStarted = () => {
    if (user) {
      router.push('/dashboard');
    } else {
      router.push('/signup');
    }
  };

  return (
    <div className="h-full bg-gradient-to-br from-gray-900 to-black text-white">
      {/* Animated Background Elements */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute -top-1/2 left-1/4 w-96 h-96 bg-orange-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute top-1/3 right-1/4 w-96 h-96 bg-yellow-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      {/* Dark Header with Navigation */}
      <header className="border-b border-gray-800 bg-gray-900/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2 animate-slide-in-left">
            <div className="w-8 h-8 bg-orange-500 rounded-lg"></div>
            <span className="text-xl font-bold">Todo App</span>
          </div>

          <nav className="hidden md:flex items-center space-x-8 animate-slide-in-right">
            <a href="#features" className="text-gray-300 hover:text-white transition-colors hover:text-orange-400">Features</a>
            <a href="#pricing" className="text-gray-300 hover:text-white transition-colors hover:text-orange-400">Pricing</a>
            <a href="#about" className="text-gray-300 hover:text-white transition-colors hover:text-orange-400">About</a>
            <a href="/login" className="text-gray-300 hover:text-white transition-colors hover:text-orange-400">Login</a>
          </nav>

          <Button
            variant="primary"
            onClick={() => router.push('/login')}
            className="hidden md:block animate-slide-in-right"
          >
            Sign In
          </Button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 md:py-32 relative">
        <div className="container mx-auto px-4 text-center">
          <h1 className={`text-4xl md:text-6xl font-bold mb-6 animate-fade-in ${isVisible ? 'opacity-100' : 'opacity-0'}`}>
            Simplify Your Life with <span className="text-orange-500">Smart Task Management</span>
          </h1>
          <p className={`text-xl text-gray-300 mb-10 max-w-2xl mx-auto animate-fade-in delay-150 ${isVisible ? 'opacity-100' : 'opacity-0'}`}>
            The most intuitive and powerful todo app designed to boost your productivity and keep you organized.
          </p>
          <div className={`flex flex-col sm:flex-row justify-center gap-4 animate-fade-in delay-300 ${isVisible ? 'opacity-100' : 'opacity-0'}`}>
            <Button
              variant="primary"
              size="lg"
              onClick={handleGetStarted}
              onMouseEnter={() => setIsHovered(true)}
              onMouseLeave={() => setIsHovered(false)}
              className="px-8 py-4 text-lg animate-scale"
            >
              {user ? 'Go to Dashboard' : 'Get Started Free'}
            </Button>
            <Button
              variant="outline"
              size="lg"
              onClick={() => router.push('/login')}
              className="px-8 py-4 text-lg animate-scale"
            >
              Sign In
            </Button>
          </div>
        </div>
      </section>

      {/* Feature Cards */}
      <section id="features" className="py-16 bg-gray-900/50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 animate-fade-in">Why Choose Our Todo App</h2>
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {/* Fast & Simple Card */}
            <div className="bg-gray-800/50 p-8 rounded-xl border border-gray-700 hover:border-orange-500/50 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 animate-slide-in-left">
              <div className="w-12 h-12 bg-orange-500 rounded-lg mb-6 flex items-center justify-center animate-bounce">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-4">Fast & Simple</h3>
              <p className="text-gray-300">
                Lightning-fast task creation and management with an intuitive interface that requires zero learning curve.
              </p>
            </div>

            {/* Smart Priorities Card */}
            <div className="bg-gray-800/50 p-8 rounded-xl border border-gray-700 hover:border-yellow-500/50 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 animate-slide-down">
              <div className="w-12 h-12 bg-yellow-500 rounded-lg mb-6 flex items-center justify-center animate-bounce delay-300">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-4">Smart Priorities</h3>
              <p className="text-gray-300">
                Intelligent priority system that learns your habits and suggests optimal task ordering.
              </p>
            </div>

            {/* Secure Sync Card */}
            <div className="bg-gray-800/50 p-8 rounded-xl border border-gray-700 hover:border-orange-500/50 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 animate-slide-in-right">
              <div className="w-12 h-12 bg-orange-500 rounded-lg mb-6 flex items-center justify-center animate-bounce delay-500">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-4">Secure Sync</h3>
              <p className="text-gray-300">
                Enterprise-grade security with seamless cross-device synchronization that keeps your data safe.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 animate-fade-in">What Our Users Say</h2>
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-700 animate-slide-in-left">
              <div className="flex items-center mb-4">
                <div className="w-10 h-10 bg-orange-500 rounded-full flex items-center justify-center text-sm font-bold">JD</div>
                <div className="ml-3">
                  <h4 className="font-bold">John Doe</h4>
                  <div className="flex text-yellow-400">
                    {'★'.repeat(5)}
                  </div>
                </div>
              </div>
              <p className="text-gray-300">
                "This app has completely transformed how I manage my tasks. The smart priorities feature is a game-changer!"
              </p>
            </div>

            <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-700 animate-slide-down">
              <div className="flex items-center mb-4">
                <div className="w-10 h-10 bg-yellow-500 rounded-full flex items-center justify-center text-sm font-bold">AS</div>
                <div className="ml-3">
                  <h4 className="font-bold">Alice Smith</h4>
                  <div className="flex text-yellow-400">
                    {'★'.repeat(5)}
                  </div>
                </div>
              </div>
              <p className="text-gray-300">
                "The clean interface and smooth animations make task management actually enjoyable. Highly recommended!"
              </p>
            </div>

            <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-700 animate-slide-in-right">
              <div className="flex items-center mb-4">
                <div className="w-10 h-10 bg-orange-500 rounded-full flex items-center justify-center text-sm font-bold">RB</div>
                <div className="ml-3">
                  <h4 className="font-bold">Robert Brown</h4>
                  <div className="flex text-yellow-400">
                    {'★'.repeat(5)}
                  </div>
                </div>
              </div>
              <p className="text-gray-300">
                "The secure sync feature gives me peace of mind. I can access my tasks from anywhere without worry."
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-12 mt-16">
        <div className="container mx-auto px-4 text-center">
          <div className="flex justify-center mb-6 animate-slide-in-up">
            <div className="w-8 h-8 bg-orange-500 rounded-lg"></div>
          </div>
          <p className="text-gray-400 animate-fade-in">
            © 2025 Todo App. All rights reserved.
          </p>
        </div>
      </footer>

     
    </div>
  );
}