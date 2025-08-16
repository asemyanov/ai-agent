import React from 'react';
import { AgentPreview } from '../agent-preview';

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
      {previewAgent && <AgentPreview agent={previewAgent} agentMetadata={agentMetadata} />}
    </div>
  );
} 