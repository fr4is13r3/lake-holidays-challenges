import React from 'react';
import { CheckCircle, X } from 'lucide-react';

interface SuccessModalProps {
  isOpen: boolean;
  title: string;
  message: string;
  onClose: () => void;
}

export const SuccessModal: React.FC<SuccessModalProps> = ({
  isOpen,
  title,
  message,
  onClose
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-md animate-pulse">
        <div className="text-center">
          {/* Close button */}
          <button
            onClick={onClose}
            className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
          >
            <X className="w-6 h-6" />
          </button>

          {/* Success icon */}
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <CheckCircle className="w-12 h-12 text-green-500" />
          </div>

          {/* Title */}
          <h2 className="text-2xl font-bold text-gray-800 mb-4">{title}</h2>

          {/* Message */}
          <p className="text-gray-600 mb-8">{message}</p>

          {/* OK button */}
          <button
            onClick={onClose}
            className="w-full bg-gradient-to-r from-green-400 to-blue-400 text-white py-4 rounded-2xl font-semibold text-lg hover:from-green-500 hover:to-blue-500 transition-all duration-200 transform hover:scale-105"
          >
            Parfait !
          </button>
        </div>
      </div>
    </div>
  );
};