'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import {
  BarChart3,
  Bot,
  Briefcase,
  Settings,
  Sparkles,
  RefreshCw,
  TrendingUp,
  Users,
  Shield,
  Zap,
  Target,
  Brain,
  Globe,
  Heart,
  PenTool,
  Code,
  Camera,
  Calendar,
  DollarSign,
  Rocket,
} from 'lucide-react';

type PromptExample = {
  title: string;
  query: string;
  icon: React.ReactNode;
};

const allPrompts: PromptExample[] = [
  {
    title: 'Patient Scheduling and Reminders',
    query: 'Automate appointment scheduling, send intelligent reminders, and handle cancellations or rescheduling requests through natural language processing.',
    icon: <Calendar className="text-amber-700 dark:text-amber-400" size={16} />,
  },
  {
    title: 'Insurance Prior Authorization',
    query: 'Streamline insurance verification processes and automate prior authorization requests using intelligent document processing and real-time payer integration.',
    icon: <Shield className="text-red-700 dark:text-red-400" size={16} />,
  },
  {
    title: 'Medical Coding and Billing Audit',
    query: 'Automatically assign ICD-10 and CPT codes from clinical documentation while conducting real-time billing audits to ensure accuracy and compliance.',
    icon: <Code className="text-violet-700 dark:text-violet-400" size={16} />,
  },
  {
    title: 'Patients Recovery EHR Analysis',
    query: 'Identify patterns, track treatment efficacy, and generate comprehensive clinical insights for improved care coordination and decision support.',
    icon: <Heart className="text-red-600 dark:text-red-300" size={16} />,
  },
  {
    title: 'Post-Op Recovery Analysis',
    query: 'Compare post-op recovery metrics against 100 similar cases and flag any protocol deviations.',
    icon: <TrendingUp className="text-teal-700 dark:text-teal-400" size={16} />,
  },
  {
    title: 'Create Pre-op Guidelines Handout',
    query: 'Compile latest pre-op guidelines from the past 6 months and create a clinical handout highlighting pre-op workflow impacts and protocol changes.',
    icon: <PenTool className="text-indigo-700 dark:text-indigo-400" size={16} />,
  },
  {
    title: 'Under-Researched Biomarkers',
    query: "Identify top 5 under-researched Alzheimer's biomarkers since 2020 using PubMed analysis. Generate a comprehensive report highlighting research gaps and potential clinical applications.",
    icon: <Brain className="text-pink-700 dark:text-pink-400" size={16} />,
  },
  {
    title: 'NIH Grant Justification Section',
    query: "Generate a comprehensive justification section analyzing success rates of similar Parkinson's research proposals for NIH grant applications. Include historical funding trends, priority areas, and strategic positioning recommendations.",
    icon: <DollarSign className="text-emerald-700 dark:text-emerald-400" size={16} />,
  },
  {
    title: 'Predict Q3 ER Admissions',
    query: "Analyze historical admission data and local flu trends to generate staffing recommendations for the upcoming quarter's emergency room patient volume.",
    icon: <TrendingUp className="text-teal-700 dark:text-teal-400" size={16} />,
  },
  {
    title: 'Medicare ACO Renewal Compliance',
    query: 'Generate a comprehensive compliance readiness report for Medicare ACO renewal, analyzing current documentation gaps and producing an actionable priority list with implementation timelines.',
    icon: <Shield className="text-red-700 dark:text-red-400" size={16} />,
  },
  {
    title: 'Surgical Outcomes Benchmarks',
    query: 'Compare surgical outcomes against top 10 US hospitals, analyze performance gaps, and create a comprehensive quality improvement roadmap with actionable steps to enhance surgical standards and patient outcomes.',
    icon: <Target className="text-orange-700 dark:text-orange-400" size={16} />,
  },
  {
    title: 'Dashboard: Current Capacity vs Surge',
    query: 'Interactive dashboard that compares current hospital capacity with CDC COVID surge prediction models, enabling healthcare administrators to visualize resource allocation needs and prepare for potential patient influxes.',
    icon: <BarChart3 className="text-green-700 dark:text-green-400" size={16} />,
  },
  {
    title: 'Analyze Clinical Trial Data',
    query: 'Analyze a dataset of clinical trial results to identify statistically significant outcomes and potential adverse effects. Generate a summary report for a medical journal.',
    icon: <Bot className="text-blue-700 dark:text-blue-400" size={16} />,
  },
  {
    title: 'Draft a Patient Discharge Summary',
    query: 'Draft a comprehensive discharge summary for a patient recovering from pneumonia, including medication reconciliation, follow-up appointments, and lifestyle recommendations.',
    icon: <Briefcase className="text-rose-700 dark:text-rose-400" size={16} />,
  },
  {
    title: 'Develop a Clinical Pathway for Diabetes',
    query: 'Develop a clinical pathway for managing Type 2 Diabetes, from diagnosis to long-term care. Include decision trees for treatment options based on patient characteristics.',
    icon: <Settings className="text-purple-700 dark:text-purple-400" size={16} />,
  },
  {
    title: 'Generate a Literature Review on Chronic Pain',
    query: 'Generate a literature review on the latest non-pharmacological treatments for chronic pain, summarizing findings from the top 10 most-cited papers in the last two years.',
    icon: <PenTool className="text-indigo-700 dark:text-indigo-400" size={16} />,
  },
  {
    title: 'Create a Medical Staffing Schedule',
    query: 'Create a fair and balanced 4-week rotating schedule for a team of 15 nurses and 5 doctors in a busy emergency department, considering shift preferences and required certifications.',
    icon: <Users className="text-cyan-700 dark:text-cyan-400" size={16} />,
  },
  {
    title: 'Summarize a Medical Research Paper',
    query: 'Summarize the key findings, methodology, and conclusions of the attached medical research paper on CAR-T cell therapy for a presentation to the oncology department.',
    icon: <Sparkles className="text-fuchsia-700 dark:text-fuchsia-400" size={16} />,
  },
  {
    title: 'Develop a Health and Wellness Program',
    query: 'Design a 12-week health and wellness program for a corporate client, focusing on stress reduction, nutrition, and physical activity. Include weekly themes and measurable goals.',
    icon: <Heart className="text-red-600 dark:text-red-300" size={16} />,
  },
];

