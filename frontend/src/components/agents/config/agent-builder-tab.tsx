import React from 'react';
import { AgentPreview } from '../agent-preview';
import { AvatarStylePicker } from './avatar-style-picker';
import { Button } from '@/components/ui/button';
import { Palette } from 'lucide-react';

interface AgentBuilderTabProps {
  agentId: string;
  displayData: {
    name: string;
    description: string;
    system_prompt: string;
    agentpress_tools: any;
    configured_mcps: any[];
    custom_mcps: any[];
    is_default: boolean;
    avatar?: string;
    avatar_color?: string;
  };
  isViewingOldVersion: boolean;
  onFieldChange: (field: string, value: any) => void;
  onStyleChange?: (emoji: string, color: string) => void;
  agentMetadata?: {
    is_suna_default?: boolean;
  };
}

export function AgentBuilderTab({
  agentId,
  displayData,
  isViewingOldVersion,
  onFieldChange,
  onStyleChange = () => {},
  agentMetadata,
}: AgentBuilderTabProps) {
  if (isViewingOldVersion) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center space-y-3 max-w-md px-6">
          <div className="text-4xl opacity-50">🔒</div>
          <div>
            <h3 className="text-base font-semibold text-foreground mb-1">Builder Unavailable</h3>
            <p className="text-sm text-muted-foreground">
              Only available for the current version. Please activate this version first.
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Create previewAgent object similar to main page
  const previewAgent = {
    agent_id: agentId,
    ...displayData,
  };

  return (
    <div className="h-full overflow-y-auto">
      {/* Avatar Style Customizer */}
      {!isViewingOldVersion && onStyleChange && (
        <div className="p-4 border-b bg-muted/30">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div 
                className="w-10 h-10 rounded-xl flex items-center justify-center text-lg border"
                style={{ 
                  backgroundColor: (displayData.avatar_color || '#6366f1') + '20', 
                  borderColor: (displayData.avatar_color || '#6366f1') + '40' 
                }}
              >
                {displayData.avatar || '🤖'}
              </div>
              <div>
                <h3 className="text-sm font-medium">Agent Style</h3>
                <p className="text-xs text-muted-foreground">Customize avatar and color</p>
              </div>
            </div>
            <AvatarStylePicker
              currentEmoji={displayData.avatar}
              currentColor={displayData.avatar_color}
              onStyleChange={onStyleChange}
            >
              <Button variant="outline" size="sm">
                <Palette className="w-4 h-4 mr-2" />
                Customize
              </Button>
            </AvatarStylePicker>
          </div>
        </div>
      )}
      
      {previewAgent && <AgentPreview agent={previewAgent} agentMetadata={agentMetadata} />}
    </div>
  );
} 