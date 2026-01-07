'use client';

import { useState,useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/UI/Card';
import { Input } from '@/components/UI/Input';
import { Button } from '@/components/UI/Button';
import { useAuthHook } from '@/hooks/useAuth';
import { validateSignupForm } from '@/lib/validation';
import Link from 'next/link';

export default function SignupPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const router = useRouter();
  const { handleRegister, isAuthenticated } = useAuthHook();

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

    const validation = validateSignupForm(name, email, password, confirmPassword);

    if (!validation.isValid) {
      setErrors(validation.errors);
      setIsSubmitting(false);
      return;
    }

    // Clear previous errors
    setErrors({});

    try {
      const result = await handleRegister({
        email,
        password,
        name
      });

      if (result.success) {
        router.push('/dashboard');
      } else {
        // Handle specific error messages from backend
        if (result.error && (result.error.toLowerCase().includes('already exists') || result.error.toLowerCase().includes('email'))) {
          setErrors({
            email: 'A user with this email already exists. Please try logging in instead.'
          });
        } else {
          setErrors({ submit: result.error || 'Registration failed. Please try again.' });
        }
      }
    } catch (error) {
      // Handle different types of errors from API
      if (error instanceof Error) {
        if (error.message.toLowerCase().includes('already exists') || error.message.toLowerCase().includes('email')) {
          setErrors({
            email: 'A user with this email already exists. Please try logging in instead.'
          });
        } else {
          setErrors({ submit: error.message || 'Registration failed. Please try again.' });
        }
      } else {
        setErrors({ submit: 'An unexpected error occurred. Please try again.' });
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-black p-4 relative overflow-hidden">
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
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </div>
          </div>
          <CardTitle className="text-2xl font-bold text-white">Create Account</CardTitle>
          <CardDescription className="text-gray-400">
            Enter your information to create an account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4 animate-fade-in">
            <div className="animate-slide-in-left">
              <Input
                label="Full Name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                error={errors.name}
                placeholder="John Doe"
                required
                className="animate-scale"
              />
            </div>
            <div className="animate-slide-in-right">
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
            <div className="animate-slide-in-left">
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
            <div className="animate-slide-in-right">
              <Input
                label="Confirm Password"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                error={errors.confirmPassword}
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
              {isSubmitting ? 'Creating account...' : 'Sign Up'}
            </Button>
          </form>
          <div className="mt-6 text-center text-sm text-gray-500 animate-fade-in">
            Already have an account?{' '}
            <Link href="/login" className="font-semibold text-orange-500 hover:underline animate-scale">
              Sign in
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}