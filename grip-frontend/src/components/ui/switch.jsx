import React from 'react';

export const Switch = ({ 
  checked = false, 
  onCheckedChange, 
  disabled = false, 
  className = '', 
  id,
  ...props 
}) => {
  const handleChange = (e) => {
    if (onCheckedChange) {
      onCheckedChange(e.target.checked);
    }
  };

  return (
    <button
      role="switch"
      aria-checked={checked}
      aria-disabled={disabled}
      onClick={(e) => {
        e.preventDefault();
        if (!disabled && onCheckedChange) {
          onCheckedChange(!checked);
        }
      }}
      className={`
        relative inline-flex h-6 w-11 items-center rounded-full
        transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2
        ${checked ? 'bg-primary' : 'bg-input'}
        ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        ${className}
      `}
      id={id}
      disabled={disabled}
      {...props}
    >
      <span
        className={`
          pointer-events-none block h-5 w-5 rounded-full bg-background shadow-lg ring-0
          transition-transform
          ${checked ? 'translate-x-6' : 'translate-x-1'}
        `}
      />
    </button>
  );
};