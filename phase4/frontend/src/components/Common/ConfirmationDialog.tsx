// Confirmation dialog component for user actions
import { Button } from '@/components/UI/Button';
import { Modal } from '@/components/UI/Modal';
import { cn } from '@/lib/utils';
import { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';

interface ConfirmationDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  variant?: 'default' | 'destructive';
  loading?: boolean;
}

export const ConfirmationDialog = ({
  isOpen,
  onClose,
  onConfirm,
  title,
  message,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  variant = 'default',
  loading = false
}: ConfirmationDialogProps) => {
  const variantClasses = variant === 'destructive'
    ? 'bg-red-500 hover:bg-red-600 text-white'
    : 'bg-orange-500 hover:bg-orange-600 text-white';

  if (!isOpen) return null;

  // The portal root is now guaranteed to exist in layout.tsx,
  // so we can directly attempt to render the portal.
  const portalRoot = typeof window !== 'undefined' ? document.getElementById('confirmation-dialog-root') : null;

  if (!portalRoot) {
    // This should not happen if layout.tsx is correct, but it's a safe fallback.
    return null;
  }

  return createPortal(
    <Modal isOpen={isOpen} onClose={onClose}>
      <div className="p-6">
        <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
        <p className="text-gray-400 mb-6">{message}</p>
        <div className="flex justify-end space-x-3">
          <Button
            variant="outline"
            onClick={onClose}
            disabled={loading}
          >
            {cancelText}
          </Button>
          <Button
            variant="primary"
            onClick={onConfirm}
            disabled={loading}
            className={cn(variantClasses)}
          >
            {loading ? 'Processing...' : confirmText}
          </Button>
        </div>
      </div>
    </Modal>,
    portalRoot
  );
};