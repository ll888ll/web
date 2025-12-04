import React from 'react';
import { cn } from '@/lib/utils';

interface {{ComponentName}}Props {
  className?: string;
  children?: React.ReactNode;
}

export const {{ComponentName}}: React.FC<{{ComponentName}}Props> = ({ 
  className, 
  children 
}) => {
  return (
    <div className={cn(
      // Base Nocturne styles
      "bg-croody-dark text-white relative overflow-hidden",
      // Noise texture overlay
      "before:content-[''] before:absolute before:inset-0 before:bg-noise before:opacity-5",
      // Border & Glow
      "border border-white/10 shadow-[0_0_15px_rgba(0,255,128,0.05)]",
      className
    )}>
      <h2 className="font-baloo text-2xl mb-4 text-croody-neon-green">
        {{ComponentName}}
      </h2>
      <div className="font-inter text-croody-gray-300">
        {children}
      </div>
    </div>
  );
};