// Function to get random prompts
const getRandomPrompts = (count: number = 3): PromptExample[] => {
  const shuffled = [...allPrompts].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
};

export const Examples = ({
  onSelectPrompt,
  count = 3,
}: {
  onSelectPrompt?: (query: string) => void;
  count?: number;
}) => {
  const [displayedPrompts, setDisplayedPrompts] = useState<PromptExample[]>([]);
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Initialize with random prompts on mount
  useEffect(() => {
    setDisplayedPrompts(getRandomPrompts(count));
  }, [count]);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setDisplayedPrompts(getRandomPrompts(count));
    setTimeout(() => setIsRefreshing(false), 300);
  };

  return (
    <div className="w-full max-w-4xl mx-auto px-4">
      <div className="group relative">
        <div className="flex gap-2 justify-center py-2 flex-wrap">
          {displayedPrompts.map((prompt, index) => (
            <motion.div
              key={`${prompt.title}-${index}`}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{
                duration: 0.3,
                delay: index * 0.03,
                ease: "easeOut"
              }}
            >
              <Button
                variant="outline"
                className="w-fit h-fit px-3 py-2 rounded-full border-neutral-200 dark:border-neutral-800 bg-neutral-50 hover:bg-neutral-100 dark:bg-neutral-900 dark:hover:bg-neutral-800 text-sm font-normal text-muted-foreground hover:text-foreground transition-colors"
                onClick={() => onSelectPrompt && onSelectPrompt(prompt.query)}
              >
                <div className="flex items-center gap-2">
                  <div className="flex-shrink-0">
                    {React.cloneElement(prompt.icon as React.ReactElement, { size: 14 })}
                  </div>
                  <span className="whitespace-nowrap">{prompt.title}</span>
                </div>
              </Button>
            </motion.div>
          ))}
        </div>

        {/* Refresh button that appears on hover */}
        <Button
          variant="ghost"
          size="sm"
          onClick={handleRefresh}
          className="absolute -top-4 right-1 h-5 w-5 p-0 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-200 hover:bg-neutral-100 dark:hover:bg-neutral-800"
        >
          <motion.div
            animate={{ rotate: isRefreshing ? 360 : 0 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
          >
            <RefreshCw size={10} className="text-muted-foreground" />
          </motion.div>
        </Button>
      </div>
    </div>
  );
};