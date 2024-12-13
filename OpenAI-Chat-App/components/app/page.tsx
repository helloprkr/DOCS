import { ChatInterface } from "@/ai/components/chat";

export default function HomePage() {
  return (
    <main className="min-h-screen py-8">
      <h1 className="text-3xl font-bold text-center mb-8">OpenAI Chat Integration</h1>
      <ChatInterface />
    </main>
  );
} 