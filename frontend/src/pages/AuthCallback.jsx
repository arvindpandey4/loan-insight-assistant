import { useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

export default function AuthCallback() {
  const { loading } = useAuth();

  useEffect(() => {
    // The AuthContext handles the token extraction
    // This component just shows a loading state
    if (!loading) {
      window.location.href = '/';
    }
  }, [loading]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Completing sign in...</p>
      </div>
    </div>
  );
}
