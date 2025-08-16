import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { 
  Dialog, 
  DialogContent, 
  DialogHeader, 
  DialogTitle, 
  DialogTrigger 
} from '@/components/ui/dialog';
import { cn } from '@/lib/utils';

interface AvatarStylePickerProps {
  currentEmoji?: string;
  currentColor?: string;
  onStyleChange: (emoji: string, color: string) => void;
  children: React.ReactNode;
}

const EMOJI_OPTIONS = [
  '🤖', '👤', '🧠', '💡', '⚡', '🔥', '🌟', '🎯', 
  '🚀', '💼', '🎨', '🔧', '📊', '🎵', '🏆', '💎',
  '🦄', '🐶', '🐱', '🦊', '🐼', '🦁', '🐸', '🦉',
  '🌈', '☀️', '🌙', '⭐', '🌸', '🌺', '🌻', '🌿'
];

const COLOR_OPTIONS = [
  '#6366f1', // Indigo
  '#8b5cf6', // Violet  
  '#ec4899', // Pink
  '#ef4444', // Red
  '#f97316', // Orange
  '#eab308', // Yellow
  '#22c55e', // Green
  '#06b6d4', // Cyan
  '#3b82f6', // Blue
  '#6366f1', // Indigo
  '#8b5cf6', // Violet
  '#a855f7', // Purple
  '#d946ef', // Fuchsia
  '#f43f5e', // Rose
  '#64748b', // Slate
  '#374151'  // Gray
];

export function AvatarStylePicker({ 
  currentEmoji = '🤖', 
  currentColor = '#6366f1', 
  onStyleChange, 
  children 
}: AvatarStylePickerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedEmoji, setSelectedEmoji] = useState(currentEmoji);
  const [selectedColor, setSelectedColor] = useState(currentColor);

  const handleSave = () => {
    onStyleChange(selectedEmoji, selectedColor);
    setIsOpen(false);
  };

  const handleCancel = () => {
    setSelectedEmoji(currentEmoji);
    setSelectedColor(currentColor);
    setIsOpen(false);
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        {children}
      </DialogTrigger>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Customize Agent Style</DialogTitle>
        </DialogHeader>
        
        <div className="space-y-6">
          {/* Preview */}
          <div className="flex flex-col items-center space-y-3">
            <div 
              className="w-16 h-16 rounded-2xl flex items-center justify-center text-2xl shadow-sm border"
              style={{ backgroundColor: selectedColor + '20', borderColor: selectedColor + '40' }}
            >
              {selectedEmoji}
            </div>
            <p className="text-sm text-muted-foreground">Preview</p>
          </div>

          {/* Emoji Selection */}
          <div className="space-y-3">
            <h4 className="text-sm font-medium">Choose Avatar</h4>
            <div className="grid grid-cols-8 gap-2">
              {EMOJI_OPTIONS.map((emoji) => (
                <button
                  key={emoji}
                  onClick={() => setSelectedEmoji(emoji)}
                  className={cn(
                    "w-8 h-8 rounded-lg flex items-center justify-center text-lg hover:bg-muted transition-colors",
                    selectedEmoji === emoji && "bg-primary/10 ring-2 ring-primary/20"
                  )}
                >
                  {emoji}
                </button>
              ))}
            </div>
          </div>

          {/* Color Selection */}
          <div className="space-y-3">
            <h4 className="text-sm font-medium">Choose Color</h4>
            <div className="grid grid-cols-8 gap-2">
              {COLOR_OPTIONS.map((color) => (
                <button
                  key={color}
                  onClick={() => setSelectedColor(color)}
                  className={cn(
                    "w-6 h-6 rounded-full border-2 border-white shadow-sm hover:scale-110 transition-transform",
                    selectedColor === color && "ring-2 ring-primary/50 ring-offset-1"
                  )}
                  style={{ backgroundColor: color }}
                />
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-end space-x-2 pt-4">
            <Button variant="outline" onClick={handleCancel}>
              Cancel
            </Button>
            <Button onClick={handleSave}>
              Save Changes
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}