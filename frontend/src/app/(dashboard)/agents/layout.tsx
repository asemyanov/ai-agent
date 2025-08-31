import { Metadata } from 'next';
import { redirect } from 'next/navigation';

export const metadata: Metadata = {
  title: 'Agent Conversation | MEVO',
  description: 'Interactive agent conversation powered by MEVO',
  openGraph: {
    title: 'Agent Conversation | MEVO',
    description: 'Interactive agent conversation powered by MEVO',
    type: 'website',
  },
};

export default async function AgentsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
