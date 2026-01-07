'use client';

import { useState , useEffect} from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/UI/Card';
import { Input } from '@/components/UI/Input';
import { Button } from '@/components/UI/Button';
import { useAuthHook } from '@/hooks/useAuth';
import { validateLoginForm } from '@/lib/validation';
import Link from 'next/link';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const router = useRouter();
  const { handleLogin, isAuthenticated } = useAuthHook();

  useEffect(() => {
    setIsVisible(true);
    if (isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router]);

  if (isAuthenticated) {
    return null; // Don't render anything while redirecting
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    const validation = validateLoginForm(email, password);

    if (!validation.isValid) {
      setErrors(validation.errors);
      setIsSubmitting(false);
      return;
    }

    // Clear previous errors
    setErrors({});

    try {
      const result = await handleLogin({ email, password });
      if (result.success) {
        router.push('/dashboard');
      } else {
        // Handle specific error messages from backend
        if (result.error && (result.error.includes('401') || result.error.toLowerCase().includes('invalid') || result.error.toLowerCase().includes('password') || result.error.toLowerCase().includes('email'))) {
          setErrors({
            password: 'Invalid email or password. Please try again.'
          });
        } else if (result.error && result.error.includes('404')) {
          setErrors({
            email: 'No account found with this email. Please check your email or sign up.'
          });
        } else {
          setErrors({ submit: result.error || 'Login failed. Please try again.' });
        }
      }
    } catch (error) {
      // Handle different types of errors from API
      if (error instanceof Error) {
        if (error.message.includes('401') || error.message.toLowerCase().includes('invalid') || error.message.toLowerCase().includes('password') || error.message.toLowerCase().includes('email')) {
          setErrors({
            password: 'Invalid email or password. Please try again.'
          });
        } else if (error.message.includes('404')) {
          setErrors({
            email: 'No account found with this email. Please check your email or sign up.'
          });
        } else {
          setErrors({ submit: error.message || 'Login failed. Please try again.' });
        }
      } else {
        setErrors({ submit: 'An unexpected error occurred. Please try again.' });
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center from-gray-900 to-black p-4 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden -z-10">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-orange-500/5 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-yellow-500/5 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      <Card className={`w-full max-w-md animate-fade-in ${isVisible ? 'opacity-100' : 'opacity-0'}`}>
        <CardHeader className="text-center animate-slide-in-down">
          <div className="flex justify-center mb-4">
            <div className="w-12 h-12 bg-orange-500 rounded-lg flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
          </div>
          <CardTitle className="text-2xl font-bold text-white">Welcome Back</CardTitle>
          <CardDescription className="text-gray-400">
            Enter your credentials to access your account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4 animate-fade-in">
            <div className="animate-slide-in-left">
              <Input
                label="Email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                error={errors.email}
                placeholder="your@email.com"
                required
                className="animate-scale"
              />
            </div>
            <div className="animate-slide-in-right">
              <Input
                label="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                error={errors.password}
                placeholder="••••••••"
                required
                className="animate-scale"
              />
            </div>
            {errors.submit && (
              <div className="text-red-500 text-sm animate-fade-in">{errors.submit}</div>
            )}
            <Button
              type="submit"
              className="w-full animate-scale"
              variant="primary"
              loading={isSubmitting}
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Signing in...' : 'Sign In'}
            </Button>
          </form>
          <div className="mt-6 text-center text-sm text-gray-500 animate-fade-in">
            Don't have an account?{' '}
            <Link href="/signup" className="font-semibold text-orange-500 hover:underline animate-scale">
              Sign up
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}